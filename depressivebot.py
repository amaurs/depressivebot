import tweepy
import markovify
import random
import os
import boto3
import time
import logging

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
BUCKET = os.environ.get("BUCKET")
KEY = os.environ.get("KEY")
PROB_TWEET = float(os.environ.get("PROB_TWEET", "0.1"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def tweet_something(status):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    access = auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    logger.info("Acces to twitter API.")
    api = tweepy.API(auth)
    api.update_status(status)
    api = None

def get_corpus_from_s3():
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET, KEY)
    text = obj.get()['Body'].read().decode('utf-8')
    logger.info("Corpus pulled from S3.")
    return text

def do_action(text):
    logger.info("Train model.")
    text_model = markovify.Text(text)
    content = text_model.make_sentence()
    logger.info("Content: %s" % content)
    tweet_something(content)

def lambda_handler(event, context):
    action = "sleep"
    logger.info('Probablilty of tweeting: %s' % PROB_TWEET)
    if(random.random() < PROB_TWEET):
        do_action(get_corpus_from_s3())
        action = "tweet"

    logger.info("Action performed: %s" % action)

    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_data(MetricData=[
        {
            'MetricName': 'Depressive Bot Action',
            'Dimensions': [
                {
                    'Name': 'Action',
                    'Value': action
                }
            ],
            'Unit': 'None',
            'Value': 1,
        }], Namespace='DepressiveBot')
    
    return { 
        'action': action
    }  