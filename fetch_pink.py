import requests
import pandas as pd
import re
import json
from fetch_tweets import main
import asyncio
import time
class PinkSaleData:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,es;q=0.7,fr;q=0.6',
            # Add other headers as needed
        }
        self.response = self.fetch_data()

    def fetch_data(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

    def process_data(self):
        df = pd.DataFrame(self.response['data'])
        df['chain'] = [df['currency'][i]['symbol'] for i in range(len(df))]
        df_normalized = pd.json_normalize(df['token'])
        df_result = pd.concat([df, df_normalized], axis=1)
        df_result = df_result.drop('token', axis=1)
        df_normalized_pool = pd.json_normalize(df['pool'])
        df_normalized_pool = df_normalized_pool.drop('initialMarketCap', axis=1)
        df_all = pd.concat([df_result, df_normalized_pool], axis=1)
        df_all['Startdate'] = pd.to_datetime(df_all['startTime'], unit='s')
        df_all['Endate'] = pd.to_datetime(df_all['endTime'], unit='s')
        df_all['publicSaleStartTime'] = df_all['publicSaleStartTime'].fillna(0)
        df_all = df_all.sort_values('Startdate', ascending=False).reset_index(drop=True)

        twitter_usernames = []

        for j in range(len(df_all)):
            try:
                data = json.loads(df_all['poolDetails'][j])
                found_twitter_username = False

                for value in data.values():
                    match = re.search(r'https://twitter.com/(\w+)', value)
                    if match:
                        twitter_username = match.group(1)
                        if len(twitter_username) > 0:
                            twitter_usernames.append(twitter_username)
                            found_twitter_username = True
                        else:
                            twitter_usernames.append(None)
                        break

                if not found_twitter_username:
                    twitter_usernames.append(None)
            except Exception as e:
                twitter_usernames.append(None)

        df_all['twitter_usernames'] = twitter_usernames
        df_all['initialMarketCapUsd'] = pd.to_numeric(df_all['initialMarketCap'], errors='coerce', downcast='float')
        df_all['telegramOnline%'] = df_all.telegramOnlineCount/ df_all.telegramMemberCount
        df_all = df_all.fillna(0)
        df_all = df_all.reset_index()
        df_all.twitter_usernames = df_all.twitter_usernames.astype(str)
        #print(df_all.twitter_usernames)
        df_all.twitter_usernames = df_all.twitter_usernames.str.lower()
        df_all = df_all.iloc[:3]
        tweets_df = []
        for i in df_all.twitter_usernames:
            tweets_df.append(asyncio.run(main(i)))
            time.sleep(2)
        
        tweets_df = pd.concat(tweets_df)
       #print(tweets_df)
        p_d = pd.merge(tweets_df, df_all, how='right', on='twitter_usernames').fillna(0)
        #print(p_d)

        return p_d
    


# Example usage
#url = 'https://pinksale-trending.s3.ap-northeast-1.amazonaws.com/active.json'
#pink_sale_data = PinkSaleData(url)
#processed_data = pink_sale_data.process_data()
#processed_data.to_csv('pink_sale_data.csv', index=False)
# Display the processed data
#print(processed_data)
