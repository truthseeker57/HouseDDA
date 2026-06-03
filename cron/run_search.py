import math
from search.sources.zillow import fetch_listings
from ai.scorer import score_listings
from db.database import init_db, get_last_price, upsert_listing

AUGUSTANA_LAT = 41.50302625752872
AUGUSTANA_LNG = -90.55139102323895
PRICE_DROP_THRESHOLD = 0.95

CRITERIA = {
    "bedrooms_preferred": 3,
    "bedrooms_min": 2,
    "bathrooms_preferred": 2,
    "bathrooms_min": 1,
    "max_price": 85000,
    "max_distance_miles": 0.6,
    "condition": "move-in ready or minor cosmetic work only"
}

def distance_from_augustana(lat, lng):
    R = 3958.8
    lat1 = math.radians(AUGUSTANA_LAT)
    lat2 = math.radians(lat)
    dlat = math.radians(lat - AUGUSTANA_LAT)
    dlng = math.radians(lng - AUGUSTANA_LNG)
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def condense_listings(listings):
    result = []
    for listing in listings:
        if (listing["homeStatus"] == "FOR_SALE"
            and listing["price"] != 0
            and listing["homeType"] == "SINGLE_FAMILY"):
            distance = distance_from_augustana(listing["latitude"], listing["longitude"])
            if distance <= CRITERIA["max_distance_miles"]:
                result.append({
                    "zpid": listing["zpid"],
                    "address": listing["address"],
                    "price": listing["price"],
                    "bedrooms": listing["bedrooms"],
                    "bathrooms": listing["bathrooms"],
                    "living_area_sqft": listing["livingArea"],
                    "days_on_zillow": listing["daysOnZillow"],
                    "price_change": listing["priceChange"],
                    "zestimate": listing["zestimate"],
                    "tax_assessed_value": listing["taxAssessedValue"],
                    "status_text": listing["statusText"],
                    "flex_field": listing["flexFieldText"],
                    "distance_miles": round(distance, 2),
                    "details": listing["detailUrl"],
                    "img": listing["imgSrc"],
                })
    return result

def run_search():
    init_db()
    listings = fetch_listings()
    condensed = condense_listings(listings)
        
        
    new_or_dropped = []
    
    for listing in condensed:
        zpid = listing["zpid"]
        price = listing["price"]
        
        last_price = get_last_price(zpid)
        
        if last_price is None or last_price * PRICE_DROP_THRESHOLD >= price:
            new_or_dropped.append(listing)
            
    scored = score_listings(new_or_dropped, CRITERIA)
    
    for listing in scored:
        print()
        print(listing)
        print()
    
    for listing in new_or_dropped:
        upsert_listing(listing["zpid"], listing["price"])
                        

if __name__ == "__main__":
    run_search()