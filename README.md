# Twitter-Sentiment-Analysis
### Poject Summary: Sentiment Analysis of Bitcoin Tweets and Price Visualization

This project focuses on analyzing the sentiment of tweets related to Bitcoin (BTC) and visualizing its price movement.

### Project Aim:
The project aims to provide insights into the sentiment surrounding Bitcoin on Twitter and its potential correlation with price movements. The sentiment analysis can help understand the general sentiment towards Bitcoin, while the visualization allows for the observation of sentiment trends over time. Comparing sentiment with BTC price can provide additional context and potential relationships between sentiment and market dynamics.


## Project Flow:


1. Authentication to Twitter: The code authenticates to Twitter using Tweepy and sets up the client with the provided bearer token.

2. Getting Tweets: The code retrieves tweets with specific criteria, such as hashtags and excluding retweets, using the Twitter API. It collects the sentiment of tweets from the past seven days at 2400 hours and at four different times of the day (0600, 1200, 1800, and 2400).

3. Preprocessing: The collected tweets are cleaned by removing stopwords, special characters, and custom stopwords. Lemmatization is applied to reduce words to their base form, making them easier to analyze.

4. Calculating Sentiment: The code uses the TextBlob library to calculate the polarity (negative or positive) and subjectivity (emotional intensity) of the preprocessed tweets.

5. Visualization: A moving average for the sentiment polarity is calculated and plotted over time. The sentiment analysis results are visualized using Matplotlib.

6. Comparing with BTC Price: The code retrieves BTC price data using the Cryptocompare API and matches it with the timestamp of the tweets. The BTC price data is then sliced and compared with the sentiment analysis results.


Please note that the code provided is a snippet, and additional implementation details and considerations may be required for a fully functional and comprehensive project.




