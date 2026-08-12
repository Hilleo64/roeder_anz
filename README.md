# Rödertal-Anzeiger – Home Assistant

Home Assistant Custom Integration für den Rödertal-Anzeiger.

## Funktionen

- lädt die 6 neuesten PDF-Ausgaben
- stellt die Ausgaben über eine Select-Entity zur Auswahl
- legt die ausgewählte Ausgabe unter `/local/anzeiger/aktuell.pdf` ab
- kompatibel mit dem vorhandenen PDF.js-Viewer
- feuert bei einer neu heruntergeladenen Ausgabe das Event `roedertal_anzeiger_new_issue`

## HACS-Struktur

Die Integration liegt bewusst unter:

`custom_components/roedertal_anzeiger/`

Damit kann das Repository direkt als HACS Custom Repository verwendet werden.

## PDF.js-Dashboard

Die bestehende Karte kann unverändert verwendet werden:

```yaml
type: iframe
url: >-
  /local/pdfjs/web/viewer.html?file=http://10.0.0.222:8123/local/anzeiger/aktuell.pdf
aspect_ratio: 180%
```
