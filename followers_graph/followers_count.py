import tweepy
from tweepy import OAuthHandler
from tweepy import API
from collections import Counter
from datetime import datetime, date, time, timedelta
import sys
import json
import os
import io
import re
import time
import pymongo

def get_followers_count(target):    
    return auth_api.followers_count(target)


if __name__ == "__main__":
    f = open('un.txt', 'r+')
    account_list = [line.replace('\n', '') for line in f.readlines()]
    f.close()

    #account_list = ["1003503961226145797"]

    consumer_key="g7bgBlTndfcRHuYWUI3Q7dCIt"
    consumer_secret="fElzxTKc1C7RGGpdRj2tQqgNcm2PuiYiIB4qSM1uaKYSOIAfmu"
    access_token="705082009559826433-cE1qYJZy484QMVFjsskez9beg5M6N9k"
    access_token_secret="QlABIEeLbUqv1UtyW8cIwijgSZGarswEzcjhBivEdujO9"

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    auth_api = API(auth)

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["bts"]
    mycol = mydb["follower_count"]
    n = 0

    for target in account_list:
        n = n + 1
        print("Processing target: " + target)
        try:

            followers_count = get_followers_count(target)
            mydict = { "id": target, "followers_count": followers_count }
            x = mycol.insert_one(mydict)
            
            print(x)
            print(str(n)+"/784 done")
            time.sleep(70)
        except tweepy.TweepError as e:
            print("Exception met, going to sleep")
            time.sleep(70)