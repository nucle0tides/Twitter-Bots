import tweepy as ty
from secrets import *
import pickle
import json
import random

def set_twitter_auth():
    auth = ty.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = ty.API(auth)
    return api

def gather_tweets(api):
    new = []
    all_tweets = []
    new = api.user_timeline(screen_name = "@StationVIII", count = 200)
    all_tweets.extend(new)
    oldest = all_tweets[-1].id - 1

    while(len(new) > 0):
        new = api.user_timeline(screen_name = "@StationVIII", count = 200, max_id = oldest)
        all_tweets.extend(new)
        oldest = all_tweets[-1].id - 1

    return all_tweets

def serialize_tweets(tweet_list): 
    with open("tweets.pickle", "wb") as f: 
        pickle.dump(tweet_list, f, pickle.HIGHEST_PROTOCOL) 

def process_tweets(serialized_tweets):
    tweet_dict = {}
    tweet_list = pickle.load(open(serialized_tweets, "rb"))
    for tweet in tweet_list: 
        if tweet.text[0:1] == "@": 
            continue
        if tweet.text[0:2] == "RT": 
            continue
        tweet_dict[tweet.id] = tweet.since_id
    return tweet_dict

def pick_tweet(tweet_json):
    f = open(tweet_json, "r")
    tweet_dict = json.loads(f.read())
    tweet = random.choice(list(tweet_dict.keys()))
    return tweet

if __name__ == '__main__':
    api = set_twitter_auth()
    victim = pick_tweet("tweets.json")
    api.retweet(victim)
