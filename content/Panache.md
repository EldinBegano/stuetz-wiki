+++
redirects = [
  "Hibernate ORM mit Panache",
  "Hibernate ORM with Panache",
  "PanacheRepository|Repository",
  "PanacheEntity|Repository und Active Record",
  "Repository-Pattern|Repository und Active Record",
  "Repository|Repository",
  "Active Record|Repository und Active Record",
  "Sort.by|Methoden",
]
navbox = ["datenbanken"]

[infobox]
Art = "[[Quarkus]]-Erweiterung"
"Baut auf" = "Hibernate ORM ([[JPA]])"
Patterns = ["Repository", "Active Record"]
+++
**Panache** (*Hibernate ORM mit Panache*) ist eine [[Quarkus]]-Erweiterung, die [[JPA]] mit Hibernate vereinfacht. Standardabfragen wie „alle laden“, „nach Id suchen“ oder „speichern“ muss man nicht mehr selbst schreiben.

## Repository und Active Record

Panache bietet zwei Patterns:

| | Repository | Active Record |
|---|---|---|
| ! Wo sind die Methoden? | in einer eigenen Repository-Klasse | in der Entity selbst (statisch) |
| ! Entity | normale [[Entität|Entity]] | erbt von `PanacheEntity` |
| ! Aufruf | `bookRepository.listAll()` | `Book.listAll()` |
| ! Injection | Repository wird mit [[CDI]] injiziert | keine |

In der [[Fruit Shipping|1. Leistungsfeststellung]] war das **Repository**-Pattern verlangt, kein Active Record.

## Repository

Ein Repository implementiert `PanacheRepository<Entity>` und ist eine CDI-Bean (`@ApplicationScoped`). Es liegt im Package `control` (siehe [[3-Schichten-Modell#Packages|Packages]]).

```java
@ApplicationScoped
public class BookRepository implements PanacheRepository<Book> {

    public List<Book> findByAuthor(long authorId) {
        return list("author.id", Sort.by("title"), authorId);
    }
}
```

## Methoden

| Methode | Bedeutung |
|---|---|
| `findById(id)` | eine Entity oder `null` |
| `listAll()`, `listAll(Sort.by("name"))` | alle Entities (sortiert) |
| `list("feld", wert)` | Kurzform für `from Entity where feld = ?1` |
| `find(…)` | wie `list`, aber mit Paging und Weiterverarbeitung |
| `count()` | Anzahl |
| `persist(entity)` | speichern |
| `delete(entity)`, `deleteById(id)`, `delete("id > ?1", 9L)` | löschen |
| `getEntityManager()` | Zugriff auf den [[JPA#EntityManager|EntityManager]] für eigene [[JPQL]]-, Named- oder native Abfragen |

Schreibende Methoden brauchen eine [[JPA#Transaktionen|Transaktion]] (`@Transactional`).

`listAll()` lädt **alle** Zeilen. Für Filtern und Summieren schreibt man eine Abfrage (siehe [[JPQL#Rechnen in der Abfrage|Rechnen in der Abfrage]]).
