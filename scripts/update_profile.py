#!/usr/bin/env python3
"""Render a terminal profile from public GitHub data using the standard library."""

import argparse
import datetime as dt
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.request
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
GREEN = "#39f5a4"
CYAN = "#63d8f2"
MUTED = "#7e949c"
WHITE = "#e4eff2"
COLORS = {"TypeScript": "#66aaff", "JavaScript": "#f3d96b", "HTML": "#ff9671", "Kotlin": "#bc90ff", "CSS": "#6ed6df", "Other": "#78939b"}


def request(url, *, authenticated=True):
    headers = {"User-Agent": "terminal-github-profile", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and authenticated:
        headers["Authorization"] = f"Bearer {token}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
                return response.read().decode("utf-8")
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def api(path):
    return json.loads(request("https://api.github.com" + path))


class ContributionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-date" in attrs and "data-level" in attrs:
            self.days.append({"date": attrs["data-date"], "level": int(attrs["data-level"])})

    def handle_data(self, data):
        self.text.append(data)


def collect(username):
    user = api(f"/users/{username}")
    repos = []
    page = 1
    while True:
        batch = api(f"/users/{username}/repos?type=owner&per_page=100&page={page}")
        repos.extend(repo for repo in batch if not repo.get("private"))
        if len(batch) < 100:
            break
        page += 1
    languages = {}
    for repo in repos:
        if repo["fork"] or repo["name"].lower() == username.lower():
            continue
        for language, size in api(f"/repos/{repo['full_name']}/languages").items():
            languages[language] = languages.get(language, 0) + size
    parser = ContributionParser()
    contributions = None
    try:
        parser.feed(request(f"https://github.com/users/{username}/contributions", authenticated=False))
        match = re.search(r"([\d,]+)\s+contributions?\s+in the last year", " ".join(parser.text))
        if match:
            contributions = int(match.group(1).replace(",", ""))
    except (urllib.error.URLError, TimeoutError, ValueError):
        # An unavailable public graph must never appear as zero activity.
        parser.days = []
    return {
        "user": {key: user[key] for key in ["login", "name", "bio", "public_repos", "followers", "following", "created_at"]},
        "repos": [{key: repo[key] for key in ["name", "stargazers_count", "forks_count", "fork", "private"]} for repo in repos],
        "languages": languages, "contributions": contributions, "days": parser.days,
        "updated": dt.datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M IST"),
    }


def render(data, config):
    parts = []
    def add(value):
        parts.append(value)
    def rect(x, y, w, h, fill, stroke=None, radius=0):
        border = f' stroke="{stroke}"' if stroke else ""
        add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"{border}/>')
    def text(x, y, value, fill=WHITE, size=18, weight=400, anchor="start"):
        add(f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{html.escape(str(value))}</text>')
    def line(x1, y1, x2, y2, color="#20353c"):
        add(f'<path d="M{x1} {y1}H{x2}" stroke="{color}"/>' if y1 == y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}"/>')
    def command(y, value):
        text(42, y, "❯", GREEN, 20, 700)
        text(70, y, value, WHITE, 19)

    user = data["user"]
    username = user["login"]
    add('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1150" viewBox="0 0 1200 1150" role="img" aria-labelledby="title desc">')
    add(f'<title id="title">{html.escape(config["name"])} — terminal GitHub profile</title>')
    add('<desc id="desc">Terminal dashboard with profile information, public GitHub statistics, repository language distribution, contribution activity, and featured projects.</desc>')
    add('<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#09171d"/><stop offset="1" stop-color="#080e13"/></linearGradient><linearGradient id="art" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#39f5a4"/><stop offset="1" stop-color="#63d8f2"/></linearGradient></defs>')
    add('<g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, Liberation Mono, monospace">')
    rect(1, 1, 1198, 1148, "url(#bg)", "#29444c", 18)
    rect(2, 2, 1196, 60, "#111d24", radius=17)
    rect(2, 35, 1196, 27, "#111d24")
    for x, color in [(32,"#ff6371"),(56,"#ffc866"),(80,GREEN)]:
        add(f'<circle cx="{x}" cy="32" r="7" fill="{color}"/>')
    text(110, 38, f"{username} / README.md", MUTED, 15)
    rect(1030, 20, 137, 26, "#112a23", "#215941", 13)
    text(1098, 38, "●  PUBLIC", GREEN, 12, 600, "middle")
    command(105, "neofetch --profile")

    # Original pixel monogram: a local SVG asset with no remote image dependencies.
    rect(32, 129, 358, 336, "#0c1a20", "#26444d", 10)
    text(55, 160, "IDENTITY.SYS", MUTED, 13)
    text(367, 160, "01", GREEN, 13, anchor="end")
    patterns = [
        "111110  100001", "100001  100010", "100001  100100",
        "111110  111000", "101000  100100", "100100  100010", "100010  100001",
    ]
    for row, pattern in enumerate(patterns):
        for column, cell in enumerate(pattern):
            if cell == "1":
                rect(61 + column * 23, 198 + row * 23, 17, 17, "url(#art)", radius=2)
    line(55, 389, 367, 389)
    text(211, 416, "RAGHAV // BUILDER", GREEN, 16, 700, "middle")
    text(211, 441, "learn · build · iterate", MUTED, 14, anchor="middle")

    rect(410, 129, 758, 336, "#0b171e", "#26444d", 10)
    text(436, 161, "system.info", CYAN, 16, 600)
    text(1142, 161, "[ ok ]", GREEN, 14, anchor="end")
    line(436, 178, 1142, 178)
    text(436, 221, config["name"], WHITE, 30, 700)
    text(436, 248, config["tagline"], MUTED, 16)
    campus = "IIT Varanasi" if (user.get("bio") or "").lower() == "iit varanasi" else user.get("bio") or "GitHub"
    fields = [("HANDLE", "@" + username), ("CAMPUS", campus), ("FOCUS", config["focus"]), ("STACK", config["stack"]), ("STATUS", config["status"])]
    for i, (key, value) in enumerate(fields):
        y = 289 + i * 33
        text(436, y, key, MUTED, 13)
        text(552, y, value, GREEN if key == "STATUS" else WHITE, 17)

    command(511, "gh stats --public")
    metrics = [("PUBLIC REPOS", user["public_repos"], GREEN), ("STARS", sum(r["stargazers_count"] for r in data["repos"] if not r["fork"]), CYAN), ("CONTRIBUTIONS / YEAR", data.get("contributions"), "#bd9aff"), ("FOLLOWERS", user["followers"], GREEN)]
    for i, (label, value, color) in enumerate(metrics):
        x = 32 + i * 289
        rect(x, 532, 269, 109, "#0d1c23", "#26444d", 8)
        text(x+20, 559, label, MUTED, 12)
        text(x+20, 605, f"{value:,}" if value is not None else "n/a", color, 35, 700)
        line(x+20, 624, x+249, 624, "#1e343c")
        line(x+20, 624, x+88, 624, color)

    rect(32, 665, 557, 255, "#0b171e", "#26444d", 10)
    rect(609, 665, 559, 255, "#0b171e", "#26444d", 10)
    text(55, 699, "❯ stack --languages", WHITE, 18, 600)
    text(55, 723, "Code bytes across public source repositories", MUTED, 12)
    langs = sorted(data["languages"].items(), key=lambda item: item[1], reverse=True)
    top = langs[:5]
    if len(langs) > 5:
        top.append(("Other", sum(value for _, value in langs[5:])))
    total = sum(data["languages"].values())
    for i, (name, count) in enumerate(top):
        y = 751 + i * 26
        color = COLORS.get(name, CYAN)
        add(f'<circle cx="59" cy="{y-5}" r="4" fill="{color}"/>')
        text(73, y, name, WHITE, 14)
        rect(195, y-11, 289, 8, "#192c34", radius=4)
        rect(195, y-11, round(289 * count / total, 2) if total else 0, 8, color, radius=4)
        text(565, y, f"{count/total*100:.1f}%" if total else "0%", color, 13, anchor="end")
    if not top:
        text(55, 774, "No public language data yet.", MUTED, 14)

    text(632, 699, "❯ activity --recent", WHITE, 18, 600)
    text(632, 723, "Last 16 weeks · public GitHub calendar", MUTED, 12)
    days = sorted(data.get("days", []), key=lambda day: day["date"])
    today = dt.date.fromisoformat(data["updated"][:10])
    cutoff = today - dt.timedelta(days=105 + (today.weekday()+1) % 7)
    recent = [day for day in days if cutoff.isoformat() <= day["date"] <= today.isoformat()]
    palette = ["#172c32", "#14543e", "#1c8656", "#22bd76", GREEN]
    if recent:
        first = dt.date.fromisoformat(recent[0]["date"])
        for day in recent:
            date = dt.date.fromisoformat(day["date"])
            n = (date-first).days
            col, row = divmod(n, 7)
            rect(642 + col*29, 750 + row*18, 22, 12, palette[min(day["level"], 4)], radius=2)
        text(632, 901, "less", MUTED, 12)
        for i, color in enumerate(palette):
            rect(676+i*18, 890, 12, 12, color, radius=2)
        text(776, 901, "more", MUTED, 12)
    else:
        text(632, 786, "Public activity temporarily unavailable.", MUTED, 14)

    command(965, "ls ~/featured-projects")
    for i, project in enumerate(config["projects"]):
        y = 1001 + i*31
        text(55, y, f"0{i+1}", GREEN, 14)
        text(94, y, project["name"], WHITE, 16, 600)
        text(539, y, project["summary"], MUTED, 14)
    line(32, 1090, 1168, 1090)
    text(42, 1123, "❯ keep learning. keep shipping.", GREEN, 14)
    text(1158, 1123, "updated " + data["updated"], MUTED, 12, anchor="end")
    add("</g></svg>\n")
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, help="Render a saved snapshot without network access")
    parser.add_argument("--snapshot", type=Path, help="Save collected public data for local verification")
    args = parser.parse_args()
    config = json.loads((ROOT / "profile.json").read_text())
    data = json.loads(args.data.read_text()) if args.data else collect(config["username"])
    if args.snapshot:
        args.snapshot.write_text(json.dumps(data, indent=2) + "\n")
    target = ROOT / "assets" / "terminal.svg"
    target.parent.mkdir(exist_ok=True)
    target.write_text(render(data, config))
    print(f"Generated {target.name} from public GitHub data")


if __name__ == "__main__":
    main()
