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
  "Hibernate",
  "Hibernate ORM",
  "@Entity|Mapping",
  "@Table|Mapping",
  "@Column|Mapping",
  "@OneToMany|Beziehungen",
  "@ManyToOne|Beziehungen",
  "@JoinColumn|Beziehungen",
  "mappedBy|Beziehungen",
  "Bidirektional|Beziehungen",
  "@Transactional|Transaktionen",
  "Transaktion|Transaktionen",
]
navbox = ["datenbanken"]

[infobox]
Langform = "Java Persistence API"
Art = "[[Datenbankzugriff#OR-Mapper|OR-Mapper]]"
Verwendet = "[[Datenbankzugriff#JDBC|JDBC]]"
Implementierung = "Hibernate ORM"
Abfragesprache = "[[JPQL]]"
+++
**JPA** (*Java Persistence API*) ist ein [[Datenbankzugriff#OR-Mapper|OR-Mapper]] für Java. Jedem Objekt wird eine Zeile in der Datenbank zugesprochen. In [[Quarkus]] ist **Hibernate ORM** die Implementierung, vereinfacht mit [[Panache]]; abgefragt wird mit [[JPQL]].

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

## Mapping

Mit [[Annotation (Java)|Annotationen]] legt man fest, wie eine Klasse auf eine Tabelle abgebildet wird:

| Annotation | Bedeutung |
|---|---|
| `@Entity` | Klasse ist eine [[Entität]] |
| `@Table(name = "BOOKS")` | Tabellenname, falls er anders als der Klassenname ist |
| `@Id`, `@GeneratedValue(strategy = IDENTITY)` | Primärschlüssel, siehe [[#Primärschlüsselstrategien|Primärschlüsselstrategien]] |
| `@Column(name = "…", nullable = false, unique = true)` | Spaltenname und Constraints (siehe [[Integrität]]) |

Im Code sind die Namen camelCase (`weightKg`), in der Datenbank meist snake_case (`weight_kg`).

## Beziehungen

| Annotation | Bedeutung |
|---|---|
| `@ManyToOne` | viele Objekte gehören zu einem (z. B. viele Container zu einer Reise); diese Seite hat den Fremdschlüssel, Spaltenname mit `@JoinColumn` |
| `@OneToMany(mappedBy = "…")` | die Gegenseite als Liste; `mappedBy` nennt das Feld auf der `@ManyToOne`-Seite |
| `@OrderBy("…")` | Sortierung der Liste |

Gibt es beide Seiten, ist die Beziehung **bidirektional**: Man kommt von der Reise zu ihren Containern und vom Container zu seiner Reise. Gespeichert wird die Beziehung nur über die Seite mit dem Fremdschlüssel (`@ManyToOne`).

Bidirektionale Beziehungen erzeugen beim Umwandeln in JSON eine Endlosschleife. Deshalb gibt man Entities nicht direkt nach außen, sondern [[DTO|DTOs]] (oder blendet eine Seite mit `@JsonIgnore` aus).

Getter ohne Feld (z. B. `getLoadedKg()`, das die Gewichte der Liste summiert) sind **berechnete Werte**, keine Spalten.

## Transaktionen

Schreibende Zugriffe (`persist`, `remove`, Änderungen) brauchen eine Transaktion. In [[Quarkus]] schreibt man `@Transactional` über die Methode.

- Läuft die Methode durch: `commit`, alles wird gespeichert.
- Wirft sie eine (Runtime-)Exception: `rollback`, **nichts** wird gespeichert (siehe [[SQL#TCL|TCL]]).

So kann eine Service-Methode zuerst alle Regeln prüfen und bei einem Fehler einfach eine Exception werfen.

## Schema und Testdaten

Hibernate kann die Tabellen aus den Entities erzeugen (`drop-and-create`) und danach ein SQL-Skript wie `import.sql` mit Testdaten einspielen (siehe [[Quarkus#Konfiguration|Konfiguration]]).
