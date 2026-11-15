+++
redirects = [
  "JDBI|Quarkus vs. JDBI und co.",
  "application.properties|Konfiguration",
  "import.sql|Konfiguration",
  "Profil (Quarkus)|Profile",
  "Quarkus-Profile|Profile",
  "Dev UI|Dev-Modus",
  "Dev-UI|Dev-Modus",
  "quarkus:dev|Dev-Modus",
  "Swagger-UI|Dev-Modus",
  "Quarkus-Erweiterung|Erweiterungen",
]
navbox = ["backend"]

[infobox]
Art = "Java-Framework"
"Gemacht für" = "[[Microservices]], Cloud"
Build = "[[Maven]]"
+++
**Quarkus** ist ein **Java-Framework** für [[Microservices]] und ist dafür gemacht, in der Cloud zu laufen.

Unter [[Kubernetes]] werden mehr Quarkus-Container hochgefahren, je mehr Anfragen kommen.

## Quarkus vs. JDBI und co.

### Quarkus

- weniger Code
- QUIC-Support
- Observability-Dashboard (Quarkus 4 Link)

### JDBI und co.

- funktioniert ohne „Magie“, also ohne [[Annotation (Java)|Annotationen]]

## Gründe für ein Framework

Gründe, bei einem Framework zu bleiben:

- weniger Code
- wird automatisch geupdatet

## Erweiterungen

Funktionen bindet man als Erweiterungen (Dependencies in der `pom.xml`, siehe [[Maven]]) ein:

| Erweiterung | Wofür |
|---|---|
| Hibernate ORM mit [[Panache]] | [[JPA]] mit Repositories |
| JDBC-Treiber (z. B. [[H2]]) | Verbindung zur Datenbank |
| REST Jackson | [[REST]]-Ressourcen mit JSON |
| Hibernate Validator | [[DTO#Validierung|Bean Validation]] |
| SmallRye GraphQL | [[GraphQL#GraphQL in Quarkus|GraphQL]] |
| SmallRye OpenAPI | API-Beschreibung und Swagger-UI |
| SmallRye Health | Health-Checks (z. B. für [[Kubernetes]]) |

## Dev-Modus

`./mvnw quarkus:dev` startet die Anwendung im **Dev-Modus** auf http://localhost:8080. Änderungen am Code werden ohne Neustart übernommen.

| URL | Inhalt |
|---|---|
| `/q/dev-ui` | Dev UI: Übersicht über Erweiterungen, Konfiguration, Datenbank |
| `/q/swagger-ui` | REST-Endpunkte ausprobieren |
| `/q/graphql-ui` | GraphQL-Abfragen ausprobieren |

Normalerweise gibt es die UIs nur im Dev-Modus; mit `quarkus.swagger-ui.always-include=true` bzw. `quarkus.smallrye-graphql.ui.always-include=true` auch im fertigen Build.

## Konfiguration

Die Konfiguration steht in `src/main/resources/application.properties`, z. B.:

| Eigenschaft | Bedeutung |
|---|---|
| `quarkus.datasource.db-kind`, `…jdbc.url`, `…username`, `…password` | Datenbankverbindung (siehe [[H2#Betriebsarten|H2]]) |
| `quarkus.hibernate-orm.schema-management.strategy=drop-and-create` | Tabellen bei jedem Start löschen und aus den Entities neu anlegen |
| `quarkus.hibernate-orm.sql-load-script=import.sql` | danach die Testdaten aus `import.sql` einfügen |
| `quarkus.hibernate-orm.log.sql=true` | erzeugtes SQL in der Konsole anzeigen |
| `quarkus.hibernate-orm.statistics=true` | [[Testen#Geladene Entities zählen|Hibernate-Statistiken]] einschalten |
| `quarkus.rest.path=/api` | Basis-Pfad aller [[REST]]-Ressourcen |
| `quarkus.http.cors.enabled`, `…origins` | [[CORS]] für das Frontend erlauben |
| `quarkus.default-locale=en` | Sprache der Validierungsmeldungen unabhängig vom Betriebssystem |

### Profile

Mit einem **Profil** gilt eine Eigenschaft nur in einer Umgebung. Man schreibt das Profil mit `%` davor:

- `%dev.`: Dev-Modus (z. B. SQL-Log einschalten)
- `%test.`: Tests (z. B. [[H2#In-Memory|In-Memory-Datenbank]], Statistiken)
- `%prod.`: fertige Anwendung

```properties
%test.quarkus.datasource.jdbc.url=jdbc:h2:mem:test;DB_CLOSE_DELAY=-1
%dev.quarkus.hibernate-orm.log.sql=true
```
