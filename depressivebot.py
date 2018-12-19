from __future__ import unicode_literals

import tweepy
import markovify
import random
import os

CONSUMER_KEY=os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET=os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN=os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET=os.environ.get("ACCESS_TOKEN_SECRET")

def tweet_something(status):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(status)
    api = None

def main():
    with open("robot.txt") as f:
        text = f.read()
    text_model = markovify.Text(text)
    tweet_something(text_model.make_sentence())

if __name__ == '__main__':
    main()