import logging
import requests

logger = logging.getLogger(__name__)



def get_weather(location: str) -> dict:
    """
    Fetch current weather for a specific city using
    Open-Meteo's free geocoding and weather APIs.
    """

    logger.info(
        "Fetching weather for location: %s",
        location,
    )

    # ========================================================
    # STEP 1: GEOCODE CITY
    # ========================================================

    geocoding_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    geocoding_params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response = requests.get(
        geocoding_url,
        params=geocoding_params,
        timeout=10,
    )

    response.raise_for_status()

    location_data = response.json()

    results = location_data.get(
        "results",
        [],
    )

    if not results:
        raise ValueError(
            f"Location not found: {location}"
        )

    place = results[0]

    latitude = place["latitude"]
    longitude = place["longitude"]
    city_name = place["name"]

    logger.info(
        "Location resolved: %s (%s, %s)",
        city_name,
        latitude,
        longitude,
    )

    # ========================================================
    # STEP 2: GET WEATHER
    # ========================================================

    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
    )

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "weather_code"
        ),
        "timezone": "auto",
    }

    response = requests.get(
        weather_url,
        params=weather_params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    precipitation = current["precipitation"]
    weather_code = current["weather_code"]

    logger.info(
        "Weather retrieved successfully for %s",
        city_name,
    )

    return {
        "location": city_name,
        "latitude": latitude,
        "longitude": longitude,
        "temperature": temperature,
        "humidity": humidity,
        "precipitation": precipitation,
        "weather_code": weather_code,
        "time": current.get("time"), 
        "timezone": data.get("timezone"),
    }