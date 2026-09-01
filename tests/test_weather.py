from src.recipe_generator.weather import get_weather


def main():
    print("=" * 60)
    print("PHASE 11 - WEATHER TEST")
    print("=" * 60)

    location = "Miami"

    print(f"\nTesting weather for: {location}")

    try:
        weather = get_weather(location)

        print("\n" + "-" * 60)
        print("WEATHER RESULT")
        print("-" * 60)

        print(f"Location:       {weather['location']}")
        print(f"Latitude:       {weather['latitude']}")
        print(f"Longitude:      {weather['longitude']}")
        print(f"Temperature:    {weather['temperature']} °C")
        print(f"Humidity:       {weather['humidity']} %")
        print(f"Precipitation:  {weather['precipitation']} mm")
        print(f"Weather Code:   {weather['weather_code']}")

        print("\n" + "-" * 60)
        print("VALIDATION")
        print("-" * 60)

        assert weather["location"]
        assert isinstance(weather["latitude"], (int, float))
        assert isinstance(weather["longitude"], (int, float))
        assert isinstance(weather["temperature"], (int, float))
        assert isinstance(weather["humidity"], (int, float))
        assert isinstance(weather["precipitation"], (int, float))
        assert isinstance(weather["weather_code"], (int, float))

        print("✓ Location resolved")
        print("✓ Temperature returned")
        print("✓ Humidity returned")
        print("✓ Precipitation returned")
        print("✓ Weather code returned")
        print("✓ All weather fields validated")

        print("\n" + "=" * 60)
        print("✓ PHASE 11 WEATHER TEST PASSED")
        print("=" * 60)

    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ PHASE 11 WEATHER TEST FAILED")
        print("=" * 60)

        print(f"\nError type: {type(e).__name__}")
        print(f"Error: {e}")

        raise


if __name__ == "__main__":
    main()