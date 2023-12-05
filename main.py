import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
# Function to simulate login
from fetch_pink import PinkSaleData
from fetch_tweets import main
import asyncio

@st.cache_data
def authenticate(password):
    return password == '1234'

@st.cache_data(ttl=86400)  # Time-to-live set to 24 hours (86400 seconds)
def fetch_and_process_data(url):
    try:
        pink_sale_data = PinkSaleData(url)
        processed_data = pink_sale_data.process_data()
        #processed_data = pd.read_csv('/Users/steven/nap/Scraping/pink_sale_data.csv')
        return processed_data
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Initialize session state
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

# Page configuration
st.set_page_config(
    page_title="Caching Login",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Sidebar
st.sidebar.title("Login")

# Username and Password input
password = st.sidebar.text_input("Enter Password", type="password")

# Login button
if st.sidebar.button("Login"):
    if authenticate(password):
        st.session_state.is_authenticated = True
        st.success("🎉 Successfully logged in!")
    else:
        st.error("❌ Incorrect password. Please try again.")

# Check if the user is authenticated before displaying the main content
if st.session_state.is_authenticated:
    st.title("Welcome to Pinksale Pre Sales !")
    st.sidebar.title('Filter Options')
    # URL of the data source
    url = 'https://pinksale-trending.s3.ap-northeast-1.amazonaws.com/active.json'

    # Call the function and retrieve the processed data
    df = fetch_and_process_data(url)
    df.twitter_last_tweet = df.twitter_last_tweet.astype(str)

    # Read the DataFrame
    #df = pd.read_csv('/Users/steven/nap/pink_proj/pink_sale_data.csv')

    now = datetime.now()
    df['Startdate'] = pd.to_datetime(df['Startdate'], errors='coerce')

    # Filter conditions for dates
    live_dates = df['Startdate'] <= now
    today = now.date()
    today_dates = df['Startdate'].dt.date == today
    tomorrow = today + timedelta(days=1)
    tomorrow_dates = df['Startdate'].dt.date == tomorrow
    future_dates = df['Startdate'] > np.datetime64(tomorrow)

    # Additional filter based on dates
    date_filter = st.sidebar.selectbox('Date Filter', ['All', 'Live', 'Today', 'Tomorrow', 'Future'])

    # Apply date filter
    if date_filter == 'Live':
        df = df[live_dates]
    elif date_filter == 'Today':
        df = df[today_dates]
    elif date_filter == 'Tomorrow':
        df = df[tomorrow_dates]
    elif date_filter == 'Future':
        df = df[future_dates]

        
    kyc_options = ['None', 'Yes', 'No']
    audit_options = ['None', 'Yes', 'No']
    safu_options = ['None', 'Yes', 'No']
    pool_options = ['None','FL', 'Presale', 'Subscription', 'Auction']

    # Filters
    kyc = st.sidebar.selectbox('KYC', kyc_options)
    audit = st.sidebar.selectbox('Audit', audit_options)
    safu = st.sidebar.selectbox('Safu', safu_options)
    pools = st.sidebar.selectbox('Pool type', pool_options)

    # Build the query string
    query_str = ""

    # KYC filter
    if kyc != 'None':
        query_str += f"hasKyc == {kyc == 'Yes'}"

    # Audit filter
    if audit != 'None':
        if query_str:
            query_str += " and "
        query_str += f"hasAudit == {audit == 'Yes'}"

    # Safu filter
    if safu != 'None':
        if query_str:
            query_str += " and "
        query_str += f"hasSafu == {safu == 'Yes'}"

    if pools != 'None':
        if query_str:
            query_str += " and "
        query_str += f"poolType == '{pools}'"

    # Apply the filter
    if query_str:
        df = df.query(query_str)



  
    # Allow user to select multiple columns
    predefined_columns = ['name', 'telegramMemberCount']  # Add your column names here

    # Allow the user to select multiple columns with predefined values
    selected_columns = st.sidebar.multiselect('Select Columns', df.columns, default=predefined_columns)

    # Display the selected columns
    if selected_columns:
        filtered_df = df[selected_columns]
        st.dataframe(filtered_df)
    else:
        st.warning('Please select at least one column.')