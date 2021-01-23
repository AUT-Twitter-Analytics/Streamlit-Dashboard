import re

import hazm
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit import caching
from wordcloud import STOPWORDS
from wordcloud_fa import WordCloudFa

from twitter import Twitter

st.title("AUT Twitter Dashboard")
st.sidebar.title("AUT Twitter Dashboard")
st.sidebar.markdown("This application is a dashboard used to analyze tweets 🐦")

# Search Section in Sidebar
st.sidebar.subheader("Search")
tweet_type = st.sidebar.radio('Search By', ('keywords', 'username'))
tweet_lang = st.sidebar.radio('Tweets Language', ('FA', 'EN'))
user_input = st.sidebar.text_input(f'Enter {tweet_type} and press ENTER to apply', key=1)

# Menu Section in Sidebar
st.sidebar.subheader("Menu")
analyze_type = st.sidebar.radio('Extracting Information By',('Exploratory Data Analysis', 'Sentiment Analysis', 'Topic Detection', 'Named Entity Recognition'))

# Load Data
@st.cache(allow_output_mutation=True)
def load_data():
    twitter = Twitter()
    twitter.connect_to_twitter_OAuth()
    if tweet_type == 'keywords':
        data = twitter.get_recent_tweet(query=user_input, language=tweet_lang.lower(), count=100)
    elif tweet_type == 'username':
        data = twitter.get_user_tweet(username=user_input, count=100)

    return data

if user_input != '':
    data = load_data()

    # Exploratory Data Analysis
    if analyze_type == 'Exploratory Data Analysis':
        st.markdown('## Exploratory Data Analysis:')
        st.markdown('## Fetched Data')
        st.write(data)

        # Random Tweet
        st.markdown('## Random Tweet')
        random_tweet = st.button('Show another random tweet')
        st.markdown(f'{data[["text"]].sample(n=1).iat[0, 0]}')

        # WordCloud
        st.markdown('## Wordcloud')
        words = ' '.join(data['text'])
        words = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))', '', words, flags=re.MULTILINE)
        words = re.sub(r"@(\w+)", ' ', words, flags=re.MULTILINE)

        if tweet_lang == 'FA':
            pn = True
            stopwords = hazm.stopwords_list()
        elif tweet_lang == 'EN':
            pn = False
            stopwords = STOPWORDS
        wordcloud = WordCloudFa(persian_normalize=pn, stopwords=stopwords, include_numbers=False, background_color='white', width=700, height=500)
        frequencies = wordcloud.process_text(words)
        wc = wordcloud.generate_from_frequencies(frequencies)
        image = wc.to_image()
        st.image(image)
