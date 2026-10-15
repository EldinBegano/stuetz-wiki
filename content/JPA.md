+++
redirects = [
  "Java Persistence API",
  "Jakarta Persistence",
  "EntityManager|EntityManager",
  "Entity-Manager|EntityManager",
  "Entity-Lebenszyklus|Lebenszyklus",
  "Entity-Lifecycle|Lebenszyklus",
  "Managed|Status",
  "Detached|Status",
  "Removed|Status",
  "Callback|Callbacks",
  "Callbacks|Callbacks",
  "Hook|Callbacks",
  "Primärschlüsselstrategie|Primärschlüsselstrategien",
  "Primärschlüsselstrategien|Primärschlüsselstrategien",
  "Primary-Key-Strategien|Primärschlüsselstrategien",
  "Eager Loading|Eager und Lazy Loading",
  "Lazy Loading|Eager und Lazy Loading",
]
navbox = ["datenbanken"]

[infobox]
Langform = "Java Persistence API"
Art = "[[Datenbankzugriff#OR-Mapper|OR-Mapper]]"
Verwendet = "[[Datenbankzugriff#JDBC|JDBC]]"
+++
**JPA** (*Java Persistence API*) ist ein [[Datenbankzugriff#OR-Mapper|OR-Mapper]] für Java. Jedem Objekt wird eine Zeile in der Datenbank zugesprochen.

## Entity-Objekte

Gespeichert werden [[Entität|Entity-Objekte]]. Ein Entity-Objekt ist ein Business-Objekt wie Person, Rechnung oder Bestellung – nichts Technisches wie ein Iterator.

## EntityManager

Warum ein EntityManager? Wegen des Caches: Wenn man mehrere hat, gibt es Probleme. Deswegen ist der EntityManager Singleton bzw. `@ApplicationScoped`.

## Lebenszyklus

[[Datei:JPA_Lebenszyklus.svg|mini|Lebenszyklus eines Entity-Objekts: Neu (transient), Managed, Removed und Detached]]

Ein Objekt wird mit `new` oder über [[Context und Dependency Injection|CDI]] erstellt und über den `EntityManager` persistiert.

| Status | Aufruf | neuer Status |
|---|---|---|
| ! – | `new` oder [[CDI]] | Neu ([[Transient|transient]]) |
| ! Neu (transient) | `persist` | Managed |
| ! Managed | `rollback` | Neu (transient) |
| ! Managed | `remove` | Removed (aus der Datenbank gelöscht) |
| ! Managed | `refresh` | Managed (Werte werden aktualisiert) |
| ! Managed | `detach` | Detached |
| ! Removed | `rollback` | Detached |
| ! Removed | `persist` | Managed |
| ! Detached | `merge` | Managed |

### Status

; Neu (transient)
: flüchtig
; Managed
: Java hat eine direkte Verbindung mit der DB-Zeile, z. B. funktioniert `setName`.
; Detached
: Man kann das Objekt noch updaten, es wird aber nicht mehr mit der Datenbank geupdatet.
; Removed
: Die Zeile wird aus der Datenbank entfernt.

Kann ein Objekt nicht direkt adressiert werden, schaut `merge` nach, ob es in der Datenbank vorhanden ist: Wenn nicht, ist es neu, sonst detached.

## Callbacks

Ein Callback ist eine Annotation über einer Methode, die dann ausgeführt wird (z. B. `@PrePersist`). Andere Wörter dafür sind Hook und Trigger: Wenn etwas eintritt, tritt ein bestimmtes Event auf.

## Primärschlüsselstrategien

In der objektorientierten Programmierung gibt es die Objekt-Identität (Speicherort, Hash). In der Datenbank lösen Primärschlüsselstrategien das Problem, dass Objekte eine eindeutige Nummer bekommen müssen.

Strategien:

- Table (`TABLE`): eine eigene Tabelle (siehe Beispiel)
- Sequenz (`SEQUENCE`)
- ID (`IDENTITY`)
- UUID (`UUID`): von der Performance etwas schlechter
- Auto (`AUTO`): schaut selbst, was verwendet wird

Beispiel für die eigene Tabelle bei der Strategie Table:

| Pkey | Pid |
|---|---|
| ! Person | 1 |
| ! Invoice | 1000 |
| ! Telephone | 10000 |

## Eager und Lazy Loading

; Eager Loading
: Entities werden direkt geladen.
; Lazy Loading
: Entities werden erst geladen, wenn die Daten gefordert sind.
