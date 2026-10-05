+++
redirects = [
  "JDBC|JDBC",
  "ResultSet|JDBC",
  "OR-Mapper|OR-Mapper",
  "ORM|OR-Mapper",
  "JPA|OR-Mapper",
  "EntityFramework|OR-Mapper",
]
navbox = ["datenbanken"]
+++
Für den **Datenbankzugriff** gibt es [[#JDBC|JDBC]] und [[#OR-Mapper|OR-Mapper]].

## JDBC

JDBC ist eine Low-Level-API. Man verwendet [[SQL]]-Statements und bekommt ein ResultSet (Tabellen) zurück. Einzelne Zeilen müssen in Objekte umgewandelt werden.

## OR-Mapper

OR-Mapper (ORM) wie JPA, EntityFramework usw. geben bereits Objekte zurück. Dabei wird (in Java) [[#JDBC|JDBC]] verwendet.
