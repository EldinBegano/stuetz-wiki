+++
redirects = [
  "1. Leistungsfeststellung",
  "Leistungsfeststellung",
  "LF1",
  "Fruit-Shipping",
  "Reefer|Fachlicher Hintergrund",
  "Kühlcontainer|Fachlicher Hintergrund",
  "Klimakterisch|Klimakterische Früchte",
  "Klimakterische Früchte|Klimakterische Früchte",
  "Ethylen|Klimakterische Früchte",
  "Laderegeln|Laderegeln",
  "Solltemperatur|Solltemperatur",
]

[infobox]
Fach = "SEW (5AHITM)"
Datum = "19.10.2026, 08:00–11:45"
Arbeitszeit = "ca. 165 Minuten"
Backend = ["Java 25", "[[Quarkus]] 3.40", "Hibernate ORM mit [[Panache]]", "[[H2]]"]
Schnittstellen = ["[[REST]]", "[[GraphQL]]"]
Frontend = "[[Angular]] 21"
+++
:: Zum Teststoff allgemein siehe [[Teststoff]].

**Fruit Shipping** war die Angabe der **1. Leistungsfeststellung** in SEW am 19.10.2026. Eine Reederei transportiert Obst in Kühlcontainern; zu bauen waren Abfragen, Geschäftslogik, eine [[REST]]-Schnittstelle, ein [[Angular]]-Client und (für „Sehr gut“) eine [[GraphQL]]-Schnittstelle.

## Organisatorisches

- Angabe zuerst **vollständig** lesen (ca. 10 Minuten).
- Alle Tests sind vorgegeben, man muss sie grün machen. Die Tests darf man **nicht ändern** (ähnlich wie bei [[Testen#TDD|TDD]]).
- Nach jeder Aufgabe committen und pushen, mit aussagekräftiger Commit-Message (z. B. `feat: …`, siehe [[Glossar#Conventional Commits|Conventional Commits]]).
- Vorgegeben: [[Entität|Entities]], [[DTO|DTOs]], Exceptions, `import.sql`, `application.properties`, der Angular-Service und die Models.
- Alle Bezeichner im Code und in der Datenbank sind englisch.
- Erlaubt: eigene Unterlagen und die offizielle Dokumentation (Quarkus, Hibernate, Angular, MDN).
- Nicht erlaubt: [[KI|KI-Assistenten]] (auch in der IDE) und jede Form der Kommunikation.

## Lernziele

- Typisierte [[JPQL]]-Abfragen mit dem [[Panache#Repository und Active Record|Repository-Pattern]] (kein Active Record)
- Eine [[JPQL#Named Queries|Named Query]] mit [[JPQL#DTO-Projektion|Konstruktor-Ausdruck]] und eine [[JPQL#Native SQL-Abfragen|native SQL-Abfrage]]
- Geschäftslogik mit klar definierter Regelreihenfolge
- REST-Endpunkte mit [[DTO|DTOs]] und sauberer [[REST#Fehlerbehandlung|Fehlerbehandlung]]
- Angular-Client mit [[Angular#Standalone Components|Standalone Components]], [[Angular#Signals|Signals]] und dem neuen [[Angular#Control Flow|Control Flow]]
- (Sehr gut) eine lesende [[GraphQL]]-Schnittstelle

## Fachlicher Hintergrund

Obst wird in Kühlcontainern (*Reefer*) von Übersee nach Europa transportiert.

| Begriff (Code) | Bedeutung |
|---|---|
| ! Reise (`Voyage`) | Schiff, Abfahrts- und Zielhafen, Abfahrtsdatum; hat mehrere Container |
| ! Container (`Container`) | Containernummer, Kapazität in kg; gehört zu einer Reise |
| ! Ladungsposten (`CargoItem`) | Gewicht und Herkunftsland; liegt in einem Container und ist eine Obstsorte |
| ! Obstsorte (`Fruit`) | Name, klimakterisch ja/nein, Temperaturbereich (min. bis max. °C) |

### Klimakterische Früchte

; Klimakterisch
: Die Frucht produziert das Reifegas **Ethylen** und **reift nach der Ernte nach**, z. B. Banane, Mango, Avocado, Tomate, Apfel, Kiwi.
; Nicht-klimakterisch
: Die Frucht reift nach der Ernte nicht nach, verdirbt aber durch das Ethylen der anderen Früchte schneller, z. B. Orange, Zitrone, Ananas, Weintraube, Erdbeere, Kirsche.

Vereinfachung in der Angabe: In Wirklichkeit ist die Ethylen-Empfindlichkeit eine Abstufung. Hier gibt es nur `climacteric` (`true`/`false`) und die Regel: Ein Container enthält **entweder nur klimakterische oder nur nicht-klimakterische** Früchte.

## Datenmodell

[[Datei:Fruit_Shipping_Datenmodell.svg|mini|Tabellen der Angabe: Eine Reise hat mehrere Container, ein Container enthält mehrere Ladungsposten, jeder Ladungsposten ist genau eine Obstsorte.]]

- `Voyage`–`Container` und `Container`–`CargoItem` sind [[JPA#Beziehungen|bidirektional]] (`@OneToMany(mappedBy = …)` und `@ManyToOne`).
- `CargoItem`–`Fruit` ist nur `@ManyToOne`.
- Der Container hat **berechnete Werte**, die keine Spalten sind, sondern in Java aus den Ladungsposten berechnet werden:
    - `loadedKg`: Summe der Gewichte
    - `freeKg`: Kapazität minus geladenes Gewicht
    - `setpointTemperature`: [[#Solltemperatur|Solltemperatur]]
    - `climacteric`: Kategorie der geladenen Früchte
- Bei einem leeren Container sind `setpointTemperature` und `climacteric` `null`.
- Die Testdaten ([[Glossar#Seed-Daten|Seed-Daten]]) stehen in `import.sql`; die Tests verlassen sich auf genau diese Daten.

## Laderegeln

Wird ein Ladungsposten in einen Container geladen, werden die Regeln **genau in dieser Reihenfolge** geprüft. Die erste verletzte Regel bestimmt den Fehler:

| # | Regel | Fehler |
|---|---|---|
| 1 | Container und Frucht müssen existieren. | `NotFoundException`, [[HTTP-Statuscodes#404|404]] |
| 2 | Das Gewicht muss größer als 0 kg sein. | `BadRequestException`, [[HTTP-Statuscodes#400|400]] |
| 3 | Nur klimakterische **oder** nur nicht-klimakterische Früchte; ein leerer Container nimmt beides. | `IncompatibleCargoException`, [[HTTP-Statuscodes#409|409]] |
| 4 | Die Temperaturbereiche aller Früchte im Container müssen sich überlappen. | `TemperatureConflictException`, 409 |
| 5 | Das Gewicht darf die Kapazität nicht überschreiten; genau voll ist erlaubt. | `CapacityExceededException`, 409 |

[[Datei:Laderegeln.svg|Die fünf Laderegeln werden der Reihe nach geprüft. Die erste verletzte Regel bestimmt den Fehler.]]

Alle drei 409-Exceptions erben von einer gemeinsamen Oberklasse (`CargoRuleException`), damit ein einziger [[REST#Fehlerbehandlung|Exception-Mapper]] für alle reicht.

Bei Erfolg wird der neue Ladungsposten gespeichert, bei einem Fehler wird **nichts** gespeichert (eine Methode mit `@Transactional` wird bei einer Exception zurückgerollt, siehe [[JPA#Transaktionen|Transaktionen]]).

### Solltemperatur

Die **Solltemperatur** eines Containers ist die **höchste Mindesttemperatur** seiner Früchte. Ein leerer Container hat keine Solltemperatur (`null`).

Die Temperaturbereiche überlappen sich genau dann, wenn die höchste Mindesttemperatur kleiner oder gleich der niedrigsten Höchsttemperatur ist.

Beispiel: Ein Container enthält Banane (13–15 °C) und Mango (10–13 °C). Die Bereiche überlappen bei 13 °C, die Solltemperatur ist 13 °C.

| neue Frucht | Ergebnis |
|---|---|
| ! Tomate (klimakterisch, 10–13 °C) | erlaubt |
| ! Orange (nicht-klimakterisch) | 409 „incompatible cargo“ (Regel 3) |
| ! Apfel (klimakterisch, -1–4 °C) | 409 „temperature conflict“ (Regel 4) |

### Stolpersteine

- Die Regeln beziehen sich nur auf die Ladungsposten **des Ziel-Containers**, nicht auf alle Ladungsposten in der Datenbank.
- Bei Regel 4 muss man die neue Frucht mit den Früchten im Container vergleichen; dass bei der neuen Frucht min ≤ max gilt, reicht nicht.
- „Genau voll ist erlaubt“: Fehler nur bei geladen + neu > Kapazität.
- Das Gewicht > 0 prüft der Service, nicht eine [[DTO#Validierung|Validierungs-Annotation]] im DTO: Sonst würde ein ungültiges Gewicht schon vor der Existenzprüfung 400 liefern und die Reihenfolge wäre verletzt.

## Aufgaben

### Block A: Abfragen

Filtern, Gruppieren und Summieren passiert **in der Abfrage** ([[JPQL]] bzw. [[SQL]] mit `where`, `group by`, `sum(…)`), nicht in Java. Alle Zeilen laden (`listAll()`) und dann mit Schleife oder Stream filtern ist verboten; die Tests zählen mit den [[Testen#Geladene Entities zählen|Hibernate-Statistiken]], wie viele Entities geladen werden.

1. Gesamtgewicht einer Reise: [[JPQL#Typisierte Abfragen|typisierte Abfrage]] mit `sum`; ohne Ladung ist das Ergebnis `0` (`coalesce`, siehe [[JPQL#Aggregation|Aggregation]]).
2. Gewicht pro Frucht: [[JPQL#Named Queries|Named Query]] in der Entity mit [[JPQL#DTO-Projektion|Konstruktor-Ausdruck]], das schwerste zuerst.
3. Container mit freier Kapazität: leere Container eingeschlossen, also `left join` ([[JPQL#Joins|Joins]]) mit `group by` und `having`.
4. Container pro Kategorie: [[JPQL#Native SQL-Abfragen|native SQL-Abfrage]]; leere Container werden nicht gezählt.

### Block B: Geschäftslogik

Ladung prüfen und speichern nach den [[#Laderegeln|Laderegeln]], in der angegebenen Reihenfolge.

### Block C: REST-Schnittstelle

Ressourcen im Package `boundary` (siehe [[3-Schichten-Modell#Packages|Packages]]). Alle Antworten sind [[DTO|DTOs]], niemals Entities. Der Basis-Pfad `/api` ist in der [[Quarkus#Konfiguration|Konfiguration]] gesetzt.

| Methode und Pfad | Beschreibung | Antwort |
|---|---|---|
| `GET /api/fruits` | alle Früchte, nach Name sortiert | 200 |
| `GET /api/voyages` | alle Reisen, nach Abfahrt sortiert | 200 |
| `GET /api/voyages/{id}/containers` | Container der Reise | 200, 404 |
| `GET /api/voyages/{id}/statistics` | Gesamtgewicht, Gewicht pro Frucht, Container pro Kategorie | 200, 404 |
| `POST /api/containers/{id}/cargo-items` | Ladung laden | 201 + `Location`-Header ([[HTTP-Statuscodes#201|201]]), 400, 404, 409 |
| `GET /api/cargo-items/{id}` | ein Ladungsposten | 200, 404 |
| `DELETE /api/cargo-items/{id}` | Ladungsposten entfernen | 204, 404 |

Fehler werden immer als JSON `{"message": "…"}` beantwortet ([[REST#Fehlerbehandlung|Fehlerbehandlung]]). Die erwarteten Antworten stehen in einer `.http`-Datei ([[REST#REST-Clients|IntelliJ HTTP Client]]).

### Block D: Angular-Client

Seite mit Reise-Auswahl (Dropdown), Containerliste (Nummer, Kategorie oder *leer*, Solltemperatur, geladenes und freies Gewicht, Ladungsposten) und Formular „Ladung laden“.

- Gesamtgewicht der Reise im Client mit `computed()` ([[Angular#Signals|Signals]]) aus der Containerliste berechnen.
- Button deaktiviert, solange ein Feld fehlt oder das Gewicht ≤ 0 ist.
- Nach Erfolg: Liste neu laden, Formular leeren. Bei Fehler: `message` des Servers anzeigen.
- Jeder Ladungsposten hat einen Button zum Entfernen; die Listen-Komponente meldet die Id mit `output()` nach oben ([[Angular#Komponenten|Komponenten]]).
- Vorgaben: [[Angular#Standalone Components|Standalone Components]], [[Angular#Control Flow|Control Flow]], [[Angular#Signals|Signals]], `inject()` ([[Angular#Dependency Injection|Dependency Injection]]), Formularfelder mit `[value]` und `(input)` statt Reactive Forms ([[Angular#Formulare|Formulare]]).
- Kontrolle: `npm run build` ohne Fehler und Test im Browser.

### Block E: GraphQL

Lesende [[GraphQL#GraphQL in Quarkus|GraphQL-Schnittstelle]] mit den Queries `voyages`, `voyage(id)` (bei unbekannter Id `null`) und `fruits(climacteric)`. Mit eigenen GraphQL-[[DTO|DTOs]] funktionieren verschachtelte Abfragen (Reise → Container → Ladungsposten → Frucht).

## Projekt starten

1. Datenbank: [[H2#Server-Modus|H2-Server]] einmalig anlegen, dann starten (eigenes Terminal)
2. Backend: `./mvnw quarkus:dev` ([[Quarkus#Dev-Modus|Dev-Modus]], http://localhost:8080)
3. Tests: `./mvnw test`
4. Frontend: `npm ci`, dann `npm start` (http://localhost:4200, `/api` wird [[CORS#Proxy|an das Backend weitergeleitet]])
