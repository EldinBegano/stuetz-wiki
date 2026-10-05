+++
redirects = ["Orchestrierungssystem", "Pod|Aufbau"]
navbox = ["backend"]

[infobox]
Art = "Orchestrierungssystem für Container"
Aufgaben = "Deployment, Skalierung, Selbstheilung"
+++
**Kubernetes** ist ein **Orchestrierungssystem** für Container. Kubernetes ist die Technologie, die hinter manchen Clouds steht.

## Aufgaben

Kubernetes kümmert sich um:

- Deployment
- Skalierung
- Selbstheilung: Wenn ein Container abstürzt, werden neue gestartet.

## Aufbau

Kubernetes ist wie mehrere Docker Compose. In einem Pod laufen mehrere Container (wie bei Docker Compose).

## Skalierung

Kubernetes ist skalierbar: Je mehr Anfragen kommen, desto mehr [[Quarkus]]-Container werden hochgefahren.
