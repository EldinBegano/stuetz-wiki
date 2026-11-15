+++
redirects = [
  "Test",
  "Tests",
  "Smoke-Test|Smoke-Test", "Smoketest|Smoke-Test",
  "TDD|TDD", "Test-Driven Development|TDD", "Test-driven|TDD",
  "Playwright|UI-Tests", "UI-Test|UI-Tests",
  "@QuarkusTest|Tests in Quarkus", "QuarkusTest|Tests in Quarkus",
  "REST Assured|REST Assured", "RestAssured|REST Assured",
  "AssertJ|AssertJ", "AssertJ-DB|AssertJ",
  "@TestTransaction|Testdaten und Transaktionen",
  "Hibernate-Statistiken|Geladene Entities zählen",
]
navbox = ["projekt"]
+++
:: Zum Test in SEW siehe [[Teststoff]].

Beim **Testen** unterscheidet man unter anderem [[#Smoke-Test|Smoke-Tests]] und [[#TDD|TDD]].

## Smoke-Test

Man testet nicht systematisch, sondern nur zufällig. Wenn ein Test fehlschlägt, weiß man, dass etwas nicht passt.

## TDD

Bei **TDD** (*Test-Driven Development*) schreibt man zuerst den Test. Erst wenn der Test fehlschlägt, wird neuer Code hinzugefügt – und zwar das Minimalste, damit der Test grün wird.

Regel: Wenn Tests geändert werden, kein Produktivcode; wenn Produktivcode geändert wird, kein Testcode.

## UI-Tests

Die UI testet man mit Playwright.

## Tests in Quarkus

Mit `@QuarkusTest` startet JUnit die ganze Anwendung (einmal für alle Testklassen); Repositories und Services kann man mit `@Inject` direkt testen. Gestartet wird mit `./mvnw test` (siehe [[Maven]]). Die Tests verwenden meist eine [[H2#In-Memory|In-Memory-Datenbank]] über das `%test`-[[Quarkus#Profile|Profil]].

### REST Assured

REST-Endpunkte testet man mit **REST Assured** im Stil *given – when – then*:

```java
given()
    .contentType(ContentType.JSON)
    .body("{\"title\": \"Dune\", \"price\": 12.5}")
.when()
    .post("/api/books")
.then()
    .statusCode(201)
    .header("Location", notNullValue())
    .body("title", is("Dune"));
```

### AssertJ

**AssertJ** liefert lesbare Prüfungen: `assertThat(wert).isEqualTo(…)`, `assertThatThrownBy(() -> …).isInstanceOf(…)`. Mit **AssertJ-DB** prüft man direkt die Datenbank, z. B. ob genau eine Zeile angelegt bzw. gelöscht wurde oder wie viele Zeilen eine Tabelle hat.

### Testdaten und Transaktionen

- Die Tests verlassen sich auf die [[Glossar#Seed-Daten|Seed-Daten]] aus `import.sql`.
- `@TestTransaction`: Der Test läuft in einer [[JPA#Transaktionen|Transaktion]], die am Ende zurückgerollt wird; die Daten sind danach wieder wie vorher.
- Ohne Rollback räumt man mit `@AfterEach` auf, z. B. alle neu angelegten Zeilen löschen.

### Geladene Entities zählen

Mit `quarkus.hibernate-orm.statistics=true` zählt Hibernate, wie viele Entities aus der Datenbank geladen wurden. Ein Test kann so prüfen, dass eine Abfrage wirklich in [[JPQL]] bzw. [[SQL]] filtert und summiert und nicht alle Zeilen in Java lädt (siehe [[JPQL#Rechnen in der Abfrage|Rechnen in der Abfrage]]).
