import os
import tweepy
import logging
import pandas as pd


class Twitter:
    # Variables that contains the credentials to access Twitter API
    ACCESS_TOKEN = '2214038774-bRdjyYxzju7EzDC936E9Lw8GJPH1vvc5QG3urDV'
    ACCESS_SECRET = 'kADbwwpPNr19yzSwSWh0xua9ghtEQtFtf4NJdx1zZcnm5'
    CONSUMER_KEY = 'cDOqVRVhKcg2uFzcXHGrdttXC'
    CONSUMER_SECRET = 'Mab1X0vQg3isdXcjfxebPod6NV1VwNUDPOAevzA6yM0TVDjC2F'

    # Setup access to API
    def connect_to_twitter_OAuth(self):
        auth = tweepy.OAuthHandler(Twitter.CONSUMER_KEY, Twitter.CONSUMER_SECRET)
        auth.set_access_token(Twitter.ACCESS_TOKEN, Twitter.ACCESS_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        logger = logging.getLogger()
        try:
            self.api.verify_credentials()
        except Exception as e:
            logger.error("Error creating API", exc_info=True)
            raise e
        logger.info("API created")
        return self.api


    def get_recent_tweet(self, query, language, count=100):
        query = query + " -filter:retweets"
        fetched_tweets = tweepy.Cursor(self.api.search, q=query, lang=language, tweet_mode='extended', result_type='recent').items(count)
        users_tweets = list()
        for tweet in fetched_tweets:
            users_tweets.append([tweet.user.screen_name, tweet.full_text, tweet.created_at, tweet.lang])
        df = pd.DataFrame(data=users_tweets, columns=["user", "text", "created_at", "lang"])
        return df
    

    def get_user_tweet(self, username, count=100):
        fetched_tweets = tweepy.Cursor(self.api.user_timeline, screen_name=username, exclude_replies=True, tweet_mode='extended').items(count)
        users_tweets = list()
        for tweet in fetched_tweets:
            users_tweets.append([tweet.user.screen_name, tweet.full_text, tweet.created_at, tweet.lang])
        df = pd.DataFrame(data=users_tweets, columns=["user", "text", "created_at", "lang"])
        return df


    def df_to_csv(self, df):
        df.to_csv("tweets.csv", encoding="utf-8")


if __name__ == '__main__':
    twitter = Twitter()
    twitter.connect_to_twitter_OAuth()
    data = twitter.get_recent_tweet(query="خامنه ای", language="fa", count=200)
    # user_data = twitter.get_user_tweet(username='mh___mp98', count=50)
    twitter.df_to_csv(data)
