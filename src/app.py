from datetime import datetime, timezone
from typing import Any, Dict, List

import requests
import tweepy
from aws_lambda_powertools import Tracer, Logger
from aws_lambda_powertools.utilities.parameters import get_parameter
from dateutil.parser import parse

tracer = Tracer()
logger = Logger()


@tracer.capture_lambda_handler
def handler(event, context):
    twitter_client().create_tweet(text=current_surf_report())
    return "Completed"


def twitter_client() -> tweepy.Client:
    """Build the twitter client"""
    twitter_credentials = get_parameter(name="/projects/cardiff/twitter", transform="json", decrypt=True, max_age=60)
    return tweepy.Client(
        bearer_token=twitter_credentials["bearer_token"],
        consumer_key=twitter_credentials["api_key"],
        consumer_secret=twitter_credentials["api_key_secret"],
        access_token=twitter_credentials["access_token"],
        access_token_secret=twitter_credentials["access_token_secret"],
    )


def current_surf_report() -> str:
    """Formatted weather report for the next hour"""
    stormglass_credential = get_parameter(
        name="/projects/cardiff/stormglass", transform="json", decrypt=True, max_age=60
    )
    response = requests.get(
        "https://api.stormglass.io/v2/weather/point",
        params={
            # Swami's Beach location
            "lat": 33.034140,
            "lng": -117.293228,
            "params": ",".join(["waveHeight", "airTemperature"]),
        },
        headers={"Authorization": stormglass_credential["api_key"]},
    )
    response.raise_for_status
    result = response.json()

    logger.debug(str(type(result)))
    logger.trace(result)

    report = next_closest_time(result["hours"])
    wave_height = report.get("waveHeight", {}).get("noaa", "N/A")
    air_temp = report.get("airTemperature", {}).get("noaa", "N/A")

    return f"Surf report: {wave_height}m wave height, air temp of {air_temp}c"


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
    current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    for hour in hours:
        hour_diff = (parse(hour["time"]) - current_time).total_seconds() / 60 / 60
        if hour_diff > 0:
            return hour
    return {}
