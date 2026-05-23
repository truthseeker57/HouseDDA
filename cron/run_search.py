from search.sources.zillow import fetch_listings

def run_search():
    listings = fetch_listings()
    condensed = condense_listings(listings)
    for listing in condensed:
        print()
        print(listing)
        print()

def condense_listings(listings):
    result = []
    for listing in listings:
        if listing["homeStatus"] == "FOR_SALE" and listing["price"] != 0:
            result.append({
                "address": listing["address"],
                "price": listing["price"],
                "bedrooms": listing["bedrooms"],
                "bathrooms": listing["bathrooms"],
                "type": listing["homeType"],
                "hours_since": listing["flexFieldText"],
                "details": listing["detailUrl"],
                "img": listing["imgSrc"],
            })
    return result

if __name__ == "__main__":
    run_search()