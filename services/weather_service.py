import requests


def get_weather(city: str) -> str:
    """Fetch current weather for a city
    and return temperature and description."""

    try:
        response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp = data["current_condition"][0]["temp_C"]
            desc = data["current_condition"][0]["weatherDesc"][0]["value"]
            return f"{city}: {temp}°C, {desc}"
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
