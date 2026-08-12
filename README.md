# Rödertal-Anzeiger für Home Assistant

Die Integration lädt die sechs neuesten PDF-Ausgaben des Rödertal-Anzeigers in das Home-Assistant-Verzeichnis `www/anzeiger/archiv/`.

## Lesen im Dashboard

Die Integration stellt die Select-Entity `Ausgabe zum Lesen` bereit. Nach der Auswahl wird die PDF unter `/local/anzeiger/auswahl.pdf` bereitgestellt.

Füge im Lovelace-Dashboard eine Webpage-/Iframe-Karte hinzu:

```yaml
type: iframe
url: /local/anzeiger/auswahl.pdf
aspect_ratio: 70%
```

Damit kann die ausgewählte Ausgabe direkt im Home-Assistant-Dashboard gelesen werden.

## Push-Benachrichtigung

Bei einer neu heruntergeladenen Ausgabe wird weiterhin das Event `roedertal_anzeiger_new_issue` ausgelöst. Beim ersten Start werden die sechs vorhandenen Ausgaben nachgeladen, ohne sechs Benachrichtigungen auszulösen.
