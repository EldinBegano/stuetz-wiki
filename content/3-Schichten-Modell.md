+++
redirects = [
  "Drei-Schichten-Modell",
  "3 Schichten Modell",
  "Boundary Control Entity|Packages",
  "BCE|Packages",
  "Boundary|Packages",
]
navbox = ["backend"]
+++
[[Datei:3-Schichten-Modell.svg|mini|Die drei Schichten: Persistence (Datenbank), Business (Application Server) und Presentation (Webserver)]]

Das **3-Schichten-Modell** besteht aus folgenden Schichten:

1. Persistence (Datenbank)
2. Business (Application Server)
3. Presentation (Webserver)

## Packages

In einem [[Quarkus]]-Backend teilt man den Code oft nach *Boundary – Control – Entity* in Packages auf:

| Package | Inhalt |
|---|---|
| `boundary` | Schnittstellen nach außen: [[REST#Ressourcen in Quarkus|REST-Ressourcen]], [[GraphQL#GraphQL in Quarkus|GraphQL-API]], [[REST#Fehlerbehandlung|Exception-Mapper]] |
| `control` | Logik: [[Panache#Repository|Repositories]], Services mit den Geschäftsregeln, eigene Exceptions |
| `entity` | [[Entität|Entities]] und [[DTO|DTOs]] |

Die Boundary ruft Control auf, Control arbeitet mit den Entities. Die Ressourcen enthalten keine Geschäftslogik.
