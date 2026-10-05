#!/usr/bin/env python3
"""Baut stuetz.wiki aus content/*.md nach _site/ (statisches HTML für GitHub Pages).

Aufruf:  python3 build.py

Artikel liegen in content/<Titel>.md (Leerzeichen im Titel als _ schreiben):

    +++
    title = "Annotation (Java)"        # optional, sonst aus dem Dateinamen
    redirects = ["CDI", "DDL|DDL"]     # Weiterleitungen; "Name|Abschnitt" springt zu einem Abschnitt
    navbox = ["backend"]               # Navigationsleisten aus content/_navboxes.toml
    type = "begriffsklaerung"          # optional: Begriffsklärungsseite
    [infobox]
    Art = "Java-Framework"
    +++

Markup im Text:
    ## Abschnitt / ### Unterabschnitt
    **fett**, *kursiv*, `code`
    [[Artikel]], [[Artikel|Text]], [[Artikel#Abschnitt|Text]], [[#Abschnitt|Text]]
    - Liste (eingerückt = Unterliste), 1. nummerierte Liste
    | Tabelle | mit | Kopfzeile |   (zweite Zeile |---|---|; Zelle mit "!" davor = Zeilenkopf)
    ; Begriff  und darunter  : Definition
    :: Hinweiszeile
    ```java ... ```  Codeblock
"""

import html
import json
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

try:
    from zoneinfo import ZoneInfo

    TZ = ZoneInfo("Europe/Vienna")
except Exception:  # keine Zeitzonendaten verfügbar
    TZ = timezone.utc

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
OUT = ROOT / "_site"

SITE = "stuetz.wiki"
BASE_URL = "https://stuetz.wiki"
REPO = "https://github.com/EldinBegano/stuetz-wiki"
MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
          "August", "September", "Oktober", "November", "Dezember"]

INLINE = re.compile(r"`([^`]+)`|\[\[([^\]]+)\]\]")
HEADING = re.compile(r"^(#{2,4})\s+(.+?)\s*$")
LIST_ITEM = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
TABLE_SEP = re.compile(r"^:?-{3,}:?$")
CELL_SPLIT = re.compile(r"\|(?![^\[]*\]\])")  # | außerhalb von [[...]]


def esc(s):
    return html.escape(s, quote=True)


def slug(title):
    return title.replace(" ", "_")


def anchor_id(text):
    return text.strip().replace(" ", "_")


def page_url(title):
    return "/wiki/" + quote(slug(title), safe="()_:,.!-'*@")


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


BLOCK_TAG = re.compile(r"</?(?:p|div|li|ul|ol|dl|dt|dd|h[1-6]|table|tr|th|td|pre|br)\b[^>]*>")


def plain(s):
    return re.sub(r"\s+", " ", strip_tags(BLOCK_TAG.sub(" ", s))).strip()


def sort_key(title):
    t = title.casefold()
    for a, b in (("ä", "a"), ("ö", "o"), ("ü", "u"), ("ß", "ss")):
        t = t.replace(a, b)
    return t


def script_json(value):
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")


def last_modified(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cI", "--", str(path)],
                             cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except OSError:
        out = ""
    dt = datetime.fromisoformat(out) if out else datetime.now(timezone.utc)
    dt = dt.astimezone(TZ)
    return f"{dt.day}. {MONTHS[dt.month - 1]} {dt.year} um {dt:%H:%M} Uhr"


class Article:
    def __init__(self, path):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"\+\+\+\n(.*?)\n?\+\+\+\n?", text, re.S)
        meta = tomllib.loads(m.group(1)) if m else {}
        self.path = path
        self.source = text[m.end():] if m else text
        self.title = meta.get("title", path.stem.replace("_", " "))
        self.url = page_url(self.title)
        self.redirects = [tuple(p.strip() for p in r.partition("|")[::2])
                          for r in meta.get("redirects", [])]
        self.infobox = meta.get("infobox", {})
        self.navboxes = meta.get("navbox", [])
        self.disambig = meta.get("type") == "begriffsklaerung"


class Wiki:
    def __init__(self):
        self.navboxes = tomllib.loads((CONTENT / "_navboxes.toml").read_text(encoding="utf-8"))
        self.articles = [Article(p) for p in sorted(CONTENT.glob("*.md"))
                         if not p.name.startswith("_")]
        self.titles = {}  # casefold-Titel -> (Artikel, Abschnitt)
        self.red_links = set()
        for a in self.articles:
            self._add(a.title, (a, ""))
        for a in self.articles:
            for name, anchor in a.redirects:
                self._add(name, (a, anchor))
            for key in a.navboxes:
                if key not in self.navboxes:
                    sys.exit(f"{a.path.name}: unbekannte navbox {key!r}")

    def _add(self, title, entry):
        if title.startswith(".") or "/" in title or title.startswith("Spezial:") \
                or title == "Hauptseite":
            sys.exit(f"Ungültiger Titel: {title!r}")
        key = title.casefold()
        if key in self.titles:
            sys.exit(f"Titel doppelt vergeben (Groß-/Kleinschreibung zählt nicht): {title!r}")
        self.titles[key] = entry

    def resolve(self, title):
        return self.titles.get(title.replace("_", " ").strip().casefold())


class Renderer:
    """Wandelt das Wiki-Markup eines Artikels in HTML um."""

    def __init__(self, wiki, article=None):
        self.wiki = wiki
        self.article = article
        self.headings = []  # (Ebene, Text, id)

    # ----- Inline -----

    def inline(self, text):
        out, pos = [], 0
        for m in INLINE.finditer(text):
            out.append(self.fmt(text[pos:m.start()]))
            if m.group(1) is not None:
                out.append(f"<code>{esc(m.group(1))}</code>")
            else:
                out.append(self.link(m.group(2)))
            pos = m.end()
        out.append(self.fmt(text[pos:]))
        return "".join(out)

    @staticmethod
    def fmt(text):
        s = html.escape(text, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        return re.sub(r"(?<![\w*])\*(?=\S)(.+?)(?<=\S)\*(?![\w*])", r"<i>\1</i>", s)

    def link(self, spec):
        target, _, label = spec.partition("|")
        page, _, anchor = target.partition("#")
        page, anchor = page.strip(), anchor.strip()
        text = self.fmt(label.strip() or page or anchor)
        if not page:
            return f'<a href="#{esc(anchor_id(anchor))}">{text}</a>'
        hit = self.wiki.resolve(page)
        if hit is None:
            self.wiki.red_links.add(page)
            return (f'<a href="{page_url(page)}" class="new" '
                    f'title="{esc(page)} (Seite nicht vorhanden)">{text}</a>')
        art, redirect_anchor = hit
        anchor = anchor or redirect_anchor
        frag = f"#{esc(anchor_id(anchor))}" if anchor else ""
        if art is self.article:
            return f'<a href="{frag}">{text}</a>' if frag else f'<b class="selflink">{text}</b>'
        return f'<a href="{art.url}{frag}" title="{esc(art.title)}">{text}</a>'

    # ----- Blöcke -----

    @staticmethod
    def starts_block(s):
        return (not s or s.startswith(("```", "|", ";", ":"))
                or HEADING.match(s) or LIST_ITEM.match(s))

    def blocks(self, src):
        lines = src.replace("\t", "    ").split("\n")
        out, i, n = [], 0, len(lines)
        while i < n:
            s = lines[i].strip()
            if not s:
                i += 1
            elif s.startswith("```"):
                i += 1
                code = []
                while i < n and not lines[i].strip().startswith("```"):
                    code.append(lines[i])
                    i += 1
                i += 1
                out.append("<pre><code>" + esc("\n".join(code)) + "</code></pre>")
            elif m := HEADING.match(s):
                level, inner = len(m.group(1)), self.inline(m.group(2))
                hid = anchor_id(plain(inner))
                self.headings.append((level, plain(inner), hid))
                out.append(f'<h{level} id="{esc(hid)}">{inner}</h{level}>')
                i += 1
            elif s.startswith("::"):
                out.append(f'<div class="hatnote">{self.inline(s[2:].strip())}</div>')
                i += 1
            elif s.startswith("|"):
                rows = []
                while i < n and lines[i].strip().startswith("|"):
                    row = lines[i].strip()[1:]
                    row = row[:-1] if row.endswith("|") else row
                    rows.append([c.strip() for c in CELL_SPLIT.split(row)])
                    i += 1
                out.append(self.table(rows))
            elif s.startswith((";", ":")):
                items = []
                while i < n and lines[i].strip().startswith((";", ":")) \
                        and not lines[i].strip().startswith("::"):
                    t = lines[i].strip()
                    inner = self.inline(t[1:].strip())
                    if t[0] == ";":
                        items.append(f'<dt id="{esc(anchor_id(plain(inner)))}">{inner}</dt>')
                    else:
                        items.append(f"<dd>{inner}</dd>")
                    i += 1
                out.append("<dl>" + "".join(items) + "</dl>")
            elif LIST_ITEM.match(lines[i]):
                items = []
                while i < n:
                    m = LIST_ITEM.match(lines[i])
                    if m:
                        items.append([len(m.group(1)), m.group(2)[-1] == ".", m.group(3)])
                    elif items and not self.starts_block(lines[i].strip()):
                        items[-1][2] += " " + lines[i].strip()  # Fortsetzungszeile
                    else:
                        break
                    i += 1
                out.append(self.list(items))
            else:
                para = []
                while i < n and lines[i].strip() and not (para and self.starts_block(lines[i].strip())):
                    para.append(lines[i].strip())
                    i += 1
                out.append(f"<p>{self.inline(' '.join(para))}</p>")
        return "\n".join(out)

    def list(self, items):
        out, stack = [], []  # stack: (Einrückung, Tag)
        for indent, ordered, text in items:
            tag = "ol" if ordered else "ul"
            if not stack or indent > stack[-1][0]:
                out.append(f"<{tag}>")
                stack.append((indent, tag))
            else:
                while len(stack) > 1 and indent < stack[-1][0]:
                    out.append(f"</li></{stack.pop()[1]}>")
                out.append("</li>")
            out.append(f"<li>{self.inline(text)}")
        while stack:
            out.append(f"</li></{stack.pop()[1]}>")
        return "".join(out)

    def table(self, rows):
        head = None
        if len(rows) > 1 and all(TABLE_SEP.match(c.replace(" ", "")) for c in rows[1]):
            head, rows = rows[0], rows[2:]
        out = ['<div class="table-wrap"><table class="wikitable">']
        if head:
            cells = "".join(f'<th scope="col">{self.inline(c)}</th>' for c in head)
            out.append(f"<thead><tr>{cells}</tr></thead>")
        out.append("<tbody>")
        for row in rows:
            cells = "".join(f'<th scope="row">{self.inline(c[1:].strip())}</th>' if c.startswith("!")
                            else f"<td>{self.inline(c)}</td>" for c in row)
            out.append(f"<tr>{cells}</tr>")
        out.append("</tbody></table></div>")
        return "".join(out)

    # ----- Bausteine -----

    def infobox(self, title, data):
        if not data:
            return ""
        rows = []
        for key, value in data.items():
            values = value if isinstance(value, list) else [value]
            cell = "<br>".join(self.inline(str(v)) for v in values)
            rows.append(f'<tr><th scope="row">{self.inline(key)}</th><td>{cell}</td></tr>')
        return (f'<table class="infobox"><tr><th colspan="2" class="infobox-title">{esc(title)}</th></tr>'
                + "".join(rows) + "</table>")

    def navbox(self, box):
        rows = []
        for group, items in box["gruppen"].items():
            links = "".join(f"<li>{self.inline('[[' + item + ']]')}</li>" for item in items)
            rows.append(f'<tr><th scope="row">{esc(group)}</th><td><ul>{links}</ul></td></tr>')
        return (f'<details class="navbox" open><summary>{esc(box["titel"])}</summary>'
                f'<table>{"".join(rows)}</table></details>')


def toc_html(headings):
    if len(headings) < 2:
        return ""
    base = min(level for level, _, _ in headings)
    items = ['<li class="toc-level-1"><a href="#">(Anfang)</a></li>']
    for level, text, hid in headings:
        items.append(f'<li class="toc-level-{level - base + 1}"><a href="#{esc(hid)}">{esc(text)}</a></li>')
    return ('<nav class="toc" aria-labelledby="toc-heading"><h2 id="toc-heading">Inhalt</h2>'
            f'<ul>{"".join(items)}</ul></nav>')


def layout(title, content, *, path, description="", toc="", tab="Artikel", source=None,
           sub="", modified=None, head="", special=None, noindex=False, body_class=""):
    actions = f'<li class="selected"><a href="{path}">Lesen</a></li>'
    if source:
        rel = quote(source.relative_to(ROOT).as_posix())
        actions += (f'<li><a href="{REPO}/edit/main/{rel}">Bearbeiten</a></li>'
                    f'<li><a href="{REPO}/commits/main/{rel}">Versionsgeschichte</a></li>')
    meta = f'<meta name="description" content="{esc(description)}">\n' if description else ""
    meta += ('<meta name="robots" content="noindex">' if noindex
             else f'<link rel="canonical" href="{BASE_URL}{path}">')
    footer = f"<p>Diese Seite wurde zuletzt am {modified} bearbeitet.</p>" if modified else ""
    attrs = (f' data-special="{special}"' if special else "") + (f' class="{body_class}"' if body_class else "")
    html_title = f"{title} – {SITE}" if title != SITE else SITE
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
{head}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(html_title)}</title>
{meta}
<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/static/wiki.css">
<script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<script src="/static/wiki.js" defer></script>
</head>
<body{attrs}>
<a class="skip-link" href="#content">Zum Inhalt springen</a>
<header class="site-header">
  <button class="menu-toggle" type="button" aria-label="Hauptmenü" aria-expanded="false" aria-controls="sidebar">
    <svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path fill="currentColor" d="M1 3h18v2H1zm0 6h18v2H1zm0 6h18v2H1z"/></svg>
  </button>
  <a class="logo" href="/"><span class="logo-mark" aria-hidden="true">S</span><span class="logo-text">stuetz.wiki</span></a>
  <form class="search" action="/wiki/Spezial:Suche" role="search">
    <input type="search" name="search" placeholder="stuetz.wiki durchsuchen" aria-label="stuetz.wiki durchsuchen"
           autocomplete="off" role="combobox" aria-autocomplete="list" aria-controls="suggestions" aria-expanded="false">
    <button type="submit">Suchen</button>
    <ul class="suggestions" id="suggestions" role="listbox" hidden></ul>
  </form>
</header>
<div class="page">
  <aside class="sidebar" id="sidebar" aria-label="Seitenleiste">
    <div class="sidebar-inner">
      <nav class="main-menu" aria-labelledby="menu-heading">
        <h2 id="menu-heading">Navigation</h2>
        <ul>
          <li><a href="/">Hauptseite</a></li>
          <li><a href="/wiki/Spezial:Alle_Seiten">Alle Artikel</a></li>
          <li><a href="/wiki/Spezial:Zuf%C3%A4llige_Seite">Zufälliger Artikel</a></li>
          <li><a href="/wiki/Spezial:Suche">Suche</a></li>
          <li><a href="{REPO}">Quelltext auf GitHub</a></li>
        </ul>
        <h2>Darstellung</h2>
        <fieldset class="theme-switch">
          <legend class="visually-hidden">Farbschema</legend>
          <label><input type="radio" name="theme" value="auto" checked> Automatisch</label>
          <label><input type="radio" name="theme" value="light"> Hell</label>
          <label><input type="radio" name="theme" value="dark"> Dunkel</label>
        </fieldset>
      </nav>
      {toc}
    </div>
  </aside>
  <div class="sidebar-backdrop"></div>
  <main class="content" id="content">
    <h1 id="firstHeading">{esc(title)}</h1>
    <nav class="tabs" aria-label="Seitenaktionen">
      <ul><li class="selected"><a href="{path}">{tab}</a></li></ul>
      <ul>{actions}</ul>
    </nav>
    <div id="siteSub">Aus stuetz.wiki</div>
    <div id="contentSub">{sub}</div>
    {content}
    <footer class="page-footer">
      {footer}
      <ul><li><a href="/">Hauptseite</a></li><li><a href="/wiki/Spezial:Alle_Seiten">Alle Artikel</a></li><li><a href="{REPO}">Quelltext auf GitHub</a></li></ul>
    </footer>
  </main>
</div>
</body>
</html>
"""


def description_of(body_html):
    m = re.search(r"<p>(.*?)</p>", body_html, re.S)
    text = plain(m.group(1)) if m else ""
    first = re.match(r"(.+?[.!?])(?=\s|$)", text)
    text = first.group(1) if first else text
    return text if len(text) <= 160 else text[:157].rsplit(" ", 1)[0] + " …"


def write(rel, text):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def redirect_page(name, art, anchor):
    target = art.url + (f"#{anchor_id(anchor)}" if anchor else "")
    shown = art.title + (f"#{anchor}" if anchor else "")
    frag = f"#{anchor_id(anchor)}" if anchor else ""
    head = ("<script>(function(){var q=new URLSearchParams(location.search);"
            'if(q.get("redirect")!=="no")location.replace('
            f'{script_json(art.url)}+"?rdfrom="+encodeURIComponent({script_json(name)})'
            f"+(location.hash||{script_json(frag)}));}})();</script>\n"
            f'<noscript><meta http-equiv="refresh" content="0; url={esc(target)}"></noscript>\n')
    content = ('<div class="body"><div class="redirectMsg"><p>Weiterleitung nach:</p>'
               f'<ul class="redirectText"><li><a href="{esc(target)}">{esc(shown)}</a></li></ul></div></div>')
    return layout(name, content, path=page_url(name), sub="Weiterleitungsseite", head=head,
                  source=art.path, noindex=True)


def main_page(wiki, rendered):
    r = Renderer(wiki)
    articles = [a for a in wiki.articles if not a.disambig]
    hits = (wiki.resolve(item.partition("|")[0])
            for box in wiki.navboxes.values() for items in box["gruppen"].values() for item in items)
    in_navbox = {hit[0] for hit in hits if hit}
    boxes = []
    teststoff = wiki.resolve("Teststoff")
    if teststoff:
        lead = re.search(r"<p>.*?</p>", rendered[teststoff[0]], re.S)
        boxes.append('<section class="mp-box mp-featured"><h2>Teststoff</h2><div class="mp-box-body">'
                     f'{lead.group(0) if lead else ""}</div></section>')
    for box in wiki.navboxes.values():
        groups = "".join(f"<h3>{esc(g)}</h3><ul>"
                         + "".join(f"<li>{r.inline('[[' + it + ']]')}</li>" for it in items) + "</ul>"
                         for g, items in box["gruppen"].items())
        boxes.append(f'<section class="mp-box"><h2>{esc(box["titel"])}</h2>'
                     f'<div class="mp-box-body">{groups}</div></section>')
    rest = sorted((a for a in articles if a not in in_navbox), key=lambda a: sort_key(a.title))
    if rest:
        links = "".join(f"<li>{r.inline('[[' + a.title + ']]')}</li>" for a in rest)
        boxes.append(f'<section class="mp-box"><h2>Weitere Artikel</h2>'
                     f'<div class="mp-box-body"><ul>{links}</ul></div></section>')
    content = ('<div class="body mainpage">'
               '<div class="mp-welcome"><p class="mp-welcome-title">Willkommen bei <b>stuetz.wiki</b></p>'
               f'<p class="mp-welcome-count"><a href="/wiki/Spezial:Alle_Seiten">{len(articles)} Artikel</a></p></div>'
               f'<div class="mp-grid">{"".join(boxes)}</div></div>')
    return layout(SITE, content, path="/", tab="Hauptseite", body_class="is-mainpage",
                  description=f"{SITE} – {len(articles)} Artikel")


def all_pages(wiki):
    entries = [(a.title, a.url, False) for a in wiki.articles]
    entries += [(name, page_url(name), True) for a in wiki.articles for name, _ in a.redirects]
    entries.sort(key=lambda e: sort_key(e[0]))
    redirect_cls = ' class="allpages-redirect"'
    items = "".join(f'<li{redirect_cls if red else ""}><a href="{u}">{esc(t)}</a></li>'
                    for t, u, red in entries)
    content = ('<div class="body allpages-wrap">'
               f"<p>{len(wiki.articles)} Artikel und {len(entries) - len(wiki.articles)} Weiterleitungen. "
               "Weiterleitungen sind <i>kursiv</i> dargestellt.</p>"
               '<p><label><input type="checkbox" id="hide-redirects"> Weiterleitungen ausblenden</label></p>'
               f'<ul class="allpages">{items}</ul></div>')
    return layout("Alle Seiten", content, path="/wiki/Spezial:Alle_Seiten", tab="Spezialseite")


def special_pages(wiki):
    search = ('<div class="body"><form class="search-page" action="/wiki/Spezial:Suche" role="search">'
              '<input type="search" name="search" aria-label="Suchbegriff">'
              '<input type="hidden" name="fulltext" value="1"><button type="submit">Suchen</button></form>'
              '<div id="search-results" aria-live="polite"></div>'
              '<noscript><p>Die Suche benötigt JavaScript. Alle Artikel stehen unter '
              '<a href="/wiki/Spezial:Alle_Seiten">Alle Seiten</a>.</p></noscript></div>')
    write("wiki/Spezial:Suche.html",
          layout("Suche", search, path="/wiki/Spezial:Suche", tab="Spezialseite", special="suche", noindex=True))
    random_page = ('<div class="body"><p>Ein zufälliger Artikel wird geladen …</p>'
                   '<noscript><p>Dafür wird JavaScript benötigt. Alle Artikel stehen unter '
                   '<a href="/wiki/Spezial:Alle_Seiten">Alle Seiten</a>.</p></noscript></div>')
    write("wiki/Spezial:Zufällige_Seite.html",
          layout("Zufälliger Artikel", random_page, path="/wiki/Spezial:Zuf%C3%A4llige_Seite",
                 tab="Spezialseite", special="zufall", noindex=True))
    write("wiki/Spezial:Alle_Seiten.html", all_pages(wiki))
    not_found = ('<div class="body"><p id="nf-message">Diese Seite existiert nicht.</p>'
                 '<div id="nf-extra"></div><p><a href="/">Zur Hauptseite</a></p></div>')
    write("404.html", layout("Seite nicht gefunden", not_found, path="/404", tab="Spezialseite",
                             special="404", noindex=True))
    home = ('<script>location.replace("/")</script>\n'
            '<noscript><meta http-equiv="refresh" content="0; url=/"></noscript>\n')
    write("wiki/Hauptseite.html", layout("Hauptseite", '<div class="body"><p><a href="/">Zur Hauptseite</a></p></div>',
                                         path="/wiki/Hauptseite", head=home, noindex=True))


def main():
    wiki = Wiki()
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT / "static")
    shutil.copy(ROOT / "CNAME", OUT / "CNAME")

    rendered, search_pages = {}, []
    for a in wiki.articles:
        r = Renderer(wiki, a)
        body = r.blocks(a.source)
        rendered[a] = body
        a.headings = r.headings
        a.infobox_html = r.infobox(a.title, a.infobox)
        a.navbox_html = "".join(r.navbox(wiki.navboxes[k]) for k in a.navboxes)
        a.description = "Begriffsklärung" if a.disambig else description_of(body)
        search_pages.append({"t": a.title, "u": a.url, "d": a.description,
                             "x": plain(body + " " + a.infobox_html)})

    for a in wiki.articles:
        content = f'<div class="body">{a.infobox_html}{rendered[a]}</div>'
        if a.disambig:
            content += ('<div class="disambig-note">Dies ist eine Begriffsklärungsseite zur Unterscheidung '
                        'mehrerer mit demselben Wort bezeichneter Begriffe.</div>')
        content += a.navbox_html
        write(f"wiki/{slug(a.title)}.html",
              layout(a.title, content, path=a.url, description=a.description, toc=toc_html(a.headings),
                     source=a.path, modified=last_modified(a.path)))
        for name, anchor in a.redirects:
            write(f"wiki/{slug(name)}.html", redirect_page(name, a, anchor))

    write("index.html", main_page(wiki, rendered))
    special_pages(wiki)

    redirects = [{"t": name, "u": page_url(name), "to": a.title}
                 for a in wiki.articles for name, _ in a.redirects]
    write("search-index.json", json.dumps({"pages": search_pages, "redirects": redirects},
                                          ensure_ascii=False, separators=(",", ":")))
    urls = ["/"] + [a.url for a in wiki.articles]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{BASE_URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n")

    print(f"{len(wiki.articles)} Artikel, {len(redirects)} Weiterleitungen -> {OUT.relative_to(ROOT)}/")
    if wiki.red_links:
        print("Rote Links (Seite existiert nicht):", ", ".join(sorted(wiki.red_links, key=sort_key)))


if __name__ == "__main__":
    main()
