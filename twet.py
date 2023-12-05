import asyncio
from twscrape import API, gather
import csv
import json
import pandas as pd
from datetime import datetime, timezone, timedelta


async def main():
    api = API()
    #tweets = await gather(api.list_timeline(1722925043104014749))
    #tweets = pd.DataFrame(tweets)
    #tweets.to_csv('list_tweets.csv')
    user_login = 'laavaai'
    users = await api.user_by_login(user_login)
    print(users.username, users.id, users.followersCount, users.friendsCount, users.favouritesCount, users.statusesCount, users.verified)
    tweets_timeline = await gather(api.user_tweets_and_replies(users.id, limit=20))
    df = pd.DataFrame(tweets_timeline)
    df.to_csv('tweets.csv')

if __name__ == "__main__":
    asyncio.run(main())
