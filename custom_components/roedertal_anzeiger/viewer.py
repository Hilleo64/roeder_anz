"""HTTP viewer for the selected Rödertal-Anzeiger PDF."""

from __future__ import annotations

from aiohttp import web
from homeassistant.components.http import HomeAssistantView

from .const import DOMAIN


class RoedertalViewerView(HomeAssistantView):
    """Serve a small page that keeps the PDF.js viewer in sync with the select entity."""

    url = "/api/roedertal_anzeiger/viewer"
    name = "api:roedertal_anzeiger:viewer"
    requires_auth = True

    async def get(self, request: web.Request) -> web.Response:
        html = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#fff}iframe{border:0;width:100%;height:100%;display:block}</style>
</head><body>
<iframe id="pdf" title="Rödertal-Anzeiger"></iframe>
<script>
const pdf = document.getElementById('pdf');
let last = null;
async function update() {
  try {
    const r = await fetch('/api/roedertal_anzeiger/selected', {cache:'no-store'});
    if (!r.ok) return;
    const d = await r.json();
    if (!d.filename) return;
    if (d.filename !== last) {
      last = d.filename;
      pdf.src = '/local/pdfjs/web/viewer.html?file=' + encodeURIComponent(d.url) + '&v=' + encodeURIComponent(d.version);
    }
  } catch (e) {}
}
update();
setInterval(update, 1000);
</script></body></html>"""
        return web.Response(text=html, content_type="text/html", headers={"Cache-Control": "no-store"})


class RoedertalSelectedView(HomeAssistantView):
    """Return the currently selected local PDF."""

    url = "/api/roedertal_anzeiger/selected"
    name = "api:roedertal_anzeiger:selected"
    requires_auth = True

    async def get(self, request: web.Request) -> web.Response:
        hass = request.app["hass"]
        coordinators = hass.data.get(DOMAIN, {})
        coordinator = next(iter(coordinators.values()), None)
        if coordinator is None or not coordinator.data:
            return web.json_response({"filename": None, "url": None, "version": 0})
        data = coordinator.data
        return web.json_response({
            "filename": data.get("selected_filename"),
            "url": "/local/anzeiger/aktuell.pdf",
            "version": data.get("selected_version", 0),
        }, headers={"Cache-Control": "no-store"})


def register_views(hass) -> None:
    hass.http.register_view(RoedertalViewerView())
    hass.http.register_view(RoedertalSelectedView())
