+++
redirects = ["CDI", "Dependency Injection|Dependency Injection", "DI-Container|DI-Container", "@Inject|Beispiel"]
navbox = ["backend"]
+++
**Context und Dependency Injection** (**CDI**) verwaltet Objekte und ihre Abhängigkeiten.

## Begriffe

; Context
: der Zusammenhang von allem (auch: Lebenslauf)
; Dependency
: ein Objekt, auf dem etwas aufgebaut ist und ohne das es nicht funktioniert

## Aufgaben

- Objekte und ihre Abhängigkeiten verwalten (Objekte erstellen mit `@Inject`)
    - Man erzeugt Objekte nicht selbst mit `new`.
- Objekte und Abhängigkeiten mit einem Lebenszyklus versehen
    - Variablen werden erst zur Laufzeit belegt.
    - Man kann die Lebensdauer einstellen.

## Dependency Injection

Dependency Injection bedeutet, dass man nicht mehr `new` verwendet, sondern dass der übergeordnete Container mit Referenzvariablen auf die neuen Objekte zeigt, die davor erstellt wurden.

## DI-Container

Der DI-Container hat einen Pool, aus dem die Objekte kommen.

## Beispiel

```java
# BSP ohne CDI
PersonRepository personRepo = new PersonRepository();

# BSP mit CDI
@Inject
List<Person> persons
```
