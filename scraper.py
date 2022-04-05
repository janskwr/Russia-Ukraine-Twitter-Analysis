# importing libraries and packages
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
        'Bucha since:2022-04-01 until:2022-04-05')
                                  .get_items()):  # declare a username
    if i > 100:  # number of tweets you want to scrape
        break
    tweets_list1.append(
        [tweet.date, tweet.id, tweet.content, tweet.user.username])  # declare the attributes to be returned

# Creating a dataframe from the tweets list above
tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

tweets_df1.to_csv('twitter_data1.csv')
