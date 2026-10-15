+++
redirects = [
  "DDL|DDL", "Data Definition Language|DDL",
  "CREATE|DDL", "DROP|DDL", "ALTER|DDL", "TRUNCATE|DDL",
  "DML|DML", "Data Manipulation Language|DML",
  "INSERT|DML", "UPDATE|DML",
  "DCL|DCL", "Data Control Language|DCL",
  "GRANT|DCL", "REVOKE|DCL",
  "DQL|DQL", "Data Query Language|DQL",
  "SELECT|DQL",
  "TCL|TCL", "Transaction Control Language|TCL",
  "COMMIT|TCL", "ROLLBACK|TCL", "SAVEPOINT|TCL",
  "Datenbank|Aufbau einer Datenbank",
]
navbox = ["datenbanken"]
+++
Zu **SQL** gehören folgende Sprachen:

| Abkürzung | Name | Befehle |
|---|---|---|
| [[#DDL|DDL]] | Data Definition Language | `CREATE`, `DROP`, `ALTER`, `TRUNCATE` |
| [[#DML|DML]] | Data Manipulation Language | `INSERT`, `UPDATE`, `DELETE` |
| [[#DCL|DCL]] | Data Control Language | `GRANT`, `REVOKE` |
| [[#DQL|DQL]] | Data Query Language | `SELECT` |
| [[#TCL|TCL]] | Transaction Control Language | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

## Aufbau einer Datenbank

Eine Datenbank besteht aus:

| Teil | Sprache |
|---|---|
| ! Struktur (Tabellen, Trigger, …) | [[#DDL|DDL]] |
| ! Daten | [[#DQL|DQL]], [[#DML|DML]] |
| ! Rechtesystem | [[#DCL|DCL]] |
| ! Transaktionen | [[#TCL|TCL]] |

## DDL

Befehle der **Data Definition Language** für die Tabellenstruktur: `CREATE`, `DROP`, `ALTER`, `TRUNCATE`

## DML

:: Zur HTTP-Methode DELETE siehe [[HTTP-Methoden#DELETE|HTTP-Methoden]].

Befehle der **Data Manipulation Language**: `INSERT`, `UPDATE`, `DELETE`

## DCL

Befehle der **Data Control Language**: `GRANT`, `REVOKE`

## DQL

Befehl der **Data Query Language**: `SELECT`

## TCL

Befehle der **Transaction Control Language**: `COMMIT`, `ROLLBACK`, `SAVEPOINT`
