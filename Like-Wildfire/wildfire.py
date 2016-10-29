"""
    Like Wildfire Bot 
    The concept is simple, spread every word like wildfire. 
"""
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

def get_word(file): 
    with open(file, 'r') as f: 
        current_word = f.readline() 
        leftover_words = list(f)
    #print(leftover_words[len(leftover_words) - 11:])
    f.close()
    with open(file, 'w') as f: 
        f.writelines(leftover_words)
    f.close()
    return current_word

if __name__ == '__main__':
    status = "Spread " + str(get_word('all_words.txt').strip()) + " like wildfire!"
    post_status(status)
    #print(status) 
