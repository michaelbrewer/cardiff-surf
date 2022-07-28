from datetime import datetime, timezone
from typing import Any, Dict, List, cast

import requests
import tweepy  # type: ignore
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.utilities.parameters import get_parameter
from dateutil.parser import parse

tracer = Tracer()


@tracer.capture_lambda_handler
def handler(event, context):
    twitter_client().create_tweet(text=current_surf_report())
    return "Completed"


def twitter_client() -> tweepy.Client:
    """Build the twitter client"""
    twitter_credentials = cast(
        dict, get_parameter(name="/projects/cardiff/twitter", transform="json", decrypt=True, max_age=60)
    )
    return tweepy.Client(
        bearer_token=twitter_credentials["bearer_token"],
        consumer_key=twitter_credentials["api_key"],
        consumer_secret=twitter_credentials["api_key_secret"],
        access_token=twitter_credentials["access_token"],
        access_token_secret=twitter_credentials["access_token_secret"],
    )


def current_surf_report() -> str:
    """Formatted weather report for the next hour"""
    stormglass_credential = cast(
        dict, get_parameter(name="/projects/cardiff/stormglass", transform="json", decrypt=True, max_age=60)
    )
    response = requests.get(
        url="https://api.stormglass.io/v2/weather/point",
        headers={"Authorization": stormglass_credential["api_key"]},
        params={  # type: ignore
            # Swami's Beach location
            "lat": 33.034140,
            "lng": -117.293228,
            "params": ",".join(["waveHeight", "airTemperature"]),
        },
    )
    response.raise_for_status()
    result = response.json()

    report = next_closest_time(result["hours"])
    wave_height = report.get("waveHeight", {}).get("sg", "N/A")
    air_temp = report.get("airTemperature", {}).get("sg", "N/A")

    return f"Swami's Beach Report: {wave_height}m wave height, air temp of {air_temp}c"


def next_closest_time(hours: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Find the next weather report

    Parameters
    ----------
    hours : List[Dict[str, Any]]
        Weather report by hour

    Returns
    -------
    Dict[str, Any]
        Next weather report by hour
    """
    current_time = datetime.now(timezone.utc)
    for hour in hours:
        hour_diff = (parse(hour["time"]) - current_time).total_seconds() / 60 / 60
        if hour_diff > 0:
            return hour
    return {}
