import json, re, urllib.request
from html.parser import HTMLParser
from pathlib import Path

USERNAME = "ankush404error"
URL = f"https://github.com/users/{USERNAME}/contributions"

class ContributionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "td" and "ContributionCalendar-day" in a.get("class", ""):
            level = re.search(r"data-level=\"?(\d)", a.get("data-level", ""))
            # data-level is normally a separate attribute; class is used as fallback.
            val = a.get("data-level", "0")
            try: val = int(val)
            except ValueError: val = 0
            date = a.get("data-date", "")
            if date: self.days.append({"date": date, "level": val})

req = urllib.request.Request(URL, headers={"User-Agent": "ankush-profile-readme/1.0"})
with urllib.request.urlopen(req, timeout=30) as response:
    html = response.read().decode("utf-8", errors="replace")
parser = ContributionParser()
parser.feed(html)
# Fail rather than silently publishing a fake graph if GitHub changes its markup.
if len(parser.days) < 300:
    raise RuntimeError(f"Expected contribution calendar data, found {len(parser.days)} days. Check GitHub's public HTML markup.")
Path("data").mkdir(exist_ok=True)
Path("data/contributions.json").write_text(json.dumps(parser.days, indent=2), encoding="utf-8")
print(f"Saved {len(parser.days)} contribution days.")
