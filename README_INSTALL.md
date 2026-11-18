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
