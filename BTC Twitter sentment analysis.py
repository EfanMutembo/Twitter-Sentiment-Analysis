#!/usr/bin/env python
# coding: utf-8

# # 1 . Authenticate to Twitter

# In[1]:


import tweepy as tw
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# In[2]:


get_ipython().run_line_magic('store', '-r bearer_token')
#initialize client
client = tw.Client(bearer_token=bearer_token)


# # 2. Get Tweets
# - Collect the sentiment(tweets) of each day fro the past seven days at 2400
# - Collect the varying sentiment over a day at 4 ifeent times of day
# 
# 0600,1200,1800,2400

# In[3]:


import datetime

# get current time and start time (14 days ago)
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
start_time = yesterday.replace(hour=20,minute=0, second=0, microsecond=0)


# format start time string for Twitter API
start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")


# In[37]:



#Create a query
query = '#BTC #bitcoin -is:retweet -eth -ETH -#ETH'


#Send the request through the client method
response = (tw.Paginator(client.search_recent_tweets,query=query,end_time = start_time  ,
                              tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=150))


# In[38]:


#Unpack the api response into a dictionary
tweets= [{'Tweets':tweet.text,'Timestamp':tweet.created_at} for tweet in response]


# Im trying to make the call 7 times with diferent end time each time
# - Trouble unpacking the gen obj

# # 3. Preprocess
# - Clean the tweets
# - Lematize words
# 
# Lematize is reducing a word to base form. Walks walking walked get turned to Walk. Making it easier to analyze

# In[39]:


df = pd.DataFrame.from_dict(tweets)
df.head()


# In[40]:


df.shape


# In[41]:


#import libs
import nltk
from nltk.corpus import stopwords
from textblob import Word, TextBlob


# In[42]:


nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
stop_words = [stopwords.words('english')]
custom_stopwords = ['#','RT','crypto']


# In[43]:


def preprocess_tweets(tweet, custom_stopwords):
    processed_tweet = tweet
    processed_tweet.replace('[^\w\s]', '')
    processed_tweet = " ".join(word for word in processed_tweet.split() if word not in stop_words)
    processed_tweet = " ".join(word for word in processed_tweet.split() if word not in custom_stopwords)
    processed_tweet = " ".join(Word(word).lemmatize() for word in processed_tweet.split())
    return(processed_tweet)

df['Processed Tweet'] = df['Tweets'].apply(lambda x: preprocess_tweets(x, custom_stopwords))
df.head()


# # 4. Calculate Sentiment
# - Get Polarity and Subjectivity
# 
# **Polarity** : Negative or Positive
# 
# **Subjectivity**: How much based on emotion is the tweet

# In[44]:


df['polarity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[0])
df['subjectivity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[1])


# In[45]:


df.head()


# In[46]:


df.shape


# In[47]:


df.describe()


# # 5. Vizualize

# In[48]:


#make a moving average for sentiment

btc = df[['Timestamp', 'polarity']]
btc = btc.sort_values(by='Timestamp', ascending=True)
btc['MA Polarity'] = btc.polarity.rolling(10, min_periods=3).mean()


# In[49]:


btc.head()


# In[50]:


#plot the MA polarity
fig,ax = plt.subplots(figsize=(15,8))
ax.plot(btc['Timestamp'],btc['MA Polarity'])
ax.set_title('Bitcoin Moving Average Polarity',fontsize = 25);
ax.set_ylabel('Polarity',fontsize = 20);
ax.set_xlabel('Time',fontsize = 20);


# # 6. Compare With BTC price
# - Collect BTC price data
# - Make sure the data is from the same time period as the tweets

# In[51]:


#Get the tweets time range
start_range = df['Timestamp'].iloc[-1].round('min')
end_range = df['Timestamp'][0].round('min')

# Format the timestamp
formatted_start_range = start_range.strftime("%Y-%m-%d %H:%M:%S")
formatted_end_range = end_range.strftime("%Y-%m-%d %H:%M:%S")

#Set the API hours variable based on the tweets end_range
API_hours = end_range.round('H').hour+1


# In[52]:


#Get the price data from API

import requests
import time

#get data from api

url = 'https://min-api.cryptocompare.com/data/v2/histominute'

start_time = yesterday.replace(hour=API_hours,minute=0, second=0, microsecond=0)

# set the parameters for the API request
params = {
    'fsym': 'BTC',
    'tsym': 'USD',
    'limit': 1400,  # number of minutes to retrieve
    'aggregate': 1,  # granularity of the data (1 = 1 minute)
    'toTs': int(time.mktime(start_time.timetuple()))
}

response = requests.get(url, params=params)
data = response.json()['Data']['Data']
df_price = pd.DataFrame(data = data)


df_price['time'] = pd.to_datetime(df_price['time'], unit='s')


# In[53]:


#get the index in the price df of values we want
start_of_tweets = df_price['time'][df_price['time'] == formatted_start_range].index.item()
end_of_tweets = df_price['time'][df_price['time'] == formatted_end_range].index.item()


# In[54]:


#Get a slice of the price df corresponding to the tweets time range
df_slice = df_price.iloc[start_of_tweets:end_of_tweets]
df_slice.head()


# In[55]:


#Plot graph of 

fig,ax = plt.subplots(2,1,figsize=(13,10))

#plot price
ax[0].plot(df_slice['time'],df_slice['close']);
ax[0].set_title('BTC Price - USD',fontsize=20);

#plot sentiment
ax[1].plot(btc['Timestamp'],btc['MA Polarity'])
ax[1].set_title('Bitcoin Moving Average Polarity',fontsize = 25);
ax[1].set_ylabel('Polarity',fontsize = 20);
ax[1].set_xlabel('Time',fontsize = 20);


# In[ ]:





# In[ ]:




