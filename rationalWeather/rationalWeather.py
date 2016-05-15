# rationalWeather!
#A weather bot that will give you an overview of what the weather is. 
#E.g. "Currently at ISU, it's salmon short weather." 
import twitter
import pywapi
#imports my SECRET keys from keys.py. 
from keys import *
import random
from weatherOptions import *
from pprint import pprint

# Authenticate via OAuth
api = twitter.Api(
    consumer_key,
    consumer_secret,
    token_key,
    token_secret
)

#Thanks, Thomas 
def postStatus(status, in_reply_tweet=None):
	""" Posts a Status, deleting any duplicate statuses.
    Parameters:
            status - Given status to post to twitter.

    Returns:
            results - The result of the PostUpdate call.
    """
	#Initialize flag, stringify status, and get a list of tweets from your account
	status = str(status)
	feed = api.GetUserTimeline("rationalWeather")
	#For the tweet in the feed
	for tweet in feed:
		#If this tweet is a duplicate
		if status == tweet.text:
			#Destroy that tweet
			api.DestroyStatus(tweet.id)
	#Post the status and return the results
	return api.PostUpdate(status, in_reply_tweet)


location = pywapi.get_location_ids('Ames, Iowa')
#print location
weather = pywapi.get_weather_from_yahoo('50011', '')
windchill = weather['wind']
weather = weather['condition']

#removed loop because it was not working exactly like I thought it was.
#if it's cold outside, choose from the windChill list, else, choose from the normal list 
if windchill['chill'] <= '20':
	currentCondition = random.choice(windChill[weather[u'code']])
else: 
	currentCondition = random.choice(weatherCodes[weather[u'code']])

print currentCondition


postStatus(currentCondition)
