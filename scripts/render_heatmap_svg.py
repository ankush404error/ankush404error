import json
from pathlib import Path
from datetime import date
from xml.sax.saxutils import escape

days = json.loads(Path("data/contributions.json").read_text(encoding="utf-8"))
palette = ["#182033", "#0e4429", "#006d32", "#26a641", "#39d353"]
# GitHub's calendar spans 53 columns. Align by weekday and pad as needed.
days = sorted(days, key=lambda d: d["date"])
if not days:
    raise RuntimeError("No contribution data available")
first = date.fromisoformat(days[0]["date"])
offset = first.weekday()  # Monday-first
cells = []
for i, item in enumerate(days[-371:]):
    d = date.fromisoformat(item["date"])
    index = i + max(0, offset)
    col, row = index // 7, index % 7
    if col >= 53: col = 52
    level = max(0, min(4, int(item.get("level", 0))))
    x, y = 22 + col * 16, 42 + row * 14
    cells.append(f'<rect x="{x}" y="{y}" width="11" height="10" rx="2" fill="{palette[level]}"><title>{escape(item["date"])} · level {level}</title><animate attributeName="opacity" values="0.25;1" dur="0.7s" begin="{(col*7+row)*0.001:.3f}s" fill="freeze"/></rect>')
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="155" viewBox="0 0 900 155">',
'<rect width="900" height="155" rx="12" fill="#0b1020"/><rect x="1" y="1" width="898" height="153" rx="12" fill="none" stroke="#29334d"/>',
'<text x="22" y="27" fill="#c7d2e7" font-family="monospace" font-size="13">PUBLIC CONTRIBUTION CALENDAR · LAST 53 WEEKS</text>', *cells,
'<text x="22" y="150" fill="#7d8ba8" font-family="monospace" font-size="10">LESS</text>']
for i, c in enumerate(palette):
    svg.append(f'<rect x="{62+i*16}" y="141" width="11" height="9" rx="2" fill="{c}"/>')
svg += ['<text x="155" y="150" fill="#7d8ba8" font-family="monospace" font-size="10">MORE · Data from GitHub public contribution calendar</text>', '</svg>']
Path("assets/contrib-heatmap.svg").write_text("\n".join(svg), encoding="utf-8")
print("Rendered assets/contrib-heatmap.svg")
