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

[[Datei:Datenbankzugriff.svg|[[#JDBC|JDBC]]: Man verwendet SQL-Statements und bekommt ein ResultSet (Tabellen) zurück; einzelne Zeilen müssen in Objekte umgewandelt werden. [[#OR-Mapper|OR-Mapper]] geben bereits Objekte zurück und verwenden dabei JDBC.]]

## JDBC

JDBC ist eine Low-Level-API. Man verwendet [[SQL]]-Statements und bekommt ein ResultSet (Tabellen) zurück. Einzelne Zeilen müssen in Objekte umgewandelt werden.

## OR-Mapper

OR-Mapper (ORM) wie JPA, EntityFramework usw. geben bereits Objekte zurück. Dabei wird (in Java) [[#JDBC|JDBC]] verwendet.
