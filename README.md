# Gem Token Identifier

**Identify potential gem tokens through PinkSale and Twitter scraping**

## Introduction

This project aims to identify potentially lucrative "gem" tokens by scraping data from PinkSale and Twitter. Gem tokens are often newly launched, low-market-cap tokens that have the potential for significant growth. By monitoring PinkSale for upcoming token launches and analyzing Twitter sentiment around these tokens, we can uncover promising investment opportunities.

## Project Components

### 1. PinkSale Scraper

- The PinkSale scraper focuses on gathering information about upcoming token launches on the PinkSale platform.
- Utilizes web scraping techniques to extract details such as token names, launch dates, and initial market caps from PinkSale listings.
- Regularly updates the scraped data to ensure the latest information is available.

### 2. Twitter Scraper

- The Twitter scraper monitors social media sentiment around specific tokens identified from PinkSale.
- Employs Twitter API or web scraping to collect tweets related to the identified tokens.
- Analyzes the sentiment of tweets using natural language processing (NLP) techniques to gauge community interest and sentiment.

### 3. Data Analysis

- Combines data from PinkSale and Twitter to create a comprehensive dataset for analysis.
- Implements algorithms or machine learning models to identify patterns and trends that may indicate potential gem tokens.
- Considers factors such as launch success, community engagement, and sentiment analysis to rank tokens.

### 4. Notification System

- Develops a notification system to alert users when a potential gem token is identified.
- Notifications could include token details, launch date, and relevant Twitter sentiment metrics.

## Getting Started

### 1. Environment Setup

- Install the required Python libraries, including web scraping tools (e.g., Beautiful Soup, Scrapy), data analysis libraries (e.g., Pandas, NumPy), and NLP libraries (e.g., NLTK, TextBlob).

### 2. Configuration

- Set up configuration files for PinkSale and Twitter API credentials. Ensure proper authentication to access data from these platforms.

### 3. AWS Credentials

Create a `.env` file in the project root directory with your AWS credentials:

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
BUCKET_NAME=pinksales3

### 4. Streamlit Application

- Use a cron job to run every day download_data_2_s3.py file
- Use Streamlit to visualize and interact with the data. Run the application using the following command:
  
 
python3.10 download_data_2_s3.py

streamlit run main.py
