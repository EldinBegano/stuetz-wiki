+++
redirects = [
  "HTTP-Statuscode",
  "Statuscode",
  "Statuscodes",
  "HTTP Status Code",
  "200|200",
  "201|201",
  "Location-Header|201",
  "204|204",
  "400|400",
  "Bad Request|400",
  "404|404",
  "Not Found|404",
  "409|409",
  "Conflict|409",
  "500|500",
]
navbox = ["maschinen"]
+++
**HTTP-Statuscodes** sind dreistellige Zahlen in der Antwort eines Servers. Sie sagen, ob die Anfrage geklappt hat. Bei [[REST]] gehört zu jeder [[HTTP-Methoden|HTTP-Methode]] ein passender Statuscode.

| Klasse | Bedeutung |
|---|---|
| ! 1xx | Information |
| ! 2xx | Erfolg |
| ! 3xx | Umleitung |
| ! 4xx | Fehler des Clients |
| ! 5xx | Fehler des Servers |

## 200

**OK**: Die Anfrage war erfolgreich, die Antwort hat einen Body, z. B. bei [[HTTP-Methoden#GET|GET]].

## 201

**Created**: Eine Ressource wurde angelegt, typisch bei [[HTTP-Methoden#POST|POST]]. Dazu gehört der **Location-Header** mit der URL der neuen Ressource (z. B. `/api/cargo-items/10`), meist auch die neue Ressource als Body.

In Quarkus: `Response.created(uri).entity(dto).build()`; die URI baut man mit `UriInfo`.

## 204

**No Content**: erfolgreich, aber ohne Body, typisch bei [[HTTP-Methoden#DELETE|DELETE]].

## 400

**Bad Request**: Die Anfrage ist ungültig, z. B. ein fehlendes Pflichtfeld ([[DTO#Validierung|Validierung]]) oder ein Gewicht ≤ 0.

## 404

**Not Found**: Die Ressource gibt es nicht, z. B. eine unbekannte Id.

Löscht man dieselbe Ressource zweimal, kommt beim zweiten Mal 404. DELETE ist trotzdem [[Idempotent|idempotent]], weil der Zustand auf dem Server gleich bleibt (die Ressource ist weg).

## 409

**Conflict**: Die Anfrage ist zwar gültig, widerspricht aber dem aktuellen Zustand, z. B. eine verletzte Geschäftsregel (siehe [[Fruit Shipping#Laderegeln|Laderegeln]]).

## 500

**Internal Server Error**: Fehler im Server, z. B. eine Exception, die nicht behandelt wurde (siehe [[REST#Fehlerbehandlung|Fehlerbehandlung]]).
