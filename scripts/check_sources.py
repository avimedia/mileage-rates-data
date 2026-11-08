"""Prints regions whose official page mentions next year while the feed has no entry for it."""
import json, urllib.request, datetime, re
next_year = datetime.date.today().year + 1
rates = json.load(open("docs/MileageRates.json"))["rates"]
latest = {}
for r in rates:
    latest[r["region"]] = max(latest.get(r["region"], ""), r["validFrom"])
pages = {"NO": "https://www.skatteetaten.no/satser/bilgodtgjorelse-kilometergodtgjorelse/",
         # Skatteverket publishes one page per year; it existing at all is the signal.
         "SE": f"https://www.skatteverket.se/privat/skatter/beloppochprocent/{next_year}",
         "DK": "https://skat.dk/en-us/businesses/employees-and-pay/transport-allowance/taxable-and-tax-free-transport-allowance"}
for region, url in pages.items():
    if latest.get(region, "") >= f"{next_year}-01-01":
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "mileage-rates-data checker"})
        text = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    except Exception as error:
        if region != "SE":  # For Sweden a missing page just means next year isn't out yet.
            print(f"{region}: could not fetch {url} ({error}); the page may have moved")
        continue
    if re.search(rf"\b{next_year}\b", text):
        print(f"{region}: {url} mentions {next_year}, but the feed has no {next_year} entry")
