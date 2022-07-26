from aws_lambda_powertools.utilities.parameters import get_parameter
import tweepy


def handler(event, _):
    twitter_credentials = get_parameter(name="/projects/cardiff/twitter", transform="json", decrypt=True, max_age=60)
    client = tweepy.Client(
        bearer_token=twitter_credentials["bearer_token"],
        consumer_key=twitter_credentials["api_key"],
        consumer_secret=twitter_credentials["api_key_secret"],
        access_token=twitter_credentials["access_token"],
        access_token_secret=twitter_credentials["access_token_secret"],
    )
    client.create_tweet(text=event.get("msg", "From cron"))
