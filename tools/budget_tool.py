from typing import Dict
from langchain.tools import tool

# PURE PYTHON LOGIC

def estimate_budget_logic(
    flight_price: int,
    hotel_price_per_night: int,
    number_of_nights: int,
    daily_expense: int,
    number_of_days: int
) -> Dict:
    hotel_cost = hotel_price_per_night * number_of_nights
    daily_cost = daily_expense * number_of_days

    total_cost = flight_price + hotel_cost + daily_cost

    return {
        "flight_cost": flight_price,
        "hotel_cost": hotel_cost,
        "daily_expenses": daily_cost,
        "total_budget": total_cost
    }


# LANGCHAIN TOOL

@tool
def budget_estimator(
    flight_price: int,
    hotel_price_per_night: int,
    number_of_nights: int,
    daily_expense: int,
    number_of_days: int
) -> Dict:
    """Estimate total travel budget"""
    return estimate_budget_logic(
        flight_price,
        hotel_price_per_night,
        number_of_nights,
        daily_expense,
        number_of_days
    )

# LOCAL TEST

if __name__ == "__main__":
    print(
        estimate_budget_logic(
            flight_price=2907,
            hotel_price_per_night=5536,
            number_of_nights=2,
            daily_expense=1000,
            number_of_days=3
        )
    )
