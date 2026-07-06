"""Supporting utilities for the AgentsVille AI travel-planning portfolio project."""

from enum import Enum
from typing import Any


class Interest(str, Enum):
    """Traveler interest categories used by the itinerary planner."""

    ART = "art"
    COOKING = "cooking"
    HIKING = "hiking"
    MUSIC = "music"
    PHOTOGRAPHY = "photography"
    TECHNOLOGY = "technology"
    TENNIS = "tennis"
    WRITING = "writing"


def call_weather_api_mocked(date: str, city: str) -> dict[str, Any]:
    """Return deterministic mocked weather data for portfolio/demo use.

    Args:
        date: Date in YYYY-MM-DD format.
        city: Destination city.

    Returns:
        A dictionary shaped like a weather API response.
    """

    return {
        "date": date,
        "city": city,
        "temperature": 75,
        "unit": "Fahrenheit",
        "condition": "sunny",
    }


def call_activities_api_mocked(date: str, city: str) -> list[dict[str, Any]]:
    """Return deterministic mocked activity data for portfolio/demo use.

    Args:
        date: Activity date in YYYY-MM-DD format.
        city: Destination city.

    Returns:
        A list of activity dictionaries similar to an external activity API.
    """

    return [
        {
            "activity_id": f"{date}-garden-music",
            "name": "Echo Gardens Music Walk",
            "description": "Outdoor garden walk with local music performances and indoor cafe backup if weather changes.",
            "start_time": "10:00",
            "end_time": "12:00",
            "price": 35,
            "related_interests": [Interest.MUSIC, Interest.ART],
        },
        {
            "activity_id": f"{date}-maker-lab",
            "name": "AgentsVille Maker Lab",
            "description": "Indoor technology and design workshop for travelers interested in creative problem solving.",
            "start_time": "14:00",
            "end_time": "16:00",
            "price": 45,
            "related_interests": [Interest.TECHNOLOGY, Interest.ART],
        },
    ]
