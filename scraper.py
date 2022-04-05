from config import *
import tweepy

client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

query = 'bucha -is:retweet'

tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100)

for tweet in tweets.data:
    print(tweet.text)
    if len(tweet.context_annotations) > 0:
        print(tweet.context_annotations)
