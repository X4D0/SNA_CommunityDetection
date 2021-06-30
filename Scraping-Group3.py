import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data to
tweets_list = []

# Using TwitterSearchScraper to scrape data and append tweets to list
print('Scraping tweets...')
scrape = sntwitter.TwitterSearchScraper('#sahkanruupks OR #tolakruupks since:2020-06-01 until:2020-12-31').get_items()
for tweet in scrape:
    if tweet.likeCount >= 1 or tweet.retweetCount >= 1 or tweet.user.followersCount >= 60:
        tweets_list.append([tweet.id, tweet.user.username, tweet.date, tweet.content,
                        tweet.retweetCount, tweet.likeCount])
    
# Creating a dataframe from the tweets list above
tweets_df = pd.DataFrame(tweets_list, columns=['ID', 'Username', 'Date', 'Text', 'RT', 'Likes'])

# Export to csv
tweets_df.to_csv('data_tweets.csv', index=False)

print('Exported to Data_Tweets.csv')
