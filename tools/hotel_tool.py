import json
from typing import Dict, List
from langchain.tools import tool


# PURE PYTHON LOGIC

def recommend_hotel_logic(city: str, max_price: int = 5000) -> Dict:
    with open("data/hotels.json", "r") as f:
        hotels = json.load(f)

    matching_hotels = [
        h for h in hotels
        if h.get("city", "").lower() == city.lower()
        and h.get("price_per_night", 0) <= max_price
    ]

    if not matching_hotels:
        return {"message": "No hotels found"}

    # Sort by rating (high → low), price (low → high)
    best_hotel = sorted(
        matching_hotels,
        key=lambda x: (-x.get("rating", 0), x.get("price_per_night", 0))
    )[0]
 
    return {
    "hotel_id": best_hotel.get("hotel_id"),
    "hotel_name": best_hotel.get("name"),
    "city": best_hotel.get("city"),
    "stars": best_hotel.get("stars"),
    "price_per_night": best_hotel.get("price_per_night"),
    "amenities": best_hotel.get("amenities")
}

# LANGCHAIN TOOL

@tool
def hotel_recommendation(city: str, max_price: int = 5000) -> Dict:
    """Recommend the best hotel based on city, rating, and budget"""
    return recommend_hotel_logic(city, max_price)

# LOCAL TEST

if __name__ == "__main__":
    print(recommend_hotel_logic("Delhi", 4000))
