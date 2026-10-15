+++
redirects = [
  "KI-Agenten",
  "Agent",
  "Harness|Harness und Graph",
  "Graph (KI)|Harness und Graph",
  "CLAUDE.md|Context",
  "AGENTS.md|Context",
  "Memory|Memory",
  "Träumen|Träumen",
  "Dream|Träumen",
  "Continuation|Continuations",
  "Runbook|Continuations",
  "Sub-Agent|src",
  "Procedurales|Procedurales",
  "Skill|Skills", "Skills|Skills",
  "Command|Commands", "Commands|Commands",
  "Rule|Rules", "Rules|Rules",
  "MCP|Tools/MCP", "Tools|Tools/MCP",
  "Tmux|Tmux-Session", "Tmux-Session|Tmux-Session",
  "Yolo-Mode|Yolo-Mode",
  "Ralph|Ralph",
  "Git-Worktree|Git-Worktree",
  "Superbox|Setup",
  "Devbox|Setup",
]
navbox = ["ki"]
+++
Zu einem **KI-Agenten** gehören Begriffe wie [[#Skills|Skills]], [[#Memory|Memorys]], [[#Rules|Rules]] und [[#Commands|Commands]].

## Harness und Graph

Prompten → Harness → Graph

; Harness
: besserer Kontext, Software-Framework
; Graph
: mehrere Agenten steuern wie eine Firma

## Wissen

Das Wissen eines Agenten in Ebenen:

1. Context (mit `CLAUDE.md`)
2. Memory
3. `openspec/`

Den Quellcode (`src/`) liest der Agent nicht selbst (siehe [[#src|src]]).

### Context

- ein Startfile (`CLAUDE.md`, `AGENTS.md`)
- präzise, aber scharf
- Umgebungs-Rundumwissen
- neuer Begriff: [[#Harness und Graph|Harness]]

Mehr unter [[Context (KI)]].

### Memory

- lebt im Home-Verzeichnis (`.claude`)
- für jedes Git-Checkout-Verzeichnis ein eigenes File
- vor dem Beenden fragen, ob er alles niedergeschrieben hat

### Träumen

Beim Träumen wird das Memory reorganisiert: Ohne Interaktion mit dem Menschen schaut die KI alle Files an, ob sich Sachen widersprechen oder doppelt vorkommen.

### Continuations

Ein Runbook verwenden, wenn man öfters Continuation-Prompts machen will, damit dabei steht, bei welchem Task er ist.

### Repo

Nicht selber committen, sondern es dem Agent sagen, damit er die Git-Commit-History später wieder lesen kann.

### src

Den Quellcode von einem Sub-Agent lesen lassen, der ihn zusammenfasst.

## Procedurales

; Skills
: bestehen aus einer Zusammenfassung mit Reizwörtern und einer genauen Definition, was er macht, falls ein Reizwort im Prompt vorkommt
; Commands
: Anweisungen, was er tun soll, z. B. `/dream` oder `/deploy`
; Rules
: z. B. wenn er ein File nicht ändern darf
; Tools/MCP
: Aufgaben, die viele [[Tokens]] brauchen, werden ausgelagert; zurückgeliefert wird nur, ob es erfolgreich war

Ein Skill oder Command sollte sich nicht mit existierenden Namen überschneiden. Für Rules, Skills usw. kann man ein eigenes Repo anlegen (siehe [[Git-Submodul]]).

## Arbeitsweise

; Tmux-Session
: Die Session wird erhalten; man kann sie später erneut aufrufen und fortfahren.
; Yolo-Mode
: Der Agent hat Root-Rechte.
; Ralph
: Für jede Teilaufgabe eine eigene Claude-Session. Falls die Tokens auslaufen, wartet er, bis wieder Tokens verfügbar sind, und macht dann weiter.
; Git-Worktree
: Das Git-Repo weiß, dass es zwei Checkouts gab.

## Setup

[[Datei:KI-Agent_Setup.svg|mini|Vom Laptop geht der Prompt an die Superbox (Opus) in der Cloud, die mit der Devbox zusammenarbeitet. Auf beiden läuft Claude in einer Tmux-Session.]]

Vom Laptop geht der Prompt an die Superbox (Opus) in der Cloud, die mit der Devbox zusammenarbeitet. Auf Superbox und Devbox läuft Claude jeweils in einer [[#Tmux-Session|Tmux-Session]], die man vom Laptop aus öffnet.
