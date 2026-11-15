+++
redirects = [
  "Data Transfer Object",
  "DTOs",
  "Record (Java)|Records",
  "Java Record|Records",
  "Records|Records",
  "DtoMapper|Mapper",
  "Mapper|Mapper",
  "Bean Validation|Validierung",
  "Validierung|Validierung",
  "@NotNull|Validierung",
  "@NotBlank|Validierung",
  "@Valid|Validierung",
]
navbox = ["backend"]

[infobox]
Langform = "Data Transfer Object"
"In Java meist" = "Record"
+++
Ein **DTO** (*Data Transfer Object*) ist ein einfaches Objekt, das nur Daten für die Übertragung enthält, z. B. die JSON-Antwort einer [[REST]]-Schnittstelle. Es hat keine Logik und ist keine [[Entität]].

## Warum DTOs?

Grundregel: **Entities verlassen nie das Backend.** Nach außen gehen nur DTOs.

- Bidirektionale [[JPA#Beziehungen|Beziehungen]] führen beim Umwandeln in JSON zu einer Endlosschleife (Reise → Container → Reise → …).
- Die Schnittstelle bleibt gleich, auch wenn sich die Datenbank ändert.
- Man gibt nur heraus, was der Client braucht, und kann berechnete Werte dazunehmen (z. B. das geladene Gewicht eines Containers).
- Lazy geladene Beziehungen machen außerhalb der Transaktion keine Probleme.

## Arten

; Antwort-DTO
: Was der Server zurückgibt, oft flach mit Ids statt verschachtelter Objekte (z. B. `containerId`, `fruitId`, `fruitName`).
; Create-DTO
: Request-Body zum Anlegen, ohne Id (wird von der Datenbank vergeben).
; Fehler-DTO
: `{"message": "…"}` für die [[REST#Fehlerbehandlung|Fehlerbehandlung]]
; Statistik-DTO
: Zusammengesetzte Werte, z. B. aus einer [[JPQL#DTO-Projektion|DTO-Projektion]].
; GraphQL-DTO
: Für [[GraphQL]] **verschachtelt** (Reise mit Containern mit Ladungsposten mit Frucht), damit der Client beliebig tief abfragen kann.

## Records

DTOs schreibt man in Java meist als **Record**: unveränderlich, kurz, mit automatisch erzeugtem Konstruktor, `equals`, `hashCode` und `toString`.

```java
public record BookDto(Long id, String title, double price) {
}
```

Die Getter heißen wie die Felder, ohne `get`: `dto.title()`.

## Mapper

Ein **Mapper** wandelt Entities in DTOs um, z. B. eine Klasse mit statischen Methoden `toDto(entity)`. Listen wandelt man mit `stream().map(Mapper::toDto).toList()` um.

## Validierung

Mit **Bean Validation** (Hibernate Validator) schreibt man Regeln als [[Annotation (Java)|Annotationen]] an die Felder des Create-DTOs:

- `@NotNull`: darf nicht `null` sein
- `@NotBlank`: String darf nicht leer sein
- `@Positive`, `@Min`, `@Max`, `@Size` …

Mit `@Valid` vor dem Parameter der REST-Methode wird geprüft, **bevor** die Methode läuft. Ein Fehler wird zu [[HTTP-Statuscodes#400|400 Bad Request]].

Die Fehlermeldungen hängen von der Sprache des Systems ab; mit `quarkus.default-locale=en` sind sie immer englisch (z. B. „must not be null“).

Achtung bei vorgegebener Regelreihenfolge: Muss zuerst geprüft werden, ob etwas existiert (404), darf die Prüfung auf 400 nicht schon vorher in der Validierung passieren (siehe [[Fruit Shipping#Stolpersteine|Fruit Shipping]]).
