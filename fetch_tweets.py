import asyncio
from twscrape import API, gather
import csv
import json
import pandas as pd
from datetime import datetime, timezone, timedelta

def prepro_tweets(df):
    last_tweet = datetime.now().replace(tzinfo=timezone.utc) - pd.to_datetime(df.date[-1])
    mean_rt_post, mean_like, mean_view, replied_count = df.agg({'retweetCount':'mean','likeCount':'mean','viewCount':'mean','replyCount':'mean'}).round()
    ld_mean_rt_post, ld_mean_like, ld_mean_view , ld_replied_count = df.resample('d').agg({'retweetCount':'mean','likeCount':'mean','viewCount':'mean','replyCount':'mean'}).round().iloc[-1]
    return last_tweet , mean_rt_post, mean_like, mean_view, replied_count, ld_mean_rt_post, ld_mean_like, ld_mean_view, ld_replied_count

async def main(username):
    try:
        api = API()
        user_login = username
        print(user_login)
        users = await api.user_by_login(user_login)
        print(users.username, users.id, users.followersCount, users.friendsCount, users.favouritesCount, users.statusesCount, users.verified)
        tweets_timeline = await gather(api.user_tweets_and_replies(users.id, limit=10))
        df = pd.DataFrame(tweets_timeline)
        df.to_csv('tweets.csv')
        df = df[(df['url'].str.lower().str.startswith(f'https://twitter.com/{user_login}/status/'))]
        df.retweetedTweet = df.retweetedTweet.fillna(0)
        df = df[df.retweetedTweet == 0]
        #print(df)
        df = df.sort_values('date').reset_index(drop=True)
        df.index = df.date
        df.index = pd.to_datetime(df.index)
        last_tweet, mean_rt_post, mean_like, mean_view, replied_count, ld_mean_rt_post, ld_mean_like, ld_mean_view, ld_replied_count = prepro_tweets(df)
        tweets_tw = {'twitter_usernames': user_login,
                     'twitter_last_tweet': last_tweet,
                     'twitter_mean_rt_post': mean_rt_post,
                     'twitter_mean_like': mean_like,
                     'twitter_mean_view': mean_view,
                     'twitter_replied_count': replied_count,
                     'twitter_ld_mean_rt_post': ld_mean_rt_post,
                     'twitter_ld_mean_like': ld_mean_like,
                     'twitter_ld_mean_view': ld_mean_view,
                     'twitter_ld_replied_count': ld_replied_count,
                     'twitter_followers_count': users.followersCount,
                     'twitter_friends_count': users.friendsCount,
                     'twitter_verified': users.verified
                     }
        tweets_tw = pd.DataFrame(tweets_tw, index=[0])
        print(tweets_tw)
        #tweets_tw.to_csv("tweet_data.csv", mode='a', header=False, index=False)
        return tweets_tw
    except Exception as e:
        print(f"Error fetching data for username {username}: {str(e)}")
        tweets_tw = {'twitter_usernames': "none",
                     'twitter_last_tweet': "none",
                     'twitter_mean_rt_post': "none",
                     'twitter_mean_like': "none",
                     'twitter_mean_view': "none",
                     'twitter_replied_count': "none",
                     'twitter_ld_mean_rt_post': "none",
                     'twitter_ld_mean_like': "none",
                     'twitter_ld_mean_view': "none",
                     'twitter_ld_replied_count': "none",
                     'twitter_followers_count': "none",
                     'twitter_friends_count': "none",
                     'twitter_verified': "none"
                     }
        tweets_tw = pd.DataFrame(tweets_tw, index=[0])
        # Return DataFrame with None values for all columns
        print(tweets_tw)
        return tweets_tw

#if __name__ == "__main__":
    #username = "laavaai"
    #asyncio.run(main(username))
