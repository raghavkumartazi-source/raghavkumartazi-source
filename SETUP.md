# Your terminal profile

The profile README displays `assets/terminal.svg`, generated from your public GitHub profile. The design is self-contained and uses no external stats-image services.

## Make it yours

Edit `profile.json` to change the name, tagline, focus, stack, status, and featured-project labels. Edit `README.md` to change the clickable project links or bio.

## Refresh

The **Refresh terminal profile** workflow runs daily at approximately **5:47 AM India time**, when the source changes on `main`, or manually from the Actions tab. GitHub can delay scheduled runs. It uses the repository's built-in `GITHUB_TOKEN`; no personal access token or extra secret is required.

To refresh locally with Python 3.12 or later:

```sh
python scripts/update_profile.py
```

The generator reads the public GitHub user and repository APIs plus the public contribution calendar. It excludes private repositories and forked code from language totals and does not store your token. Public repository count includes this profile repository. Stars are summed across public, non-fork repositories. Languages are weighted by GitHub's code-byte counts, not a measure of personal proficiency. Contribution totals follow the public GitHub calendar; GitHub may include anonymous private contribution counts if you enabled that setting.

The workflow writes only `assets/terminal.svg`. If the contribution calendar is unavailable, it shows **n/a** instead of inventing a count. If the GitHub API fails, the existing dashboard stays in place and the run fails visibly in Actions.

GitHub may disable scheduled workflows on public repositories after 60 days without repository activity. Re-enable the workflow in Actions if that happens.
