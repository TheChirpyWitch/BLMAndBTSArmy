import yaml
config = dict(
    search_tweets_api = dict(
        account_type = 'premium',
        # ipark
        endpoint =        'https://api.twitter.com/1.1/tweets/search/fullarchive/dev.json',
        consumer_key =    ###yours
        consumer_secret = ###yours
    )
)
with open('twitter_keys_fullarchive.yaml', 'w') as config_file:
    yaml.dump(config, config_file, default_flow_style=False)

from searchtweets import load_credentials

premium_search_args = load_credentials("twitter_keys_fullarchive.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)
print(premium_search_args)

from searchtweets import gen_rule_payload
from searchtweets import ResultStream
import time
import datetime
query = "#MatchAMillion"
###rule = gen_rule_payload(query, results_per_call=100,
###from_date="2020-06-07", to_date="2020-06-08")

#https://twitterdev.github.io/search-tweets-python/index.html?highlight=gen_rule_payload
import pandas as pd
# 1st collection
# generate starting time from 13:00 to 23:00 at every 15 minutes 
"""
startTimeList = (pd.DataFrame(columns = ['NULL'],
    index = pd.date_range('2020-06-07T13:00', '2020-06-07T23:00', 
    freq = '15T')).index.strftime('%Y-%m-%d %H:%M').tolist())
endTimeList = (pd.DataFrame(columns = ['NULL'],
    index = pd.date_range('2020-06-07T13:15', '2020-06-07T23:15', 
    freq = '15T')).index.strftime('%Y-%m-%d %H:%M').tolist())
"""
# 2nd collection
# generate starting time from 13:03 to 23:03 at every 10 minutes 
startTimeList = (pd.DataFrame(columns = ['NULL'],
    index = pd.date_range('2020-06-07T13:03', '2020-06-07T23:03', 
    freq = '10T')).index.strftime('%Y-%m-%d %H:%M').tolist())
endTimeList = (pd.DataFrame(columns = ['NULL'],
    index = pd.date_range('2020-06-07T13:18', '2020-06-07T23:18', 
    freq = '10T')).index.strftime('%Y-%m-%d %H:%M').tolist())


#### for-loop
for startTime, endTime in zip(startTimeList, endTimeList):
    print(startTime, endTime)
    rule = gen_rule_payload(query, results_per_call=100, 
            from_date="%s" % startTime,
            to_date="%s" % endTime)

    rs = ResultStream(rule_payload=rule,
                     max_results=100,
                     **premium_search_args)
    print(rs)
    time.sleep(65) # wait 65 seconds

    import json
    with open('tweetsData.jsonl', 'a', encoding='utf-8') as f:
        for tweet in rs.stream():
            json.dump(tweet, f)
            f.write('\n')
    print('done')
