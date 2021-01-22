import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

from twitter import Twitter

st.title("AUT Twitter Dashboard")
st.sidebar.title("AUT Twitter Dashboard")

st.markdown("This application is a dashboard used to analyze tweets 🐦")
st.sidebar.markdown("This application is a dashboard used to analyze tweets 🐦")

st.sidebar.subheader("Search Business")
tweet_type = st.sidebar.radio('Search By', ('keywords', 'username'))
tweet_lang = st.sidebar.radio('Tweets Language', ('FA', 'EN'))
user_input = st.sidebar.text_input(f'Enter {tweet_type} please:', key=1)

# Load Data
@st.cache(persist=True)
def load_data():
    twitter = Twitter()
    twitter.connect_to_twitter_OAuth()
    if tweet_type == 'keywords':
        data = twitter.get_recent_tweet(query=user_input, language=tweet_lang.lower(), count=100)
    elif tweet_type == 'username':
        data = twitter.get_user_tweet(username=user_input, count=100)

    return data

if user_input:
    data = load_data()
    st.write(data)


st.sidebar.subheader("Menu")
analyze_type = st.sidebar.radio('',('Exploratory data analysis', 'Sentiment Analysis', 'Topic Detection', 'Named Entity Recognition'))