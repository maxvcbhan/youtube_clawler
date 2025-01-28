import snscrape.modules.twitter as sntwitter
import pandas as pd

for i, tweet in enumerate(sntwitter.TwitterSearchScraper('bitcoin since:2021-07-01 until:2022-12-31').get_items()):
    # if i>maxTweets:
    #     break

    tweets_list1.append([tweet.date, tweet.id, tweet.rawContent, tweet.user.username])

    if (i + 1) % 5000 == 0:

        # Creating a dataframe from the tweets list above
        tweet_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
        print(tweet_df1)

        # Export dataframe into a csv
        tweet_df1.to_csv(f'bitcoin-{(i+1)/5000}.csv', sep=',', index=False)
        tweets_list1 = []