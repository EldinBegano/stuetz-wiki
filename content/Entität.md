+++
redirects = ["Entitäten", "Entitätsklasse", "Entity", "Entity-Objekt", "Business-Objekt"]
navbox = ["datenbanken"]
+++
Eine **Entität** ist eine Klasse, die in der Datenbank gespeichert wird. Sie ist eine Business-Klasse, keine technische.

Ein **Entity-Objekt** ist ein Business-Objekt wie Person, Rechnung oder Bestellung – nichts Technisches wie ein Iterator.

## Verwendung

- Bei [[JPA]] wird jedem Entity-Objekt eine Zeile in der Datenbank zugesprochen (siehe [[JPA#Lebenszyklus|Lebenszyklus]]).
- Im [[Externes Schema|externen Schema]] werden die Entitäten für die User in Views zusammengeführt.
- Bei [[JSON Binding]] wird eine Entitätsklasse zu einem JSON-Objekt gemacht.
- Über Schnittstellen gibt man Entities nicht direkt heraus, sondern [[DTO|DTOs]].
