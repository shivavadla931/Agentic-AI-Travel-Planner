import requests
from typing import Dict, List
from langchain.tools import tool

# ---------------------------------------
# CITY → LAT/LON MAPPING
# (expand if needed)
# ---------------------------------------
CITY_COORDINATES = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867},
    "Goa": {"lat": 15.2993, "lon": 74.1240}
}

# ---------------------------------------
# PURE PYTHON LOGIC
# ---------------------------------------
def get_weather_logic(city: str) -> Dict:
    # Check if city has coordinates
    if city not in CITY_COORDINATES:
        return {"message": "City not supported"}

    lat = CITY_COORDINATES[city]["lat"]
    lon = CITY_COORDINATES[city]["lon"]

    # Build API URL
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        "&daily=temperature_2m_max"
        "&timezone=auto"
    )

    resp = requests.get(url, timeout=10)
    data = resp.json()

    daily = data.get("daily", {})
    times: List[str] = daily.get("time", [])
    temps: List[float] = daily.get("temperature_2m_max", [])

    # Prepare a simple textual description per day
    weather_list = []
    for i in range(min(3, len(times))):
        day = times[i]
        temp = temps[i] if i < len(temps) else None

        if temp is not None:
            # Simple phrase based on temperature
            if temp >= 30:
                summary = f"Sunny ({round(temp)}°C)"
            elif temp >= 25:
                summary = f"Partly Cloudy ({round(temp)}°C)"
            else:
                summary = f"Light Breeze ({round(temp)}°C)"
        else:
            summary = "Weather data unavailable"

        weather_list.append(summary)

    return {
        "city": city,
        "daily_weather": weather_list
    }


# ---------------------------------------
# LANGCHAIN TOOL
# ---------------------------------------
@tool
def weather_lookup(city: str) -> Dict:
    """Get daily weather forecast for a city."""
    return get_weather_logic(city)


# ---------------------------------------
# LOCAL TEST
# ---------------------------------------
if __name__ == "__main__":
    print(get_weather_logic("Goa"))
