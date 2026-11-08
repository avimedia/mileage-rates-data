# mileage-rates-data

Official mileage rates (kilometergodtgjørelse) for Norway, Sweden and Denmark, published as JSON
for the Timely Pro app's in-app rate update.

Served via GitHub Pages from `/docs`:
- `docs/MileageRates.json`: every rate with the day it takes effect (`validFrom`) and its official source.

The app ships with the same file built in and only uses a downloaded copy after strict validation
(all regions present, positive amounts, real dates, no duplicates). Trips keep the rate they were
saved with, so a change here only affects new trips.

## Updating (usually December/January)

1. Find the new rates: Skatteetaten (NO), Skatteverket (SE), Skat (DK). The `check-sources` workflow
   opens an issue when a source page mentions next year and the file has no entry for it yet.
2. Add one entry per region with `validFrom` = the first day it applies. Never edit or remove old
   entries; earlier trips still look them up.
3. Push. The `validate` workflow checks the file; apps pick it up within a day.
4. Copy the file into the app (`Timely Pro/Services/MileageRates/MileageRates.json`) for the next release.

## Disclaimer

Unofficial, independently maintained copy of rates published by the tax authorities. Not affiliated
with Skatteetaten, Skatteverket or Skattestyrelsen. Verify against the official sources linked in each
entry. Provided "as is", without warranty.
