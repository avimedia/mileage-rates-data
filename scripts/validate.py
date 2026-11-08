"""Same rules as MileageRateFeed.validate in the app."""
import json, sys, datetime
data = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "docs/MileageRates.json"))
rates = data["rates"]
errors = []
currency = {"NO": "NOK", "SE": "SEK", "DK": "DKK"}
seen = set()
limit = datetime.date.today() + datetime.timedelta(days=366)
for r in rates:
    key = (r["region"], r["validFrom"])
    if key in seen: errors.append(f"duplicate {key}")
    seen.add(key)
    try:
        day = datetime.date.fromisoformat(r["validFrom"])
        if not (datetime.date(2000, 1, 1) <= day <= limit): errors.append(f"validFrom out of range {key}")
    except ValueError:
        errors.append(f"bad date {key}")
    if currency.get(r["region"]) != r["currencyCode"]: errors.append(f"currency {key}")
    for field in ("allowancePerKm", "deductionPerKm", "passengerPerKm", "upperTierPerKm"):
        if field in r and not (0 < r[field] < 1000): errors.append(f"{field} {key}")
    if ("upperTierFromKm" in r) != ("upperTierPerKm" in r): errors.append(f"upper tier incomplete {key}")
missing = set(currency) - {r["region"] for r in rates}
if missing: errors.append(f"missing regions {missing}")
print("\n".join(errors) or f"OK: {len(rates)} rates")
sys.exit(1 if errors else 0)
