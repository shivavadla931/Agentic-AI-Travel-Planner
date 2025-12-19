import json
from typing import List, Dict
from langchain.tools import tool


# PURE PYTHON LOGIC

def discover_places_logic(city: str, top_n: int = 5) -> List[Dict]:
    with open("data/places.json", "r") as f:
        places = json.load(f)

    matching_places = [
        p for p in places
        if p.get("city", "").lower() == city.lower()
    ]

    if not matching_places:
        return [{"message": "No places found"}]

    # Sort by rating (high → low)
    sorted_places = sorted(
        matching_places,
        key=lambda x: x.get("rating", 0),
        reverse=True
    )

    return [
        {
            "place_id": p.get("place_id"),
            "place_name": p.get("name"),
            "type": p.get("type"),
            "rating": p.get("rating")
        }
        for p in sorted_places[:top_n]
    ]

# LANGCHAIN TOOL

@tool
def discover_places(city: str, top_n: int = 5) -> List[Dict]:
    """Discover top tourist attractions in a given city"""
    return discover_places_logic(city, top_n)


# LOCAL TEST

if __name__ == "__main__":
    print(discover_places_logic("Delhi", 3))
