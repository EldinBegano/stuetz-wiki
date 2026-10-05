/* stuetz.wiki – Darstellung, Menü, Weiterleitungen, Inhaltsverzeichnis, Suche */
(() => {
  "use strict";

  const root = document.documentElement;
  const body = document.body;
  const params = new URLSearchParams(location.search);

  // ---------- Darstellung (hell/dunkel) ----------
  let savedTheme = null;
  try { savedTheme = localStorage.getItem("theme"); } catch (e) { /* kein Speicher */ }
  for (const radio of document.querySelectorAll('input[name="theme"]')) {
    radio.checked = radio.value === (savedTheme || "auto");
    radio.addEventListener("change", () => {
      if (radio.value === "auto") delete root.dataset.theme;
      else root.dataset.theme = radio.value;
      try {
        if (radio.value === "auto") localStorage.removeItem("theme");
        else localStorage.setItem("theme", radio.value);
      } catch (e) { /* kein Speicher */ }
    });
  }

  // ---------- Hauptmenü (mobil) ----------
  const menuButton = document.querySelector(".menu-toggle");
  const setMenu = (open) => {
    body.classList.toggle("menu-open", open);
    menuButton?.setAttribute("aria-expanded", String(open));
  };
  menuButton?.addEventListener("click", () => setMenu(!body.classList.contains("menu-open")));
  document.querySelector(".sidebar-backdrop")?.addEventListener("click", () => setMenu(false));
  document.querySelector(".sidebar")?.addEventListener("click", (e) => {
    if (e.target.closest("a")) setMenu(false);
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setMenu(false);
  });

  // ---------- „Weitergeleitet von …“ ----------
  const redirectedFrom = params.get("rdfrom");
  const contentSub = document.getElementById("contentSub");
  if (redirectedFrom && contentSub) {
    const a = document.createElement("a");
    a.href = "/wiki/" + encodeURIComponent(redirectedFrom.replace(/ /g, "_")) + "?redirect=no";
    a.textContent = redirectedFrom;
    contentSub.replaceChildren("(Weitergeleitet von ", a, ")");
    params.delete("rdfrom");
    const rest = params.toString();
    history.replaceState(null, "", location.pathname + (rest ? "?" + rest : "") + location.hash);
  }

  // ---------- Inhaltsverzeichnis: aktuellen Abschnitt markieren ----------
  const tocLinks = [...document.querySelectorAll(".toc a")];
  const sections = tocLinks
    .map((a) => [document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1))), a])
    .filter(([el]) => el);
  if (sections.length) {
    const topLink = tocLinks.find((a) => a.getAttribute("href") === "#");
    let ticking = false;
    const update = () => {
      ticking = false;
      let current = topLink;
      for (const [el, a] of sections) {
        if (el.getBoundingClientRect().top < 120) current = a;
        else break;
      }
      for (const a of tocLinks) a.classList.toggle("active", a === current);
    };
    addEventListener("scroll", () => {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  // ---------- Suchindex ----------
  const fold = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase()
    .replace(/_/g, " ").replace(/\s+/g, " ").trim();

  let indexPromise = null;
  const loadIndex = () => {
    if (!indexPromise) {
      indexPromise = fetch("/search-index.json")
        .then((r) => {
          if (!r.ok) throw new Error("Suchindex: HTTP " + r.status);
          return r.json();
        })
        .then((data) => {
          const byTitle = new Map(data.pages.map((p) => [p.t, p]));
          for (const p of data.pages) p.redirects = [];
          for (const r of data.redirects) byTitle.get(r.to)?.redirects.push(r.t);
          for (const p of data.pages) p.hay = fold([p.t, ...p.redirects, p.x].join(" "));
          const entries = data.pages.map((p) => ({ title: p.t, url: p.u, page: p, key: fold(p.t) }))
            .concat(data.redirects.map((r) => ({
              title: r.t, url: r.u, page: byTitle.get(r.to), redirect: true, key: fold(r.t),
            })));
          return { pages: data.pages, entries };
        });
      indexPromise.catch(() => { indexPromise = null; });
    }
    return indexPromise;
  };

  const findExact = (index, q) => {
    const k = fold(q);
    return index.entries.find((e) => e.key === k);
  };

  const suggest = (index, q, limit = 8) => {
    const k = fold(q);
    if (!k) return [];
    const scored = [];
    for (const e of index.entries) {
      let s;
      if (e.key === k) s = 0;
      else if (e.key.startsWith(k)) s = 1;
      else if (e.key.split(/[\s\-(]+/).some((w) => w.startsWith(k))) s = 2;
      else if (e.key.includes(k)) s = 3;
      else continue;
      scored.push({ e, s: s + (e.redirect ? 0.5 : 0) });
    }
    scored.sort((a, b) => a.s - b.s || a.e.title.length - b.e.title.length
      || a.e.title.localeCompare(b.e.title, "de"));
    const seen = new Set();
    const out = [];
    for (const { e } of scored) {
      if (seen.has(e.page)) continue;
      seen.add(e.page);
      out.push(e);
      if (out.length === limit) break;
    }
    return out;
  };

  const searchUrl = (q, fulltext) =>
    "/wiki/Spezial:Suche?search=" + encodeURIComponent(q) + (fulltext ? "&fulltext=1" : "");

  // ---------- Suchfeld mit Vorschlägen ----------
  for (const form of document.querySelectorAll("form.search")) {
    const input = form.querySelector('input[name="search"]');
    const list = form.querySelector(".suggestions");
    let active = -1;

    const close = () => {
      list.hidden = true;
      active = -1;
      input.setAttribute("aria-expanded", "false");
      input.removeAttribute("aria-activedescendant");
    };

    const select = (i) => {
      active = i;
      [...list.children].forEach((li, j) => li.setAttribute("aria-selected", String(j === i)));
      if (i >= 0) input.setAttribute("aria-activedescendant", list.children[i].id);
      else input.removeAttribute("aria-activedescendant");
    };

    const item = (href, title, desc, cls) => {
      const li = document.createElement("li");
      li.id = "suggestion-" + list.children.length;
      li.setAttribute("role", "option");
      if (cls) li.className = cls;
      const a = document.createElement("a");
      a.href = href;
      a.tabIndex = -1;
      const t = document.createElement("span");
      t.className = "s-title";
      t.textContent = title;
      a.append(t);
      if (desc) {
        const d = document.createElement("span");
        d.className = "s-desc";
        d.textContent = desc;
        a.append(d);
      }
      li.append(a);
      return li;
    };

    const render = (q, results) => {
      list.replaceChildren();
      if (!q.trim()) return close();
      for (const e of results) list.append(item(e.url, e.title, e.page ? e.page.d : "", ""));
      list.append(item(searchUrl(q.trim(), true), "Suche nach Seiten, die „" + q.trim() + "“ enthalten", "", "s-fulltext"));
      list.hidden = false;
      input.setAttribute("aria-expanded", "true");
      select(-1);
    };

    input.addEventListener("focus", () => { loadIndex().catch(() => {}); });
    input.addEventListener("input", async () => {
      const q = input.value;
      let results = [];
      try {
        const index = await loadIndex();
        if (input.value !== q) return;
        results = suggest(index, q);
      } catch (e) { /* ohne Index nur Volltextsuche anbieten */ }
      render(q, results);
    });
    input.addEventListener("keydown", (e) => {
      if (list.hidden) return;
      const n = list.children.length;
      if (e.key === "ArrowDown") { e.preventDefault(); select((active + 1) % n); }
      else if (e.key === "ArrowUp") { e.preventDefault(); select(active <= 0 ? n - 1 : active - 1); }
      else if (e.key === "Escape") close();
      else if (e.key === "Enter" && active >= 0) {
        e.preventDefault();
        location.href = list.children[active].querySelector("a").href;
      }
    });
    input.addEventListener("blur", () => setTimeout(close, 150));
    list.addEventListener("mousedown", (e) => e.preventDefault());

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const q = input.value.trim();
      if (!q) return;
      try {
        const hit = findExact(await loadIndex(), q);
        location.href = hit ? hit.url : searchUrl(q, true);
      } catch (err) {
        location.href = searchUrl(q, false);
      }
    });
  }

  // ---------- Spezialseiten ----------
  const snippet = (text, terms) => {
    const hay = fold(text);
    let pos = -1;
    for (const t of terms) {
      const i = hay.indexOf(t);
      if (i >= 0 && (pos < 0 || i < pos)) pos = i;
    }
    let start = Math.max(0, pos - 70);
    if (start > 0) {
      const sp = text.indexOf(" ", start);
      if (sp >= 0 && sp < pos) start = sp + 1;
    }
    let end = Math.min(text.length, start + 220);
    if (end < text.length) {
      const sp = text.lastIndexOf(" ", end);
      if (sp > pos) end = sp;
    }
    const part = text.slice(start, end);
    const partHay = hay.slice(start, end);
    const ranges = [];
    for (const t of terms) {
      for (let i = partHay.indexOf(t); i >= 0; i = partHay.indexOf(t, i + t.length)) ranges.push([i, i + t.length]);
    }
    ranges.sort((a, b) => a[0] - b[0]);
    const frag = document.createDocumentFragment();
    if (start > 0) frag.append("… ");
    let cur = 0;
    for (const [a, b] of ranges) {
      if (a < cur) continue;
      frag.append(part.slice(cur, a));
      const m = document.createElement("mark");
      m.textContent = part.slice(a, b);
      frag.append(m);
      cur = b;
    }
    frag.append(part.slice(cur));
    if (end < text.length) frag.append(" …");
    return frag;
  };

  const runSearchPage = async () => {
    const q = (params.get("search") || "").trim();
    const out = document.getElementById("search-results");
    const field = document.querySelector('.search-page input[name="search"]');
    if (field) field.value = q;
    if (!q || !out) return;
    document.title = q + " – Suchergebnisse – stuetz.wiki";
    let index;
    try {
      index = await loadIndex();
    } catch (e) {
      out.textContent = "Der Suchindex konnte nicht geladen werden.";
      return;
    }
    if (!params.has("fulltext")) {
      const hit = findExact(index, q);
      if (hit) { location.replace(hit.url); return; }
    }
    const terms = fold(q).split(" ").filter(Boolean);
    const results = [];
    for (const p of index.pages) {
      if (!terms.every((t) => p.hay.includes(t))) continue;
      const titleKey = fold(p.t);
      let score = 0;
      for (const t of terms) {
        if (titleKey.includes(t)) score += 20;
        score += p.hay.split(t).length - 1;
      }
      const via = terms.some((t) => titleKey.includes(t)) ? null
        : p.redirects.find((r) => terms.every((t) => fold(r).includes(t)));
      results.push({ p, score, via });
    }
    results.sort((a, b) => b.score - a.score || a.p.t.localeCompare(b.p.t, "de"));

    const info = document.createElement("p");
    info.className = "search-info";
    info.textContent = results.length
      ? results.length + (results.length === 1 ? " Ergebnis" : " Ergebnisse") + " für „" + q + "“"
      : "Es wurden keine mit der Anfrage „" + q + "“ übereinstimmenden Ergebnisse gefunden.";
    const ul = document.createElement("ul");
    ul.className = "search-results";
    for (const { p, via } of results) {
      const li = document.createElement("li");
      const head = document.createElement("div");
      head.className = "sr-heading";
      const a = document.createElement("a");
      a.href = p.u;
      a.textContent = p.t;
      head.append(a);
      if (via) {
        const r = document.createElement("span");
        r.className = "sr-redirect";
        r.textContent = " (Weiterleitung von „" + via + "“)";
        head.append(r);
      }
      const snip = document.createElement("div");
      snip.className = "sr-snippet";
      snip.append(snippet(p.x, terms));
      const meta = document.createElement("div");
      meta.className = "sr-meta";
      const words = p.x.split(/\s+/).filter(Boolean).length;
      meta.textContent = words + (words === 1 ? " Wort" : " Wörter");
      li.append(head, snip, meta);
      ul.append(li);
    }
    out.replaceChildren(info, ul);
  };

  const runRandom = async () => {
    try {
      const { pages } = await loadIndex();
      location.replace(pages[Math.floor(Math.random() * pages.length)].u);
    } catch (e) {
      location.replace("/wiki/Spezial:Alle_Seiten");
    }
  };

  const safeDecode = (s) => {
    try { return decodeURIComponent(s); } catch (e) { return s; }
  };

  const runNotFound = async () => {
    const path = safeDecode(location.pathname);
    if (!path.startsWith("/wiki/")) return;
    const name = path.slice(6).replace(/_/g, " ").trim();
    if (!name) return;
    let index = null;
    try { index = await loadIndex(); } catch (e) { /* ohne Index keine Vorschläge */ }
    const hit = index && findExact(index, name);
    if (hit && safeDecode(new URL(hit.url, location.origin).pathname) !== path) {
      location.replace(hit.url + location.search + location.hash);
      return;
    }
    document.title = name + " – stuetz.wiki";
    document.getElementById("firstHeading").textContent = name;
    document.getElementById("nf-message").textContent = "Der Artikel „" + name + "“ existiert in stuetz.wiki nicht.";
    const extra = document.getElementById("nf-extra");
    const searchLink = document.createElement("a");
    searchLink.href = searchUrl(name, true);
    searchLink.textContent = "Nach „" + name + "“ suchen";
    const p = document.createElement("p");
    p.append(searchLink);
    extra.append(p);
    const similar = index ? suggest(index, name.split(" ")[0], 5) : [];
    if (similar.length) {
      const h = document.createElement("p");
      h.textContent = "Ähnliche Seiten:";
      const ul = document.createElement("ul");
      for (const e of similar) {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = e.url;
        a.textContent = e.title;
        li.append(a);
        ul.append(li);
      }
      extra.append(h, ul);
    }
  };

  const special = body.dataset.special;
  if (special === "suche") runSearchPage();
  else if (special === "zufall") runRandom();
  else if (special === "404") runNotFound();
})();
