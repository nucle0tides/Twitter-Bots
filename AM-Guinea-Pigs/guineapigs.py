import praw 
import twitter 
from pprint import pprint 
from keys import * 
import urllib

#Some Twitter Housekeeping Stuff
# Authenticate via OAuth
api = twitter.Api(
    consumer_key,
    consumer_secret,
    token_key,
    token_secret
)

def verifyCredentials():
    '''
        Method to verify that your keys work
        Also known as a "network connectivity test"
    '''
    print api.VerifyCredentials()

def postStatus(status, image): 
    length = len(status) + len(image)
    if (length) > 140:
        max_chars = 140
        to_remove = length - max_chars
        status = status[:-to_remove - 3] + "..."
        api.PostMedia(status, image)
    else: 
        api.PostMedia(status, image)

def searchByTerm(term): 
    '''
        Method to search for a term
    '''
    search_feed = api.GetSearch(term)
    for tweet in search_feed: 
        #use .encode() to avoid some unicode issues when trying to print tweets
        print "@" + tweet.user.screen_name.encode('utf-8') + " tweeted " + "\"" + tweet.text.encode('utf-8') + "\"" 

        #Do whatever you want here! 
        #favorite that tweet 
        favoriteTweet(tweet)
        #follow the account that tweeted the message
        #followAccount(tweet.user.id)
        #retweet tweet 
        #retweetTweet(tweet.id)

def favoriteTweet(given_tweet): 
    '''
        Method to favorite a tweet. 
        Status.GetFavorited() was not working as intended- so I just threw it into a try/except block 
        so the bot won't throw any errors when trying to favorite something 
    '''
    try: 
        api.CreateFavorite(given_tweet)
    except twitter.TwitterError, t: 
        print "You've already favorited that tweet!"

def autoFavoriteMentions(): 
    '''
        Method to auto-favorite mentions
    '''
    mentions = api.GetMentions()
    for tweet in mentions: 
        #print "@" + tweet.user.screen_name + " tweeted " + "\"" + tweet.text.encode('utf-8') + "\"" 
        favoriteTweet(tweet)

#Now some Reddit Stuff 

user_agent = ("Guinea Pigs and Rabbits by /u/nucle0tides") 
r = praw.Reddit(user_agent=user_agent) 

guineapigs = r.get_subreddit('guineapigs')
rabbits = r.get_subreddit('rabbits')

guineapigs = guineapigs.get_top(limit=1)
rabbits = rabbits.get_top(limit=1) 

def get_animals(subreddit): 
    response = []
    for post in subreddit: 
        post = vars(post)
        if 'imgur.com' in post['domain']: 
            if '.jpg' in post['url']: 
                response = [post['title'], post['url']]
            else: 
                response = [post['title'], post['url'] + '.jpg']
    return response

rabbit = get_animals(rabbits)
guineapig = get_animals(guineapigs)

postStatus(guineapig[0],guineapig[1])
postStatus(rabbit[0],rabbit[1])
searchByTerm("Guinea Pig")
searchByTerm("Rabbit")
autoFavoriteMentions()
