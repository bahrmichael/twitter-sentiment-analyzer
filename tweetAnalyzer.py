import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
table = dynamodb.Table(os.environ['TABLE_NAME'])

comprehend = boto3.client('comprehend')


def handle(event, context):

    language = os.environ.get('LANGUAGE')

    tweets = []
    for item in event.get('Records', []):
        item_id = int(item['dynamodb']['Keys']['id']['N'])
        tweet = table.get_item(Key={'id': item_id}).get('Item', None)
        if 'sentiment_score' not in tweet:
            tweets.append(tweet)

    if len(tweets) == 0:
        print('No new tweets to analyse')
        return

    text_list = list(map(lambda tweet: tweet['text'], tweets))
    comprehend_response = comprehend.batch_detect_sentiment(
        TextList=text_list,
        LanguageCode=language
    )

    for entry in comprehend_response.get('ResultList', []):
        tweet = tweets[entry['Index']]
        tweet['sentiment_score'] = json.loads(json.dumps(entry['SentimentScore']), parse_float=Decimal)
        table.put_item(Item=tweet)

    print(f'Analyzed {len(tweets)} tweets')
