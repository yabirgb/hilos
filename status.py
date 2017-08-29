import json
import time
import hashlib

import tweepy

from db.models_data import Tweet, Branch, calldb

CLIENT = os.environ.get("CLIENT", None)
SECRET = os.environ.get("SECRET", None)

auth = tweepy.OAuthHandler(CLIENT, SECRET)



api = tweepy.API(auth)
db = calldb()

def search(looking_for, tweets, branch):
    print("Reached search", " ", looking_for)
    if looking_for != None:
        for status in tweets:
            print(status.id_str)
            if int(status.in_reply_to_status_id) == int(looking_for):
                tweet = Tweet.create(username=status.user.screen_name,
                                 tweet_id = status.id_str ,
                                 date=status.created_at,
                                 reply_to=status.in_reply_to_status_id,
                                 branch=branch)
                branch.height += 1
                return status.id_str

    return None

def run_up(tid, branch):
    tweet_status = api.get_status(tid)
    while (tweet_status.in_reply_to_status_id != None):

        tweet = Tweet.create(username=tweet_status.user.screen_name,
                            tweet_id = tweet_status.id_str ,
                            date=tweet_status.created_at,
                            reply_to=tweet_status.in_reply_to_status_id,
                            branch=branch)
        branch.height += 1
        print("Done "+ str(tweet_status.in_reply_to_status_id))

        tweet_status = api.get_status(tweet_status.in_reply_to_status_id)
    #Add last one
    tweet = Tweet.create(username=tweet_status.user.screen_name,
                            tweet_id = tweet_status.id_str ,
                            date=tweet_status.created_at,
                            reply_to=tweet_status.in_reply_to_status_id,
                            branch=branch)

def run_down(tid, username, branch):
    query = "to:{} from:{}".format(username, username)
    tweets = tweepy.Cursor(api.search, q=query, since_id=tid, rpp=100).items()
    next_tweet = search(tid, tweets, branch)
    print(query)
    while next_tweet != None:
        print("Going down")
        ntid = int(next_tweet)
        tweets = tweepy.Cursor(api.search, q=query, since_id=ntid, rpp=100).items()
        next_tweet = search(ntid, tweets, branch)

def root(tid):
    try:
        tweet_status = api.get_status(tid)

        branch = Branch.create(height=1)

        tweet = Tweet.create(username=tweet_status.user.screen_name,
                            tweet_id = tweet_status.id_str ,
                            date=tweet_status.created_at,
                            reply_to=tweet_status.in_reply_to_status_id,
                            branch=branch)

        if tweet_status.in_reply_to_status_id != None:
            run_up(tweet_status.in_reply_to_status_id, branch)

        run_down(int(tweet_status.id_str), tweet_status.user.screen_name, branch)

        branch.save()

    except tweepy.TweepError as e:

        print (e.api_code)
        print (e.reason)
