+++
redirects = [
  "Query (GraphQL)|Abfragen",
  "Mutation|Queries und Mutations",
  "SmallRye GraphQL|GraphQL in Quarkus",
  "@GraphQLApi|GraphQL in Quarkus",
  "GraphQL-UI|GraphQL in Quarkus",
]
navbox = ["maschinen"]

[infobox]
Art = "Abfragesprache für APIs"
Endpoints = "eine einzige Endpoint-URL"
Typisierung = "stark typisiert"
"Weiterentwicklung von" = "[[REST]]"
+++
**GraphQL** ist eine Weiterentwicklung von [[REST]] und besitzt eine starke Ähnlichkeit dazu. GraphQL ist eine Abfragesprache für APIs.

## Eigenschaften

- flexible Abfragen
- nur eine einzige Endpoint-URL
- gut geeignet für komplexe Datenstrukturen
- weniger Overhead als REST
- stark typisiert

## Abfragen

Der Client schreibt selbst, welche Felder er haben will, auch verschachtelt. Die Antwort hat genau diese Form und steht unter `data`:

```graphql
{
  author(id: 1) {
    name
    books { title price }
  }
}
```

Alle Abfragen gehen per POST an **eine** URL (z. B. `/graphql`). Gibt es ein Objekt nicht, ist das Ergebnis `null` statt eines 404.

## Queries und Mutations

; Query
: lesen
; Mutation
: ändern (anlegen, löschen …)

Eine **lesende** Schnittstelle hat nur Queries.

## GraphQL in Quarkus

Mit der Erweiterung SmallRye GraphQL wird das Schema aus den Java-Klassen erzeugt (code-first):

| Annotation | Bedeutung |
|---|---|
| `@GraphQLApi` | Klasse mit GraphQL-Operationen (im Package `boundary`) |
| `@Query("authors")` | Methode ist eine Query mit diesem Namen |
| `@Name("id")` | Name eines Arguments |
| `@Type("Author")` | Name des GraphQL-Typs für eine Klasse bzw. einen Record |

- Rückgabewerte sind verschachtelte [[DTO|DTOs]], damit der Client tief abfragen kann.
- Ein optionales Argument (z. B. `Boolean` statt `boolean`) ist `null`, wenn es fehlt; dann gibt man z. B. alle Einträge zurück.
- Auch hier: Filtern in der Abfrage, mit den Methoden der [[Panache|Repositories]].
- Ausprobieren in der GraphQL-UI unter `/q/graphql-ui`.
