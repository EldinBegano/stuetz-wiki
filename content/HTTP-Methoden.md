+++
redirects = [
  "HTTP Requests",
  "HTTP-Request",
  "HTTP Methoden",
  "GET|GET",
  "POST|POST",
  "PUT|PUT",
  "PATCH|PATCH",
  "OPTIONS|OPTIONS",
  "HEAD|HEAD",
]
navbox = ["maschinen"]
+++
**HTTP-Methoden** (HTTP Requests) werden unter anderem von [[REST]] benutzt.

| Methode | safe | [[Idempotent|idempotent]] |
|---|---|---|
| [[#GET|GET]] | ja | ja |
| [[#POST|POST]] | nein | nein |
| [[#PUT|PUT]] | nein | ja |
| [[#PATCH|PATCH]] | nein | nein |
| [[#DELETE|DELETE]] | nein | ja |
| [[#OPTIONS|OPTIONS]] | ja | ja |
| [[#HEAD|HEAD]] | ja | ja |

## GET

Ein GET-Request wird verwendet, um Daten von einem Webserver zu lesen bzw. abzurufen. Wurden die Daten erfolgreich vom Server abgerufen, gibt GET den HTTP-Statuscode 200 (OK) zurück. GET ist *safe* und *idempotent*.

## POST

Ein POST-Request wird verwendet, um Daten (Datei, Formulardaten usw.) an den Server zu senden. Bei erfolgreicher Erstellung wird der HTTP-Statuscode 201 zurückgegeben. POST ist *unsafe* und *nicht idempotent*.

## PUT

Ein PUT-Request wird verwendet, um Daten auf dem Server zu ändern. Er ersetzt den gesamten Inhalt an einer bestimmten Stelle durch die Daten, die im Body (Payload) übergeben werden. Gibt es keine passende Ressource, wird eine erzeugt. PUT ist *unsafe* und *idempotent*.

## PATCH

PATCH ist ähnlich wie ein PUT-Request. Der einzige Unterschied: PATCH ändert nur einen Teil der Daten und ersetzt nur den Inhalt, der aktualisiert werden soll. PATCH ist *unsafe* und *nicht idempotent*.

## DELETE

:: Zum SQL-Befehl DELETE siehe [[SQL#DML|SQL (DML)]].

Ein DELETE-Request wird verwendet, um Daten an einer bestimmten Stelle auf dem Server zu löschen. DELETE ist *unsafe* und *idempotent*.

## OPTIONS

OPTIONS beschreibt die Kommunikationsoptionen für die Zielressource. OPTIONS ist *safe* und *idempotent*.

## HEAD

HEAD ist ähnlich wie GET, ruft aber nur die Header einer Ressource ab, ohne den Body. HEAD ist *safe* und *idempotent*.
