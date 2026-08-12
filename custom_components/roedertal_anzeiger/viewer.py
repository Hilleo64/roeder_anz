"""HTTP viewer for the selected Rödertal-Anzeiger PDF."""

from __future__ import annotations

from aiohttp import web
from homeassistant.components.http import HomeAssistantView


class RoedertalViewerView(HomeAssistantView):
    """Serve a small wrapper that embeds the existing PDF.js viewer.

    The PDF.js URL deliberately mirrors the URL that worked in the user's
    existing dashboard.  The wrapper only adds cache busting when
    ``aktuell.pdf`` changes after selecting another issue.
    """

    url = "/api/roedertal_anzeiger/viewer"
    name = "api:roedertal_anzeiger:viewer"
    requires_auth = False

    async def get(self, request: web.Request) -> web.Response:
        origin = f"{request.scheme}://{request.host}"
        pdf_url = f"{origin}/local/anzeiger/aktuell.pdf"
        pdf_js_url = f"{origin}/local/pdfjs/web/viewer.html"

        # encodeURI keeps : and / intact.  This is important for older/custom
        # PDF.js builds which expect the same file URL format as the original
        # dashboard card.
        import json
        pdf_url_js = json.dumps(pdf_url)
        pdf_js_url_js = json.dumps(pdf_js_url)

        html = f"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>html,body{{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#fff}}iframe{{border:0;width:100%;height:100%;display:block}}</style>
</head><body>
<iframe id="pdf" title="Rödertal-Anzeiger"></iframe>
<script>
const pdf = document.getElementById('pdf');
const pdfBase = {pdf_url_js};
const viewerBase = {pdf_js_url_js};
let lastStamp = null;
let firstLoad = true;
function loadPdf(stamp) {{
  // Keep the same PDF.js URL structure as the user's working dashboard.
  const file = pdfBase + '?v=' + encodeURIComponent(stamp);
  pdf.src = viewerBase + '?file=' + encodeURI(file);
}}
async function check() {{
  try {{
    const r = await fetch(pdfBase + '?check=' + Date.now(), {{cache:'no-store'}});
    if (!r.ok) return;
    const stamp = r.headers.get('last-modified') || r.headers.get('etag') ||
      String(r.headers.get('content-length') || '') + ':' + String(Date.now() / 5000 | 0);
    if (firstLoad || stamp !== lastStamp) {{
      firstLoad = false;
      lastStamp = stamp;
      loadPdf(stamp);
    }}
  }} catch (e) {{
    console.debug('Rödertal-Anzeiger viewer check failed', e);
  }}
}}
check();
setInterval(check, 1500);
</script></body></html>"""
        return web.Response(
            text=html,
            content_type="text/html",
            headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
        )


def register_views(hass) -> None:
    """Register the viewer once per Home Assistant instance."""
    key = "roedertal_anzeiger_viewer_registered"
    if hass.data.get(key):
        return
    hass.http.register_view(RoedertalViewerView())
    hass.data[key] = True
