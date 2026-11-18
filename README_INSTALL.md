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
