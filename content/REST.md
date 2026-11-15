+++
redirects = [
  "Representational State Transfer",
  "REST-Client|REST-Clients",
  "REST-Clients|REST-Clients",
  "Insomnia|REST-Clients",
  "HTTP Yac|REST-Clients",
  "Postman|REST-Clients",
  "Curl|REST-Clients",
  "Swagger|REST-Clients",
  "REST-Parameter|Parameter",
  "PathParam|Parameter",
  "QueryParam|Parameter",
  "RequestParam|Parameter",
  "CookieParam|Parameter",
  "Fehlerbehandlung|Fehlerbehandlung",
  "ServerExceptionMapper|Fehlerbehandlung",
  "@ServerExceptionMapper|Fehlerbehandlung",
  "Exception-Mapper|Fehlerbehandlung",
  "ErrorDto|Fehlerbehandlung",
  "Ressource|Ressourcen in Quarkus",
  "REST-Ressource|Ressourcen in Quarkus",
  "JAX-RS|Ressourcen in Quarkus",
  "Jakarta REST|Ressourcen in Quarkus",
  "IntelliJ HTTP Client|REST-Clients",
  "HTTP-Datei|REST-Clients",
]
navbox = ["maschinen"]

[infobox]
Langform = "Representational State Transfer"
"Basiert auf" = "Standards des Internets (HTTP, URLs, JSON/XML etc.) + CRUD"
"Übertragung" = "HTTP"
Datenformate = "Text- und Binärformate"
Endpoints = "mehrere Endpoint-URLs"
"Vorgänger" = "[[SOAP]]"
+++
**REST** (*Representational State Transfer*) gehört zum [[Internet für Maschinen]]: Zwei Maschinen transferieren über Schnittstellen Daten. REST basiert auf den Standards des Internets (HTTP, URLs, JSON/XML etc.) sowie CRUD.

## Datenübertragung

Übertragen werden beliebige Text- (HTML, CSS, JavaScript, …) und Binärformate (Bilder, PDFs, …).

Der Transfer funktioniert über HTTP. Dabei werden [[HTTP-Methoden]] wie [[HTTP-Methoden#GET|GET]], [[HTTP-Methoden#PUT|PUT]], [[HTTP-Methoden#POST|POST]], [[HTTP-Methoden#PATCH|PATCH]] und [[HTTP-Methoden#DELETE|DELETE]] benutzt.

REST verwendet mehrere Endpoint-URLs.

## Parameter

- PathParam
- QueryParam
- RequestParam
- CookieParam

## REST-Clients

- Webbrowser
- Insomnia
- HTTP Yac
- Postman
- Curl
- Swagger (in [[Quarkus#Dev-Modus|Quarkus]] unter `/q/swagger-ui`)
- IntelliJ HTTP Client: Requests in `.http`-Dateien, Variablen wie `{{host}}` pro Environment in `http-client.env.json`; die erwarteten Antworten kann man als Kommentar dazuschreiben

## Ressourcen in Quarkus

Eine **Ressource** ist eine Klasse im Package `boundary` (siehe [[3-Schichten-Modell#Packages|Packages]]) mit Annotationen aus Jakarta REST (früher JAX-RS):

| Annotation | Bedeutung |
|---|---|
| `@Path("books")` | Pfad der Klasse bzw. Methode, mit Platzhaltern wie `{id}` |
| `@GET`, `@POST`, `@DELETE` … | [[HTTP-Methoden|HTTP-Methode]] |
| `@PathParam("id")` | Wert aus dem Pfad |
| `@Produces`, `@Consumes` | Datenformat, z. B. JSON |

Die Ressource ruft nur Repositories und Services auf und gibt [[DTO|DTOs]] zurück, nie Entities. Mit `Response` setzt man den [[HTTP-Statuscodes|Statuscode]], z. B. `Response.created(uri)` für 201 mit `Location`-Header und `Response.noContent()` für 204.

## Fehlerbehandlung

Fehler sollen immer gleich aussehen, z. B. als JSON `{"message": "Book 999 not found"}` (ein Fehler-[[DTO]]).

Die Ressource wirft dafür nur Exceptions; ein **Exception-Mapper** wandelt sie zentral in eine Antwort um. In Quarkus schreibt man eine Klasse mit Methoden, die mit `@ServerExceptionMapper` annotiert sind:

```java
@ServerExceptionMapper
public RestResponse<ErrorDto> mapNotFound(NotFoundException e) {
    return RestResponse.status(Response.Status.NOT_FOUND, new ErrorDto(e.getMessage()));
}
```

| Exception | [[HTTP-Statuscodes|Statuscode]] |
|---|---|
| `NotFoundException` | 404 |
| `BadRequestException`, Fehler der [[DTO#Validierung|Bean Validation]] | 400 |
| eigene Exception für verletzte Geschäftsregeln | 409 |
| nicht behandelte Exception | 500 |

Haben mehrere eigene Exceptions eine gemeinsame Oberklasse, reicht ein Mapper für die Oberklasse.

## Geschichte

Der Vorgänger von REST war [[SOAP]] (Simple Object Access Protocol), entwickelt von Microsoft. Eine Weiterentwicklung von REST ist [[GraphQL]].
