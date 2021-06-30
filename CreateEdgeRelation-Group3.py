import pandas as pd
import tweepy
import time
import sys

#Twitter API credentials
consumer_key = "uBaoKrzU3YCS9a6RjIWlD2Fkp"
consumer_secret = "7RZuRMFr23Szu5sGsEMAYIPCyeLMGf7I98kZobBk2Ta2BDVAVi"
OAUTH_KEYS = {'consumer_key':consumer_key, 'consumer_secret':consumer_secret}
auth = tweepy.OAuthHandler(OAUTH_KEYS['consumer_key'], OAUTH_KEYS['consumer_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#read dataset
df_tweets = pd.read_csv("data_tweets.csv", dtype = str)
#clean the dataset
df_tweets.drop(df_tweets[df_tweets['RT'] < "1"].index, inplace = True)
df_tweets.drop(df_tweets[df_tweets['Likes'] < "1"].index, inplace = True)

#create dataframe relation
df_relation = pd.DataFrame()
df_relation['TweetID'] = []
df_relation['User1'] = []
df_relation['User2'] = []

#Listing the retweeter
count = 0
nameCount = len(df_tweets)
for index, row in df_tweets.iterrows():
    try:
        retweets_list = api.retweets(row['ID'])
        for retweet in retweets_list:
            df = pd.DataFrame({'TweetID':[row['ID']],
                               'User1':[row['Username']],
                               'User2':[retweet.user.screen_name]})
            df_relation = pd.concat([df_relation, df])
    except tweepy.TweepError as e:
        if e == "[{u'message': u'Rate limit exceeded', u'code': 88}]":
            time.sleep(60 * 5)  # Sleep for 5 minutes
        else:
            pass
    time.sleep(1)
    #Status Bar
    count += 1
    per = round(count * 100.0 / nameCount, 1)
    sys.stdout.write("\rTwitter call %s%% complete." % per)
    sys.stdout.flush()
df_relation = df_relation.rename(columns = {'TweetID': 'Source', 'User2': 'Target'}, inplace = False)
#Convert Dataframe to CSV
df_relation.to_csv('relasi.csv',index = False)


