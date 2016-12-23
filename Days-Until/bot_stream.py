# -*- coding: utf-8 -*-
"""
    The streaming portion of the Days Until bot. 
    This will parse a date from a tweet, 
    calculate the number of days until that date,
    and then tweet the days until that date.
"""
import tweepy as ty
import json
from keys import *
from datetime import date 

#override tweepy.StreamListener class
class DaysStreamListener(ty.StreamListener):

    def __init__(self, api):
        self.api = api
        super(ty.StreamListener, self).__init__()

    def on_data(self, data):
        data = json.loads(data)
        self.respond(data)

    def on_error(self, status):
        print(status)

    def respond(self, data): 
        """
        method to respond to a tweet directed at @daysminusminus
        """
        user = data['user']['screen_name']
        tweet_id = data['id']
        tweet = data['text']
        
        unformatted_date = self.strip_date(data) #date from tweet
        try: 
            if unformatted_date: 
                formatted_date = self.get_date(unformatted_date) #date object
            else: 
                return
            if formatted_date: 
                pretty_date = formatted_date.strftime('%B %d, %Y')
            else: 
                return 
        except ValueError: 
            return #later, I will send a tweet that addresses the issue at hand
        num_days_until = self.days_until(formatted_date)

        if num_days_until: 
            reply_tweet = "@"+ user + " There are " + str(num_days_until) + " days until " + pretty_date + "."
            api.update_status(status = reply_tweet, in_reply_to_status_id = tweet_id)

    def strip_date(self, data): 
        """
        method to strip the string representation of a date
        from a tweet 
        """
        tweet = data['text'].lower()
        if "@daysminusminus days until" in tweet: 
            tweet = tweet.strip("@daysminusminus days until")
        else: 
            return False #do not respond to this tweet 
        return tweet

    def get_date(self, tweet_date):
        """
        method to strip the date from a string 
        raises a ValueError if the date is not in the correct format
        per date() arg reqs
        """
        if '-' in tweet_date: 
            l_date = tweet_date.split('-')
            try: 
                date_obj = date(int(l_date[2]), int(l_date[0]), int(l_date[1]))
                return date_obj
            except ValueError: 
                raise ValueError
        else: 
            return False 

    def days_until(self, date_obj): 
        """
        method to calculate the number of days until date_obj
        """
        if date_obj < date.today(): 
            return
        return str((date_obj - date.today()).days)

def set_twitter_auth():
    """
    authorize with the Twitter API
    thanks, elias
    """
    auth = ty.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = ty.API(auth)
    return api

if __name__ == "__main__": 
    api = set_twitter_auth()
    daysStreamListener = DaysStreamListener(api)
    daysStream = ty.Stream(auth = api.auth, listener=daysStreamListener)
    daysStream.filter(track=['@daysminusminus'])
