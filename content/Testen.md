+++
redirects = [
  "Test",
  "Tests",
  "Smoke-Test|Smoke-Test", "Smoketest|Smoke-Test",
  "TDD|TDD", "Test-Driven Development|TDD", "Test-driven|TDD",
  "Playwright|UI-Tests", "UI-Test|UI-Tests",
]
navbox = ["projekt"]
+++
:: Zum Test in SEW siehe [[Teststoff]].

Beim **Testen** unterscheidet man unter anderem [[#Smoke-Test|Smoke-Tests]] und [[#TDD|TDD]].

## Smoke-Test

Man testet nicht systematisch, sondern nur zufällig. Wenn ein Test fehlschlägt, weiß man, dass etwas nicht passt.

## TDD

Bei **TDD** (*Test-Driven Development*) schreibt man zuerst den Test. Erst wenn der Test fehlschlägt, wird neuer Code hinzugefügt – und zwar das Minimalste, damit der Test grün wird.

Regel: Wenn Tests geändert werden, kein Produktivcode; wenn Produktivcode geändert wird, kein Testcode.

## UI-Tests

Die UI testet man mit Playwright.
