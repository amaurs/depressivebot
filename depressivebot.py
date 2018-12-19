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

def tweet_something(status):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(status)
    api = None

def get_corpus_from_s3():
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET, KEY)
    text = obj.get()['Body'].read().decode('utf-8')
    return text

def do_action(text):
    text_model = markovify.Text(text)
    tweet_something(text_model.make_sentence())

def lambda_handler(event, context):
    action = "sleep"
    logging.warning('Probablilty of tweet: %s' % PROB_TWEET)
    if(random.random() < PROB_TWEET):
        do_action(get_corpus_from_s3())
        action = "tweet"
    return { 
        'action': action
    }  