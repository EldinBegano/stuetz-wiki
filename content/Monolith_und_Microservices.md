+++
redirects = ["Monolith", "Monolithen", "Microservices", "Microservice"]
navbox = ["backend"]
+++
Bei einem **Monolithen** sind alle Services in einem JAR-File. Bei **Microservices** gibt es für jeden Service eine eigene Datenbank und ein eigenes File.

[[Datei:Monolith_und_Microservices.svg|Beispiel mit Lager und Verkauf: als Monolith in einem JAR-File, als Microservices jeweils in einem eigenen JAR-File mit eigener Datenbank]]

| | Monolith | Microservices |
|---|---|---|
| ! Services | alle in einem JAR-File | je Service eine Datenbank und ein File |
| ! Beispiel | Lager und Verkauf in einem JAR-File | Lager und Verkauf jeweils in einem eigenen JAR-File |

## Verwendung

Wir programmieren einen Monolithen. Wir verwenden Monolithen, weil es keinen Grund gibt, ihn aufzuteilen – erst wenn es einen Grund gibt, sollte man ihn aufteilen.
