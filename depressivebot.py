import tweepy
import markovify
import random
import os
import boto3

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
BUCKET = os.environ.get("BUCKET")
KEY = os.environ.get("KEY")

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

def main():
    text = get_corpus_from_s3()
    text_model = markovify.Text(text)
    tweet_something(text_model.make_sentence())

if __name__ == '__main__':
    main()