"""Download reference photos from Wikimedia Commons and log their licences in SOURCES.md.

Examples
  python -I fetch_refs.py --query "wakizashi blade" --query "tsuka ito" --limit 8 --out refs
  python -I fetch_refs.py --titles titles.json --out refs          # {"blade": ["File:...jpg", ...], ...}
  python -I fetch_refs.py --query "medieval lantern" --dry-run      # list matches, download nothing

Commons rate-limits fast clients (HTTP 429): requests are spaced out and retried with backoff,
existing files are skipped, and 0-byte partial files are removed so a re-run picks them up.
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

API = "https://commons.wikimedia.org/w/api.php?"
UA = {"User-Agent": "staged-3d-build-refs/1.0 (3D modelling reference collection)"}


def fetch(url, pause=2.0):
    for attempt in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                data = r.read()
            time.sleep(pause)
            return data
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("still rate-limited: " + url)


def api(params):
    return json.loads(fetch(API + urllib.parse.urlencode(dict(params, format="json"))))


def search(query, limit):
    d = api({"action": "query", "list": "search", "srnamespace": 6, "srlimit": limit, "srsearch": query})
    return [r["title"] for r in d["query"]["search"] if r["title"].lower().endswith((".jpg", ".jpeg", ".png"))]


def slug(title, i, group):
    base = re.sub(r"[^A-Za-z0-9]+", "_", os.path.splitext(title.split(":", 1)[-1])[0]).strip("_")[:60]
    return f"{group}_{i:02d}_{base}.jpg"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--query", action="append", default=[], help="Commons search (repeatable)")
    ap.add_argument("--titles", help="JSON file {group: [File titles]}")
    ap.add_argument("--limit", type=int, default=8, help="results per query")
    ap.add_argument("--width", type=int, default=2000, help="download width in px (smaller = fewer 429s)")
    ap.add_argument("--out", default="refs")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    groups = {}
    if a.titles:
        groups.update(json.load(open(a.titles, encoding="utf-8")))
    for q in a.query:
        groups[re.sub(r"[^a-z0-9]+", "_", q.lower()).strip("_")[:24]] = search(q, a.limit)
    if not groups:
        ap.error("give --query and/or --titles")

    if a.dry_run:
        for g, titles in groups.items():
            print(f"== {g}")
            for t in titles:
                print("  ", t)
        return

    os.makedirs(a.out, exist_ok=True)
    for f in os.listdir(a.out):                      # drop partial downloads from earlier runs
        p = os.path.join(a.out, f)
        if os.path.isfile(p) and os.path.getsize(p) == 0:
            os.remove(p)

    rows = []
    for g, titles in groups.items():
        for i, t in enumerate(titles, 1):
            t = t if t.startswith("File:") else "File:" + t
            page = next(iter(api({"action": "query", "titles": t, "prop": "imageinfo",
                                  "iiprop": "url|extmetadata", "iiurlwidth": a.width})["query"]["pages"].values()))
            if "imageinfo" not in page:
                print("MISSING", t)
                continue
            ii = page["imageinfo"][0]
            meta = ii.get("extmetadata", {})
            lic = meta.get("LicenseShortName", {}).get("value", "?")
            artist = re.sub("<[^>]+>", "", meta.get("Artist", {}).get("value", "?")).strip()
            out = os.path.join(a.out, slug(t, i, g))
            if not os.path.exists(out):
                try:
                    data = fetch(ii.get("thumburl") or ii["url"])
                except RuntimeError as e:
                    print("SKIP", e)
                    continue
                with open(out, "wb") as f:
                    f.write(data)
            rows.append((os.path.basename(out), t, ii["descriptionurl"], lic, artist))
            print("OK", os.path.basename(out), lic)

    src = os.path.join(a.out, "SOURCES.md")
    with open(src, "w", encoding="utf-8") as f:
        f.write("# Reference sources (Wikimedia Commons)\n\n| File | Commons title | License | Author |\n|---|---|---|---|\n")
        for name, t, url, lic, artist in rows:
            f.write(f"| {name} | [{t}]({url}) | {lic} | {artist[:60]} |\n")
    print(len(rows), "files; sources ->", src)


if __name__ == "__main__":
    sys.exit(main())
