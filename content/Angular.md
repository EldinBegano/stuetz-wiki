+++
redirects = [
  "Angular-Client",
  "Standalone Component|Standalone Components",
  "Standalone Components|Standalone Components",
  "NgModule|Standalone Components",
  "Signal|Signals",
  "Signals|Signals",
  "computed()|Signals",
  "signal()|Signals",
  "input.required|Komponenten",
  "output()|Komponenten",
  "Control Flow|Control Flow",
  "@if|Control Flow",
  "@for|Control Flow",
  "@switch|Control Flow",
  "ngIf|Control Flow",
  "ngFor|Control Flow",
  "inject()|Dependency Injection",
  "Reactive Forms|Formulare",
  "ng generate|Befehle",
  "npm ci|Befehle",
]
navbox = ["frontend"]

[infobox]
Art = "Frontend-Framework"
Sprache = "TypeScript"
Version = "21 (in der [[Fruit Shipping|1. Leistungsfeststellung]])"
"Dev-Server" = "http://localhost:4200"
+++
**Angular** ist ein Frontend-Framework für Webanwendungen, geschrieben in TypeScript. Ein Angular-Client spricht über [[REST]] (oder [[GraphQL]]) mit dem Backend, z. B. mit [[Quarkus]].

Moderne Angular-Versionen verwenden [[#Standalone Components|Standalone Components]], [[#Signals|Signals]], den neuen [[#Control Flow|Control Flow]] und `inject()` ([[#Dependency Injection|Dependency Injection]]).

## Standalone Components

Eine **Standalone Component** braucht kein `NgModule`. Sie gibt selbst an, was sie verwendet (andere Komponenten in `imports`). Neue Komponenten erzeugt man mit `ng generate component <name>`.

## Signals

Ein **Signal** ist ein Wert, bei dessen Änderung Angular die Anzeige automatisch aktualisiert. Der UI-Zustand (ausgewählte Reise, Formularfelder, Fehlermeldung, Liste) wird in Signals gespeichert.

| Funktion | Bedeutung |
|---|---|
| `signal(start)` | Signal mit Startwert; lesen mit `name()`, schreiben mit `set(…)` oder `update(…)` |
| `computed(() => …)` | abgeleiteter Wert, wird automatisch neu berechnet, wenn sich ein verwendetes Signal ändert |

```ts
books = signal<BookDto[]>([]);
total = computed(() => this.books().reduce((sum, b) => sum + b.price, 0));
valid = computed(() => this.title() !== '' && this.price() > 0);
```

Mit `computed()` kann man z. B. ein Gesamtgewicht im Client aus einer Liste berechnen oder einen Button deaktivieren (`[disabled]="!valid()"`).

## Komponenten

Daten gehen zwischen Eltern- und Kind-Komponente über Signal-basierte Inputs und Outputs:

- `input.required<T>()`: Wert, den die Eltern-Komponente übergeben **muss**, z. B. eine Liste
- `output<T>()`: Ereignis an die Eltern-Komponente, ausgelöst mit `emit(wert)`, z. B. die Id eines Eintrags, der gelöscht werden soll

```html
<app-book-list [books]="books()" (remove)="onRemove($event)" />
```

So bleibt die Liste eine reine Anzeige-Komponente, die Eltern-Komponente ruft den Service auf.

## Control Flow

Der neue **Control Flow** ersetzt `*ngIf`, `*ngFor` und `ngSwitch`:

```html
@if (error()) {
  <p class="error">{{ error() }}</p>
}

@for (book of books(); track book.id) {
  <li>{{ book.title }}</li>
} @empty {
  <li>keine Bücher</li>
}

@switch (container.climacteric) {
  @case (true) { klimakterisch }
  @case (false) { nicht-klimakterisch }
  @default { leer }
}
```

Bei `@for` ist `track` Pflicht: Angular erkennt damit, welcher Eintrag welcher ist (meist die Id).

## Dependency Injection

Services holt man mit `inject()` statt über den Konstruktor (vergleiche [[CDI]] im Backend):

```ts
private service = inject(BookService);
```

Ein Service kapselt die HTTP-Aufrufe (`HttpClient`); die Models sind TypeScript-Interfaces, die den [[DTO|DTOs]] des Backends entsprechen.

## Formulare

Statt Reactive Forms kann man Formularfelder direkt an Signals binden:

- `[value]="title()"`: Signal → Feld
- `(input)="title.set($any($event.target).value)"`: Feld → Signal (bei `<select>` mit `(change)`)

Nach erfolgreichem Senden setzt man die Signals zurück und lädt die Liste neu. Bei einem Fehler zeigt man die `message` aus der [[REST#Fehlerbehandlung|Fehlerantwort]] des Servers an.

## Befehle

| Befehl | Bedeutung |
|---|---|
| `npm ci` | Abhängigkeiten genau nach `package-lock.json` installieren |
| `npm start` | Dev-Server auf http://localhost:4200 (mit [[CORS#Proxy|Proxy]] für `/api`) |
| `npm run build` | Produktions-Build; muss ohne Fehler durchlaufen |
| `ng generate component <name>` | neue Komponente anlegen |
