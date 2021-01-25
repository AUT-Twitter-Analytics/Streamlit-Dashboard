import re
import string

import hazm
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit import caching
from wordcloud import STOPWORDS
from wordcloud_fa import WordCloudFa

from preprocess import Preprocess
from sentiment import sentiment_run
from topic import topic_run
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
        # Dataframe
        st.markdown('## **Data**')
        st.write(data)

        # Random Tweet
        col1, col2 = st.beta_columns(2)
        with col1:
            st.markdown('')
            st.markdown('')
            random_tweet = st.button('Show another random tweet')
        with col2:
            st.markdown('')
            st.markdown(f'{data[["text"]].sample(n=1).iat[0, 0]}')


        # WordCloud
        st.markdown('## **Wordcloud**')
        words = ' '.join(data['text'])
        punctuations_list = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''' + string.punctuation
        def remove_punctuations(text):
            translator = str.maketrans('', '', punctuations_list)
            return text.translate(translator)
        words = remove_punctuations(words)
        words = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))', '', words, flags=re.MULTILINE)
        words = re.sub(r"@(\w+)", ' ', words, flags=re.MULTILINE)
        wordcloud = WordCloudFa(persian_normalize=True, stopwords=list(STOPWORDS)+hazm.stopwords_list(), include_numbers=False, background_color='white', width=700, height=500)
        frequencies = wordcloud.process_text(words)
        wc = wordcloud.generate_from_frequencies(frequencies)
        image = wc.to_image()
        st.image(image)

            
    # Sentiment Analysis
    if analyze_type == 'Sentiment Analysis':
        st.markdown('## Sentiment Analysis:')
        if tweet_lang == 'FA':
            sentiment_data = sentiment_run(data, 'fa')
        elif tweet_lang == 'EN':
            sentiment_data = sentiment_run(data, 'en')
        
        sentiment_count = sentiment_data['sentiment'].value_counts()
        sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)

        st.markdown('## Data')
        st.write(sentiment_data)
        
        col1, col2 = st.beta_columns(2)
        with col1:
            st.markdown('')
            st.markdown('')
            random_tweet = st.button('Show another random tweet')
            tmp = sentiment_data[["text", "sentiment"]].sample(n=1)
        with col2:
            st.markdown('')
            st.markdown(f'**Text:**    {tmp.iat[0, 0]}')
            st.markdown(f'**Sentiment:**    {tmp.iat[0, 1]}')


    # Topic Detection
    if analyze_type == 'Topic Detection':
        st.markdown('## Topic Detection:')
        if tweet_lang == 'FA':
            topic_data = topic_run(data, 'fa')
        elif tweet_lang == 'EN':
            topic_data = topic_run(data, 'en')
        
        topic_count = topic_data['topic'].value_counts()
        topic_count = pd.DataFrame({'Topic':topic_count.index, 'Tweets':topic_count.values})

        fig = px.pie(topic_count, values='Tweets', names='Topic')
        st.plotly_chart(fig)

        fig = px.bar(topic_count, x='Topic', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)

        st.markdown('## **Data**')
        st.write(topic_data)
        

        col1, col2 = st.beta_columns(2)
        with col1:
            st.markdown('')
            st.markdown('')
            random_tweet = st.button('Show another random tweet')
            tmp = topic_data[["text", "topic"]].sample(n=1)
        with col2:
            st.markdown('')
            st.markdown(f'**Text:**    {tmp.iat[0, 0]}')
            st.markdown(f'**Topic:**    {tmp.iat[0, 1]}')
