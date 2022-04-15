# importing libraries and packages
import snscrape.modules.twitter as sntwitter
import pandas as pd

# Creating list to append tweet data
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(

        'Bucha since:2022-04-03 until:2022-04-05')
                                  .get_items()):
    if i > 10000:  # number of tweets you want to scrape
        break
    tweets_list1.append(
        [tweet.date,
         tweet.id,
         tweet.content,
         tweet.user.username,
         tweet.replyCount,
         tweet.retweetCount,
         tweet.likeCount,
         tweet.quoteCount,
         tweet.lang,
         #tweet.source,
         tweet.retweetedTweet,
         tweet.quotedTweet,
         tweet.mentionedUsers
         ])  # declare the attributes to be returned

# Creating a dataframe from the tweets list above
tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime',
                                                 'Tweet Id',
                                                 'Text',
                                                 'Username',
                                                 'Replies Count',
                                                 'Retweets Count',
                                                 'Likes Count',
                                                 'Quotes Count',
                                                 'Language',
                                                 #'Source',
                                                 'Retweeted Tweet',
                                                 'Quoted Tweet',
                                                 'Mentioned Users'
                                                 ])
tweets_df1['Mentioned Users'] = tweets_df1['Mentioned Users']. \
                                    apply(lambda x: [o.username for o in x] if(x is not None) else x)

tweets_df1.to_csv('bucha_10k.csv')

