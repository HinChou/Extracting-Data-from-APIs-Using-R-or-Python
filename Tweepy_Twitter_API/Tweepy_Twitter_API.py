# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 15:27:38 2016

@author: Hin
"""

import tweepy
import re



def get_text_twitter(twitter_id, cs_key, cs_secret, as_token, as_token_secret):
    """
    Get maximal amount of twitters from an account(twitter_id),
    which can be found after the "id_str" in "view page source".
    The approximate maximum amount is around 3200, 
    which is limited by tweepy.
    
    Parameters:
    cs_key = Consumer Key / API Key
    cs_secret = Consumer Secret / API Secret
    as_token = Access Token
    as_token_secret = Access Token Secret
    """
    
    auth = tweepy.OAuthHandler(cs_key, cs_secret)
    
    auth.set_access_token(as_token, as_token_secret)
    
    api = tweepy.API(auth)

    try:
        user_tweets = tweepy.Cursor(api.user_timeline, id = twitter_id).pages()
        # list comprehension, which is equal to:
        #    for tweet in user_tweets:
        #        twitter_contents.append(tweet)
        twitter_contents = [tweet for tweet in user_tweets]
        
    except tweepy.TweepError as e:
        return ('Error: ', e)
            
    tweet_all_list = []
    
    #Compiled the regex and made the regex case-insensitive
    pattern = "(?<=text\=\").*?(?=\")|(?<=text\=').*?(?=')"
    regex = re.compile(pattern, flags=re.IGNORECASE)
    
    for text_str in twitter_contents:
        text_str = str(text_str)
        tweets_text = regex.findall(text_str)
        tweet_all_list.append(tweets_text)
    
    # Retrieved a flat list out of list of lists (Looks like it's also a fast way)  
    # Template: [item for sublist in l for item in sublist], l is the list to be flattened.
    tweets_all = [item for sublist in tweet_all_list for item in sublist]
    
    return tweets_all
    
