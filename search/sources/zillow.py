import httpx
from config import RAPIDAPI_KEY



def fetch_listings():
    url = "https://unofficial-zillow-api2.p.rapidapi.com/search/address"
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "unofficial-zillow-api2.p.rapidapi.com",
        "Content-Type": "application/json"
        }
    
    payload = {
        "location": "Rock Island, IL",
        "min_beds": 2,
        "max_beds": 3,
        "min_baths": 1,
        "max_baths": 2,
        "max_price": 85000,
        "status": "for_sale"
    }
    
    
    response = httpx.post(url, json=payload, headers=headers)
    data = response.json()
    
    return data.get("listings", [])
    
    