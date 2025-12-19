import json
from typing import Dict, List
from langchain.tools import tool



# PURE PYTHON LOGIC (CALLABLE)

def search_flights_logic(source: str, destination: str) -> Dict:
    with open("data/flights.json", "r") as f:
        flights = json.load(f)

    matching_flights = [
        f for f in flights
        if f.get("from", "").lower() == source.lower()
        and f.get("to", "").lower() == destination.lower()
    ]

    if not matching_flights:
        return {"message": "No flights found"}

    best_flight = min(matching_flights, key=lambda x: x["price"])

    return {
        "flight_id": best_flight["flight_id"],
        "airline": best_flight["airline"],
        "price": best_flight["price"],
        "departure_time": best_flight["departure_time"],
        "arrival_time": best_flight["arrival_time"]
    }


# LANGCHAIN TOOL (AGENT USES THIS)

@tool
def flight_search(source: str, destination: str) -> Dict:
    """Find the cheapest flight between two cities"""
    return search_flights_logic(source, destination)


# LOCAL TEST (NO LANGCHAIN CALL)

if __name__ == "__main__":
    print(search_flights_logic("Hyderabad", "Delhi"))
