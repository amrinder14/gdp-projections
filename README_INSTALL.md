# Top 50 Economies — iPhone PWA

## Deploy
1. Unzip the archive. Upload the **contents** of the `top_50_economies_pwa` directory to any static HTTPS host (for example Netlify Drop, Cloudflare Pages or GitHub Pages). Keep all files and `icons/` in their relative positions.
2. Open the published HTTPS site in Safari on the iPhone.
3. Tap **Share → Add to Home Screen**. If available, enable **Open as Web App** and tap **Add**.
4. Open the Home Screen icon once while connected to the internet to populate the offline cache.

## Limitations / provenance
- Works offline for the core dashboard after first successful online launch and service-worker activation. The official-source links require internet.
- Excel (.xlsx) imports currently load an external parsing library on demand, which requires internet. CSV imports function offline.
- User-selected controls and imported data are not preserved automatically after clearing or reloading the app; re-import source files as needed. CSV export is available.
- Embedded 2026 nominal GDP country anchors were characterized as October 2026 IMF WEO figures in the original dashboard. Other population, TFR, PPP, growth, inflation and FX assumptions are provisional illustrative assumptions, and long-term trajectories are extrapolations, not official IMF or UN forecasts.
- No App Store publication, device-side installation, or web hosting was performed as part of this package.


## Version 2: appearance and settings

The Settings gear in the upper right contains forecast controls, filters, exports, and data imports. Choose Light or Dark with four color schemes each. Theme preference persists on the device. Replace the existing repository files with the contents of this ZIP at the repository root, commit and push via GitHub Desktop. GitHub Pages redeploys automatically. The updated service-worker cache version ensures a refresh after deployment. If the installed iPhone icon shows an older interface, close the app completely and reopen online; if necessary remove and re-add the Home Screen icon.


## v3 update: trajectory country picker
Visible country dropdown and Add economy button, removable selected-country chips, browse-all disclosure, eight-country enforcement. Update GitHub repository files then commit and push. Refresh website; installed PWA may require closing and reopening to load the new cached version.

## v4 correction: restore all country data displays
Fixed a JavaScript variable collision in the trajectory renderer that stopped the first render and left the economy selector, browse panel, and 50-country table empty. Verified in headless Chromium: 50 table rows, 50 browse buttons, dropdown population, add/remove country, and light theme.

To update GitHub Pages, replace the repository-root files with this package, commit, and push. After GitHub Pages deploys, open the site in Safari while connected to the internet and reload. The service worker uses a new cache key. If the Home Screen app shows stale content, close it, reopen online, then retry.


## Version 5 trajectory plotting repair
Fixed three SVG horizontal coordinate calculations that incorrectly subtracted the global dataset array instead of the right margin. The malformed coordinates produced NaN paths and invisible trend lines. The service-worker cache version was incremented for deployment.


## Version 6: trajectory placement and visible status
The country picker now appears ABOVE the line chart. A live chart status counts plotted economies; the header displays `v6 · trajectory`. Verified Chromium rendering of SVG polylines and dynamic selection in a desktop/mobile viewport. After pushing, visit the GitHub Pages site in Safari first and confirm the v6 label before reopening the installed PWA.


## Version 7 — Interactive year crosshair
Move your pointer over the trajectory chart or drag a finger horizontally on the chart to move the vertical year guide. The year slider above the chart also controls the guide. The list below the chart gives the exact selected metric for every selected economy for the indicated year. Changes to countries, metric or scenario refresh the guide. The current app version is displayed as `v7 · year crosshair`.


## V8: Historical trajectories (1947–2050)
Select **Load 1960–2025 historical GDP** to retrieve World Bank annual current-USD GDP, population and PPP GDP per capita via the official World Bank API. A working internet connection is needed for first retrieval. Data are then cached locally. 1947–1959 values are intentionally missing unless sourced data are imported using the historical CSV field. Not every country is covered by the World Bank API. The forecast begins in 2026. The vertical year guide and CSV export include 1947–2050 and mark missing years clearly. Note that historical figures are nominal values of their respective years; they are not inflation-adjusted into 2026 dollars.


## V9: continuous annual 1947–2050 curves
Chart displays all 104 years continuously for selected economies. Prior to loading source data, history uses a clearly labeled *illustrative backcast* from the 2026 anchor (not historical observations). Press **Load World Bank + Maddison history** online to load nominal World Bank GDP, population and PPP observations (generally 1960 onward) plus Maddison historical real GDP-per-capita growth where available. For years preceding the earliest actual nominal GDP observation, the app rescales Maddison growth to that nominal anchor and uses a declared proxy population and 2% annual price/currency factor. Where unavailable, it applies an explicitly labeled growth fallback. This reconstructs a *continuous indicative nominal USD* history, not a 1947–1959 source-certified nominal GDP series. Tooltip labels show provenance, and the chart footer cites both sources. CSV exports carry source labels. GitHub Pages hosting required for live source retrieval; cache stored locally after loading.


## Version 10: all available economies and 1947–2100
- Load all economies using the **Load all economies (World Bank)** button while online. The app retrieves World Bank country metadata and recent GDP/population, excludes regional aggregates, and adds eligible countries or separately reported territories. Only economies with recent positive GDP and population observations are added; no unsupported claim that all UN 237 country areas have GDP forecasts. The starting built-in 50 entries remain available offline. The expanded catalog is saved locally, if device storage allows.
- The original 50 have their embedded 2026 IMF nominal GDP anchor; new countries derive a **modeled** 2026 anchor by increasing their most recent World Bank GDP observation by 4% annually to 2026, which is not an IMF forecast. Their real growth (2%), inflation (2.5%), FX loss (0.5%), fertility (2.1) and PPP multiplier (1) are provisional placeholders and must be replaced for serious comparisons.
- Projection horizon is extended to 2100. Currently, no OECD / Goldman Sachs / IIASA country-year macroeconomic series is bundled; years 2027–2100 are **illustrative scenario extrapolations**, not those institutions' reported projections. UN WPP CSV import accepts values through 2100. Historical nominal GDP can be loaded separately using the World Bank + Maddison button. Some pre-1960 backcasts are illustrative and not observed statistics.
- Local persistence stores the expanded country catalog; full World Bank historical series may exceed some devices' localStorage limits. Online loading is required to expand a fresh browser instance. GitHub Pages hosts the static files; it does not proxy World Bank API requests.
