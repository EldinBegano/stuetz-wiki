+++
redirects = ["GitHub Workflow", "GitHub-Workflows"]
navbox = ["projekt"]
+++
Bei **GitHub Workflows** gibt `on` an, wann der Workflow gestartet wird. Darunter spezifizieren z. B. `issues` und `types` das genauer:

```yaml
on:
  issues:
    types: [opened, edited]
```

Wenn alle Betriebsabläufe auf GitHub laufen, droht ein [[Services#Vendor-Lock-in|Vendor-Lock-in]].
