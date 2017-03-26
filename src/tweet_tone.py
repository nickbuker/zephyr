# -*- coding: utf-8 -*-
import json
from watson_developer_cloud import ToneAnalyzerV3

# vector analysis
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# BEGIN of python-dotenv section
import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import os


def find_risk(tweet, tone_analyzer):

    # crisis is a determined experimentally by analzing tweets
    # for sentiments that reflect when a person may be depressed
    # or otherwise at risk

    # ['Anger', 'Disgust', 'Fear', 'Joy', 'Sadness']
    crisis = np.array([0.02, 0.04, 0.01, 0, 0.93]).reshape(1, -1)

    json_response = tone_analyzer.tone(text=tweet)
    tones_json = json_response['document_tone']['tone_categories'][0]['tones']
    sentiment = np.array([d['score'] for d in tones_json]).reshape(1, -1)
    # return sentiment

    # Find cosine similarity between sentiment of current tweet
    # and crisis vector
    risk = cosine_similarity(crisis, sentiment)[0][0]
    return round(risk,4)


def process_feed(tweet_list):
    # takes a list(/feed) of dictionaries of tweet data
    # adds risk score to each item in the list(/feed)

    load_dotenv(find_dotenv())
    tone_analyzer = ToneAnalyzerV3(
       username=os.environ.get("TONE_USERNAME"),
       password=os.environ.get("TONE_PASSWORD"),
       version='2016-05-19')

    for tweet in tweet_list:
        tweet['risk'] = find_risk(tweet['text'], tone_analyzer)


def main():

    load_dotenv(find_dotenv())
    tone_analyzer = ToneAnalyzerV3(
       username=os.environ.get("TONE_USERNAME"),
       password=os.environ.get("TONE_PASSWORD"),
       version='2016-05-19')

    test_tweet = 'suicide die pain misery myself'
    # test_tweet = 'ight. "hello there, gar'

    print(find_risk(test_tweet, tone_analyzer))

if __name__ == '__main__':
    main()
