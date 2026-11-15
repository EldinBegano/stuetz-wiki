+++
redirects = ["Maven Wrapper|Maven Wrapper", "mvnw|Maven Wrapper", "pom.xml|pom.xml"]
navbox = ["backend"]

[infobox]
Art = "Tool"
Aufgaben = "Management von Dependencies und Libraries, Build, Test, Packaging, Deployment"
Speicherort = "`.m2`-Verzeichnis"
+++
**Maven** ist ein Tool zum Managen der benötigten Dependencies und Libraries für ein Programm. Gespeichert werden sie im `.m2`-Verzeichnis.

## Aufgaben

Neben dem Management der Dependencies übernimmt Maven auch:

- Build
- Test
- Packaging
- Deployment

## pom.xml

In der `pom.xml` stehen die Dependencies des Projekts (bei [[Quarkus]] die [[Quarkus#Erweiterungen|Erweiterungen]]) und die Plugins für Build und Test.

## Maven Wrapper

Der **Maven Wrapper** (`mvnw`, unter Windows `mvnw.cmd`) lädt die passende Maven-Version selbst herunter. Maven muss also nicht installiert sein und alle verwenden dieselbe Version.

| Befehl | Bedeutung |
|---|---|
| `./mvnw quarkus:dev` | Quarkus im [[Quarkus#Dev-Modus|Dev-Modus]] starten |
| `./mvnw test` | alle Tests ausführen (siehe [[Testen#Tests in Quarkus|Tests in Quarkus]]) |
