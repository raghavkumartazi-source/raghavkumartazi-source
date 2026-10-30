# Cosmic profile

An animated, self-contained SVG portfolio for the GitHub profile. The hero uses an original ringed planet illustration, large lettering, and a violet/peach palette. Three illustrated project cards link to public repositories. Statistics live inside an optional details section.

## Customize

- `README.md`: bio, interests, links, and section order.
- `profile.json`: name and project-card titles, descriptions, categories, and stacks. Keep mobile copy short enough for the separate phone layouts.
- `scripts/design.py`: typography, colors, illustration, and SVG animation. The hero name lettering and campus line are art-directed here; update them alongside the config if reusing this design for someone else.
- `scripts/update_profile.py`: public GitHub data collection and asset generation.

The ten generated images live in `assets/`. Each image has desktop and phone layouts; the README selects phone layouts below a 640px viewport width. Native SVG animations respect `prefers-reduced-motion`. All image assets are stored in this repository; no external stats-image host, font, script, or tracker is required.

## Refresh

The **Refresh cosmic profile** workflow runs daily at approximately **5:47 AM India time**, when its source changes on `main`, or manually from Actions. GitHub can delay scheduled runs. It uses the built-in `GITHUB_TOKEN`; no additional secret is required.

With Python 3.12 or later:

```sh
python scripts/update_profile.py
```

For a repeatable local preview:

```sh
python scripts/update_profile.py --snapshot /tmp/profile-data.json
python scripts/update_profile.py --data /tmp/profile-data.json
```

The generator reads the public user/repository APIs and contribution calendar. Private repositories are excluded. Stars count public, non-fork repositories. Languages exclude forks and this profile repository, and measure code bytes rather than proficiency. Contribution totals reflect GitHub's public calendar, including anonymous private counts if enabled. The recent-activity grid covers 16 calendar weeks.

Unavailable contribution data displays as **n/a**, never as invented activity. If a required API request fails, the workflow fails without committing replacements. The token is never written to an asset. GitHub may disable scheduled workflows on inactive public repositories after 60 days; re-enable the workflow in Actions if needed.
