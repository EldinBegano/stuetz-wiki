+++
redirects = [
  "Cross-Origin Resource Sharing",
  "Same-Origin-Policy|Same-Origin-Policy",
  "Origin|Same-Origin-Policy",
  "Preflight|Preflight",
  "Proxy (Angular)|Proxy",
]
navbox = ["frontend"]

[infobox]
Langform = "Cross-Origin Resource Sharing"
"Geprüft von" = "Webbrowser"
"Erlaubt vom" = "Server (HTTP-Header)"
+++
**CORS** (*Cross-Origin Resource Sharing*) regelt, ob eine Webseite per JavaScript auf einen Server mit einem **anderen Origin** zugreifen darf.

## Same-Origin-Policy

Der **Origin** besteht aus Protokoll, Host und Port. Der Browser erlaubt Anfragen per JavaScript standardmäßig nur an denselben Origin.

Beispiel: Der [[Angular]]-Dev-Server läuft auf `http://localhost:4200`, das [[Quarkus]]-Backend auf `http://localhost:8080`. Wegen des anderen Ports ist das ein anderer Origin, der Browser blockiert die Antwort.

## Erlauben am Server

Der Server erlaubt fremde Origins mit dem Header `Access-Control-Allow-Origin`. In Quarkus:

```properties
quarkus.http.cors.enabled=true
quarkus.http.cors.origins=http://localhost:4200
```

## Preflight

Bei vielen Anfragen (z. B. [[HTTP-Methoden#POST|POST]] mit JSON oder [[HTTP-Methoden#DELETE|DELETE]]) schickt der Browser vorher eine [[HTTP-Methoden#OPTIONS|OPTIONS]]-Anfrage (**Preflight**) und fragt, ob die eigentliche Anfrage erlaubt ist.

## Proxy

Alternative für die Entwicklung: Der Angular-Dev-Server leitet alle Anfragen auf `/api` an das Backend weiter. Der Browser spricht dann nur mit `localhost:4200`, also mit demselben Origin, und CORS ist nicht nötig.

CORS betrifft nur Browser. [[REST#REST-Clients|REST-Clients]] wie Curl oder Postman prüfen es nicht.
