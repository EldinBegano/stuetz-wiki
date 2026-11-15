+++
redirects = [
  "Jakarta Persistence Query Language",
  "Java Persistence Query Language",
  "HQL",
  "TypedQuery|Typisierte Abfragen",
  "Typisierte Abfrage|Typisierte Abfragen",
  "Named Query|Named Queries",
  "NamedQuery|Named Queries",
  "@NamedQuery|Named Queries",
  "Konstruktor-Ausdruck|DTO-Projektion",
  "DTO-Projektion|DTO-Projektion",
  "Native Query|Native SQL-Abfragen",
  "Native SQL|Native SQL-Abfragen",
  "Native Abfrage|Native SQL-Abfragen",
  "coalesce|Aggregation",
  "GROUP BY|Aggregation",
  "HAVING|Aggregation",
  "LEFT JOIN|Joins",
]
navbox = ["datenbanken"]

[infobox]
Langform = "Jakarta Persistence Query Language"
"Teil von" = "[[JPA]]"
"Arbeitet auf" = "Entity-Klassen und Attributen"
"Ähnlich wie" = "[[SQL]]"
+++
**JPQL** (*Jakarta Persistence Query Language*) ist die Abfragesprache von [[JPA]]. Sie sieht aus wie [[SQL]], arbeitet aber auf **Entity-Klassen und deren Attributen**, nicht auf Tabellen und Spalten. Hibernate erweitert JPQL zu **HQL**.

| | JPQL | SQL |
|---|---|---|
| ! Abfrage auf | Entity `CargoItem` | Tabelle `CARGO_ITEMS` |
| ! Felder | `i.weightKg` | `weight_kg` |
| ! Beziehungen | Navigation mit Punkt: `i.container.voyage.id` | Join über Fremdschlüssel |

## Rechnen in der Abfrage

Filtern, Gruppieren und Summieren gehört **in die Abfrage** (`where`, `group by`, `sum`), nicht in Java. Lädt man alle Zeilen (`listAll()`) und filtert dann mit einer Schleife oder einem Stream, werden unnötig viele Entities aus der Datenbank geladen. In Tests kann man das mit den [[Testen#Geladene Entities zählen|Hibernate-Statistiken]] prüfen.

## Typisierte Abfragen

Eine **typisierte Abfrage** (`TypedQuery<T>`) bekommt den Ergebnistyp mit, dadurch braucht man keinen Cast:

```java
TypedQuery<Double> q = em.createQuery(
        "select sum(b.price) from Book b where b.author.id = :authorId", Double.class);
q.setParameter("authorId", authorId);
Double total = q.getSingleResult();
```

- Parameter mit Namen (`:authorId`) oder Position (`?1`), gesetzt mit `setParameter`
- `getSingleResult()` für genau ein Ergebnis, `getResultList()` für eine Liste
- Parameter nie mit String-Verkettung einbauen (SQL-Injection)

## Named Queries

Eine **Named Query** wird mit `@NamedQuery(name = …, query = …)` direkt über der [[Entität]] definiert (mehrere mit `@NamedQueries`) und über den Namen aufgerufen:

```java
em.createNamedQuery("Book.byAuthor", Book.class)
  .setParameter("authorId", authorId)
  .getResultList();
```

Vorteil: Die Abfrage steht bei der Entity und wird schon beim Start der Anwendung geprüft, nicht erst beim Aufruf.

## DTO-Projektion

Mit einem **Konstruktor-Ausdruck** (`select new …`) erzeugt die Abfrage direkt [[DTO|DTOs]] statt Entities:

```sql
select new at.htl.shop.dto.AuthorRevenueDto(b.author.name, sum(b.price))
from Book b
group by b.author.name
order by sum(b.price) desc
```

- Der Klassenname muss **voll qualifiziert** sein (mit Package).
- Der DTO braucht einen Konstruktor mit genau diesen Parametertypen (ein Java-Record passt).
- Es werden keine Entities geladen, nur die gewählten Werte.

## Aggregation

- `sum`, `count`, `avg`, `min`, `max` fassen Zeilen zusammen.
- `group by` bildet Gruppen, `having` filtert die Gruppen (in `where` sind Aggregatfunktionen nicht erlaubt).
- `sum` über keine Zeilen liefert `null`, nicht `0`. Mit `coalesce(sum(x), 0)` bekommt man `0`.

## Joins

- `join` (inner join): nur Zeilen mit Partner
- `left join`: auch Zeilen **ohne** Partner, z. B. leere Container ohne Ladungsposten. Deren Summe ist `null`, also mit `coalesce` arbeiten.

Beispiel: alle Container mit mindestens `minFree` freier Kapazität, leere eingeschlossen:

```sql
select c from Container c left join c.cargoItems i
where c.voyage.id = :voyageId
group by c
having c.capacityKg - coalesce(sum(i.weightKg), 0) >= :minFree
order by c.containerNumber
```

## Native SQL-Abfragen

Mit `em.createNativeQuery(sql)` schreibt man **echtes SQL** mit Tabellen- und Spaltennamen. Das braucht man für datenbankspezifische Funktionen oder wenn JPQL nicht reicht.

- Das Ergebnis sind keine Entities, sondern einzelne Werte bzw. `Object[]` pro Zeile, die man selbst in einen [[DTO]] umwandelt.
- Zahlentypen hängen von der Datenbank ab (z. B. `Long` oder `BigInteger`), deshalb sicher über `((Number) wert).longValue()` umwandeln.
- Zählen mit Bedingung geht z. B. mit `count(distinct case when … then c.id end)`.
