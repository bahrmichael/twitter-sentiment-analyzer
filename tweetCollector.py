import json
import tweepy
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
table = dynamodb.Table(os.environ['TABLE_NAME'])


auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])


def handle(event, context):

    api = tweepy.API(auth)
    if not api:
        print("Can't Authenticate")
        return

    tweets_per_query = 100
    loaded_tweets = 0
    max_tweets = 100
    search_query = os.environ['SEARCH_QUERY']
    max_id = -1
    since_id = None
    language = os.environ['LANGUAGE']

    count = 0

    while loaded_tweets < max_tweets:
        try:
            if (max_id <= 0):
                if (not since_id):
                    new_tweets = api.search(q=search_query, lang=language, count=tweets_per_query)
                else:
                    new_tweets = api.search(q=search_query, lang=language, count=tweets_per_query, since_id=since_id)
            else:
                if (not since_id):
                    new_tweets = api.search(q=search_query, lang=language, count=tweets_per_query, max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=search_query, lang=language, count=tweets_per_query, max_id=str(max_id - 1), since_id=since_id)

            if not new_tweets:
                print("No more tweets found")
                break
            loaded_tweets += len(new_tweets)
            print(f"Downloaded {loaded_tweets} tweets")
            max_id = new_tweets[-1].id

            for tweet in new_tweets:
                existing_tweet = table.get_item(Key={'id': tweet._json['id']}).get('Item', None)
                if existing_tweet is None:
                    table.put_item(
                        Item={
                                'id': tweet._json['id'],
                                'created_at': tweet._json['created_at'],
                                'text': tweet._json['text'],
                                'query': search_query
                            }
                        )
                    count += 1
        except tweepy.TweepError as e:
            print("Error: %s" % str(e))

    print("Saved tweets: %d" % count)
