# -*- coding: utf-8 -*-
from datetime import date 
import tweepy 
from keys import * 

#override tweepy.StreamListener to add logic to on_status
class DaysUntilStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

def set_auth(): 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token_key, token_secret)

    api = tweepy.API(auth)
    return api 


if __name__ == '__main__': 
    api = set_auth()

    days_until = DaysUntilStreamListener()
    days_until_stream = tweepy.Stream(auth = api, listener=myStreamListener()
