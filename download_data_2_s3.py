#import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from fetch_pink import PinkSaleData
from fetch_tweets import main
import boto3
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def fetch_and_process_data(url):
    try:
        pink_sale_data = PinkSaleData(url)
        processed_data = pink_sale_data.process_data()
        #processed_data = pd.read_csv('/Users/steven/nap/Scraping/pink_sale_data.csv')
        return processed_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = os.getenv('BUCKET_NAME')
csv_path = 'pinksale.csv'  # Path to your local CSV file

url = 'https://pinksale-trending.s3.ap-northeast-1.amazonaws.com/active.json'

# Call the function and retrieve the processed data
#df = fetch_and_process_data(url)
df = pd.read_csv( '/Users/steven/nap/Scraping/pinksale.csv')
df.twitter_last_tweet = df.twitter_last_tweet.astype(str)
df['Relative Engagement Metrics'] = ((df.twitter_mean_rt_post + df.twitter_mean_like + df.twitter_replied_count) / df.twitter_followers_count).fillna(0)
df['Interactive Engagement Ratio'] = (df.twitter_replied_count / (df.twitter_mean_rt_post + df.twitter_mean_like)).fillna(0)
df['Recent Engagement Trend'] = ((df.twitter_ld_mean_rt_post + df.twitter_ld_mean_like) / (df.twitter_mean_rt_post + df.twitter_mean_like)).fillna(0)
df['Temporal Engagement Analysis'] = ((df.twitter_mean_rt_post + df.twitter_mean_like) / (df.twitter_ld_mean_rt_post + df.twitter_ld_mean_like)).replace([np.inf, -np.inf], np.nan).fillna(0)
df['Cross-Platform Engagement Index'] = ((df.twitter_mean_rt_post + df.telegramOnlineCount) / (df.twitter_followers_count + df.telegramMemberCount)).fillna(0)
df['Telegram Engagement Percentage'] = (df.telegramOnlineCount / df.telegramMemberCount * 100).fillna(0).round(2)

hasKyc = np.where(df['hasKyc'] == False, 1,0)
hasAudit = np.where(df['hasAudit'] == False, 1,0)
hasSafu = np.where(df['hasSafu'] == False, 1,0)
df['Compliance and Sentiment Impact'] = (hasKyc+hasAudit+hasSafu) * (df.twitter_mean_rt_post*df.twitter_mean_like*df.twitter_mean_view)
df['Fundraising Event Impact'] = (df.formattedTotalRaised / (df.twitter_mean_rt_post + df.twitter_mean_like)).replace([np.inf, -np.inf], np.nan).fillna(0)
df['hasUrl'] = df['whitelistApprobationLink'].fillna('').str.contains(r'https?://\S+').astype(int)
df['Whitelist and Affiliate Influence'] = (df.twitter_mean_rt_post*df.twitter_mean_like*df.twitter_mean_view) * df.affiliateBps + df.hasUrl

df.to_csv(csv_path, index=False)

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_path)

# Convert DataFrame to CSV format in memory
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

# Upload the CSV data to the S3 bucket
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
s3.put_object(Body=csv_data, Bucket=bucket_name, Key='pinksale.csv')

print(f"CSV file has been uploaded to S3 bucket: {bucket_name}")