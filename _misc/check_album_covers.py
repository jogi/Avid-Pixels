"""Check built cover URLs before deployment, including responsive candidates."""

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class CoverParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.covers = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img" and "album-thumbnail" in attrs.get("class", "").split():
            self.covers.append(attrs)


def check(build):
    for page in ("index.html", "albums/index.html"):
        parser = CoverParser()
        parser.feed((build / page).read_text(encoding="utf-8"))
        if not parser.covers:
            raise ValueError(f"{page}: no album covers found")
        for cover in parser.covers:
            urls = [cover["src"]]
            urls.extend(candidate.strip().split()[0]
                        for candidate in cover.get("srcset", "").split(",")
                        if candidate.strip())
            for url in urls:
                parsed = urlsplit(url)
                if parsed.scheme or parsed.netloc or not parsed.path.startswith("/"):
                    raise ValueError(f"{page}: cover URL must be site-relative: {url}")
                if not (build / unquote(parsed.path).lstrip("/")).is_file():
                    raise ValueError(f"{page}: missing cover file: {url}")
        print(f"{page}: {len(parser.covers)} covers checked")


if __name__ == "__main__":
    check(Path(sys.argv[1] if len(sys.argv) > 1 else "public"))
