#!/usr/bin/env python3
"""Refresh cosmic profile artwork using only public GitHub data."""

import argparse
import datetime as dt
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


def request(url, *, authenticated=True):
    headers = {"User-Agent": "cosmic-github-profile", "Accept": "application/vnd.github+json"}
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


from design import render_assets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, help="Render a saved snapshot without network access")
    parser.add_argument("--snapshot", type=Path, help="Save collected public data for local verification")
    args = parser.parse_args()
    config = json.loads((ROOT / "profile.json").read_text())
    data = json.loads(args.data.read_text()) if args.data else collect(config["username"])
    if args.snapshot:
        args.snapshot.write_text(json.dumps(data, indent=2) + "\n")
    target = ROOT / "assets"
    target.mkdir(exist_ok=True)
    assets = render_assets(data, config)
    for name, content in assets.items():
        (target / name).write_text(content)
    print(f"Generated {len(assets)} cosmic profile assets from public GitHub data")


if __name__ == "__main__":
    main()
