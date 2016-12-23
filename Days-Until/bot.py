# -*- coding: utf-8 -*-
from datetime import date 
import tweepy as ty 
from keys import * 


def set_twitter_auth():
    """
    authorize with the Twitter API
    thanks, elias
    """
    auth = ty.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = ty.API(auth)
    return api

def post_status(api, status):
    status = str(status)
    return api.update_status(status)

def days_until(target_date): 
    return str((target_date - date.today()).days)

if __name__ == '__main__': 
    api = set_twitter_auth()
    spring_status = days_until(date(2017, 3, 30)) + " days until spring! 🌼"
    post_status(api, spring_status)