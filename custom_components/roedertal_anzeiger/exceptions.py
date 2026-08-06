class RoedertalError(Exception):
    """Basisfehler."""


class DownloadError(RoedertalError):
    """Download fehlgeschlagen."""


class ParseError(RoedertalError):
    """Parserfehler."""