import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

from tools.flight_tool import search_flights_logic
from tools.hotel_tool import recommend_hotel_logic
from tools.places_tool import discover_places_logic
from tools.weather_tool import get_weather_logic
from tools.budget_tool import estimate_budget_logic

# ---------------------------------------
# LLM (optional – kept for future use)
# ---------------------------------------
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)


def run_travel_agent(source, destination, days):

    # ---------------- FLIGHT ----------------
    flight = search_flights_logic(source, destination)

    if not flight or "price" not in flight:
        return f"No flight data available for route {source} → {destination}"

    # ---------------- HOTEL ----------------
    hotel = recommend_hotel_logic(destination, max_price=6000)

    # ---------------- PLACES ----------------
    places = discover_places_logic(destination, top_n=10)

    # ---------------- WEATHER ----------------
    weather = get_weather_logic(destination)
    daily_weather = weather.get("daily_weather", [])

    # ---------------- BUDGET ----------------
    budget = estimate_budget_logic(
        flight_price=flight.get("price", 0),
        hotel_price_per_night=hotel.get("price_per_night", 0),
        number_of_nights=days - 1,
        daily_expense=1000,
        number_of_days=days
    )

    # ---------------- WEATHER TEXT (DYNAMIC) ----------------
    max_weather_days = min(days, len(daily_weather))

    weather_text = ""
    for i in range(max_weather_days):
        weather_text += f"> Day {i+1}: {daily_weather[i]}\n"
    if days > max_weather_days:
        weather_text += f"\n⚠️ Weather forecast available only for {max_weather_days} days.\n"

    # ---------------- ITINERARY TEXT (DYNAMIC) ----------------
    itinerary_text = ""
    max_days = min(days, len(places))
    for i in range(max_days):
     itinerary_text += f"> Day {i+1}: Visit {places[i]['place_name']}\n"

    if days > max_days:
     itinerary_text += (
        f"\n⚠️ Only {max_days} unique places available. "
        f"Remaining days can be used for leisure or personal exploration.\n"
    )
    # ---------------- FINAL OUTPUT ----------------
    output = f"""
Your {days}-Day Trip to {destination}

Flight Selected:
> {flight.get('airline', 'N/A')} (₹{flight.get('price', 'N/A')}) – Departs {source}

Hotel Booked:
> {hotel.get('hotel_name', 'N/A')} (₹{hotel.get('price_per_night', 'N/A')}/night, {hotel.get('stars', 'N/A')}-star)

Weather:
{weather_text}

Itinerary:
{itinerary_text}

Estimated Total Budget:
> Flight: ₹{budget['flight_cost']}
> Hotel: ₹{budget['hotel_cost']}
> Food & Travel: ₹{budget['daily_expenses']}

-------------------------------------
Total Cost: ₹{budget['total_budget']}
"""

    return output


# ---------------------------------------
# LOCAL TEST
# ---------------------------------------
if __name__ == "__main__":
    print(run_travel_agent("Hyderabad", "Delhi", 3))
