# World Economies PWA v12 — sourced data build

This release **adds an actual data-build pipeline**. It does not bundle pre-downloaded data, because the build environment used to prepare this ZIP cannot access external data APIs. The GitHub Actions job downloads source files, validates them, normalizes country-year series, writes `data/macro_observations.json` and `data/data_audit.json`, and deploys the PWA with those data files.

## First deployment (one-time GitHub Pages change)

1. Extract this ZIP into the **root** of the existing local repository. Be sure to copy the hidden `.github` folder as well as `scripts/`, `index.html`, and the PWA assets.
2. Commit all changes in GitHub Desktop and **Push origin**.
3. Open the repository on github.com and go to **Settings → Pages → Build and deployment → Source**, and change it from **Deploy from a branch** to **GitHub Actions**.
4. Open **Actions → Build and deploy verified macro data → Run workflow → main → Run workflow**.
5. Open the latest workflow run. Confirm that the **build** and **deploy** jobs both have green checks.
6. Open the usual GitHub Pages URL. The top of the dashboard will show **Published dataset active** with country-year coverage and statuses for individual sources. Click **View data audit** for the exact counts and any download failures.
7. On iPhone, reopen the installed app while online to cache the new version. If the PWA is stale, reload the Safari website first.

Data refresh is scheduled for the first day of every month; it may also be run manually in Actions.

## What is truly integrated

- **World Bank WDI**: current-USD annual GDP, population, and PPP GDP per capita, 1960–2025, across countries/areas with records. This is required; the deployment fails if substantially incomplete.
- **UN WPP 2024**: medium-variant population and TFR, 2026–2100. Optional: a failure is recorded in the audit and does not silently become a sourced projection.
- **IMF WEO October 2026**: NGDPD nominal USD GDP (source value in USD billions), 2026–2031, if the workbook remains available and its schema is recognized. Optional, auditable.
- **Maddison Project 2023 via Our World in Data**: historical real GDP per capita (1947–2025) for pre-1960 reconstruction, not nominal USD. Optional, audited.
- **OECD 2025 long-run scenarios**: only unambiguously parsed country-year annual real-GDP-growth entries. If the supplied CSV is not an annual growth-rate series, it is **not misrepresented** as one and the audit reports unavailable. The dashboard retains its existing extrapolation model for those years.

**Very important:** Neither OECD real GDP/PPP trajectories nor UN population series are direct nominal US-dollar GDP projections. After the last official WEO observation, calculated nominal USD GDP still incorporates explicit analyst inflation and FX assumptions. Earlier than 1960, historical reconstructions are estimates, not observations. Never treat a dashed estimated line as a reported historical value.

## Technical notes

The static GitHub Pages website has no database server. The GitHub Actions data job serves as its repeatable build-time backend, producing versioned JSON files inside the deployed artifact. All files are ordinary static content and cached by the service worker. No tokens or API credentials are required for public datasets.

If an optional source fails, see `data/data_audit.json`. The PWA shows source statuses; source gaps must not be described as downloaded observations. This package was syntax-checked and browser-tested with synthetic fixtures, but real data downloads and source-format compatibility require the first GitHub Actions run.
