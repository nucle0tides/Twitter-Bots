# -*- coding: utf-8 -*-
from datetime import date 
import twitter 
from keys import * 


# Authenticate via OAuth
api = twitter.Api(
    consumer_key,
    consumer_secret,
    token_key,
    token_secret
)

def post_status(status):
    status = str(status)
    return api.PostUpdate(status)

def days_until(target_date): 
    return str((target_date - date.today()).days)

if __name__ == '__main__': 
    #spring_status = days_until(date(2017, 3, 30)) + " days until spring! 🌼"
    graduation_status = days_until(date(2017, 12, 16)) + " days until graduation 🎓"
    #post_status(spring_status)
    post_status(graduation_status)