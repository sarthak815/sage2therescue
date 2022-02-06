import tweepy
import pandas as pd
import csv
import re 
import string
import preprocessor as p
import pickle
from transformers import TFDistilBertForSequenceClassification, DistilBertTokenizerFast
import numpy as np
import tensorflow as tf
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import spacy
from iso3166 import countries

class TweetScraper:
    def __init__(self):
        self.consumer_key = 'gN7E6RbXXOqm389hzN23PZFBb'
        self.consumer_secret = 'MvG8vNbp6et4b0ZO6fJcCRcYYx7I4YPSaaNK1Ckn9aG9doGFbL'
        self.access_key= '80507337-VfyQTELYTH5go54ZwR8pPRgn1JPxB6Yx60akNjDRo'
        self.access_secret = 'CZ8in6tw3DOsVEH3QIzRWU4OYy8qRLH8A9xifUi4H84gN'
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(self.auth,wait_on_rate_limit=True)
        
    def scrapeTwitter(self, query, count=1000):
        try:
            tweets = tweepy.Cursor(self.api.search_tweets, q=query).items(count)
            tweets_list = [[tweet.created_at, tweet.id, tweet.text,tweet.user.location] for tweet in tweets]
            tweets_df = pd.DataFrame(tweets_list)
            tweets_df.columns = ["Date", "ID", "Text", "Location"]
        except BaseException as e:
            tweets_df = pd.DataFrame({"Error": [str(e)]})
        return tweets_df

class DetectionModel:
    def __init__(self, model_path='svc.pb', scaler_path='scaler.pb'):
        self.disaster_detection_model = pickle.load(open(model_path, 'rb'))
        self.nlp = spacy.load("en_core_web_lg")
        self.scaler = pickle.load(open(scaler_path, 'rb'))
        
    def predictTweets(self, sentences):
        tweet_vectors = np.array([self.nlp(sentence).vector for sentence in sentences])
        tweet_vectors_scaled = self.scaler.transform(tweet_vectors.astype(np.float32))
        predictions = self.disaster_detection_model.predict(tweet_vectors_scaled)
        return predictions

class SAModel:
    def __init__(self):
        # self.device = cuda.get_current_device()
        # self.device.reset()
        self.tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
        self.model = TFDistilBertForSequenceClassification.from_pretrained('./SAModel/saved_model/', local_files_only=True)
    def predictTweets(self, sentences):
        test_encodings = self.tokenizer(sentences, truncation=True, padding=True)
        test_dataset = tf.data.Dataset.from_tensor_slices((
            dict(test_encodings), np.array([1 for _ in range(len(sentences))])
        ))
        results = self.model.predict(test_dataset).logits
        results = 1/(1+np.exp(-results))
        return 2*results.T[1]-1

class LocationExtractor:
    def __init__(self, default_loc=''):
        self.nlp_wk = spacy.load('xx_ent_wiki_sm')
        self.default_loc = default_loc
        self.countries = [str(i.name) for i in countries]
        
    def preprocess(self, sentence):
        return ' '.join([i for i in sentence.split() if not i.startswith('@')])
    
    def extractLocations(self, sentences, prev_locations=None):
        locations, location_flags = [], []
        for index, sentence in enumerate(sentences):
            doc = self.nlp_wk(self.preprocess(sentence))
            loc = ' '.join([str(ent) for ent in doc.ents if ent.label_ in ['LOC']])
            loc = ' '.join([i for i in loc.split() if i not in self.countries])
            if loc.strip() == '':
                if prev_locations is None:
                    locations.append(self.default_loc)
                    location_flags.append(False)
                else:
                    locations.append(prev_locations[index])
                    location_flags.append(True)
            else:
                locations.append(loc)
                location_flags.append(False)
        return locations, location_flags

def scrape_and_get(query, p_loc=0.25):
    ts = TweetScraper()
    dm = DetectionModel()
    sa = SAModel()
    le = LocationExtractor()
    
    tweets_df = ts.scrapeTwitter(query)
    tweets = [sentence for sentence in tweets_df["Text"]]
    disaster_or_not = dm.predictTweets(tweets)
    sentiment_scores = sa.predictTweets(tweets)
    locations, location_flags = le.extractLocations(tweets, [i for i in tweets_df["Location"]])
    
    loc_scores = {'locations': [], 'Sentiment': []}
    for index in range(len(locations)):
        if disaster_or_not[index]==1:
            if locations[index] not in loc_scores['locations']:
                loc_scores['locations'].append(locations[index])
                if location_flags[index]:
                    loc_scores['Sentiment'].append(sentiment_scores[index]*p_loc)
                else:
                    loc_scores['Sentiment'].append(sentiment_scores[index])
            else:
                present_index = loc_scores['locations'].index(locations[index])
                if location_flags[index]:
                    loc_scores['Sentiment'][present_index] += sentiment_scores[index]*p_loc
                else:
                    loc_scores['Sentiment'][present_index] += sentiment_scores[index]
    min_value = min(loc_scores['Sentiment'])
    max_value = max(loc_scores['Sentiment'])
    loc_scores['Sentiment'] = np.array(loc_scores['Sentiment'])
    if max_value != min_value:
        loc_scores['Sentiment'] = ((loc_scores['Sentiment'] - min_value)/(max_value - min_value))*-9+10
    else:
        loc_scores['Sentiment'] = loc_scores['Sentiment']*0+5
    loc_scores['Sentiment'] = [round(i, 2) for i in loc_scores['Sentiment']] 
    df = pd.DataFrame(loc_scores)
    return df

if __name__ == '__main__':
    df = scrape_and_get(query='Odisha')
    print(df)