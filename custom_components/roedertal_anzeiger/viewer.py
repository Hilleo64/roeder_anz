"""HTTP viewer for the selected Rödertal-Anzeiger PDF."""

from __future__ import annotations

from aiohttp import web
from homeassistant.components.http import HomeAssistantView


class RoedertalViewerView(HomeAssistantView):
    """A small wrapper around the existing PDF.js viewer.

    The wrapper keeps the existing PDF.js setup but reloads the PDF with a
    cache-busting query parameter whenever the selected local PDF changes.
    No Home Assistant API authentication is required because this page only
    serves the public local PDF path already used by the dashboard.
    """

    url = "/api/roedertal_anzeiger/viewer"
    name = "api:roedertal_anzeiger:viewer"
    requires_auth = False

    async def get(self, request: web.Request) -> web.Response:
        html = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>html,body{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#fff}iframe{border:0;width:100%;height:100%;display:block}</style>
</head><body>
<iframe id="pdf" title="Rödertal-Anzeiger"></iframe>
<script>
const pdf = document.getElementById('pdf');
let lastUrl = null;
let lastStamp = null;
function loadPdf(stamp) {
  const url = '/local/anzeiger/aktuell.pdf?v=' + encodeURIComponent(stamp);
  if (url === lastUrl) return;
  lastUrl = url;
  pdf.src = '/local/pdfjs/web/viewer.html?file=' + encodeURIComponent(url);
}
async function check() {
  try {
    const r = await fetch('/local/anzeiger/aktuell.pdf?check=' + Date.now(), {cache:'no-store'});
    if (!r.ok) return;
    const stamp = r.headers.get('last-modified') || r.headers.get('etag') || String(r.headers.get('content-length') || '') + ':' + String(Date.now() / 5000 | 0);
    if (stamp !== lastStamp) {
      lastStamp = stamp;
      loadPdf(stamp);
    }
  } catch (e) {}
}
check();
setInterval(check, 2000);
</script></body></html>"""
        return web.Response(text=html, content_type="text/html", headers={"Cache-Control": "no-store"})


def register_views(hass) -> None:
    """Register the viewer once per Home Assistant instance.

    HomeAssistantHTTP does not expose a public ``views`` collection, so we
    keep our own registration flag in ``hass.data`` instead of inspecting
    private HTTP internals.
    """
    key = "roedertal_anzeiger_viewer_registered"
    if hass.data.get(key):
        return
    hass.http.register_view(RoedertalViewerView())
    hass.data[key] = True
