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


def find_risk(tweet, tone_analyzer, testing=False):

    # crisis vector is determined experimentally by analzing tweets
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
    risk = round(risk,4)
    if testing == True:
        emotion = 'Ang Disg Fear Joy Sad'
        sentiment = [round(float(s),4) for s in sentiment[0]]
        risk = 'emotion: {}\ncrisis:  {}\ntweet: {}\nrisk score: {}'\
                .format(emotion, crisis[0], sentiment, risk)

    return risk


def process_feed(tweet_list, testing=False):
    # takes a list(/feed) of dictionaries of tweet data
    # adds risk score to each item in the list(/feed)

    load_dotenv(find_dotenv())
    tone_analyzer = ToneAnalyzerV3(
       username=os.environ.get("TONE_USERNAME"),
       password=os.environ.get("TONE_PASSWORD"),
       version='2016-05-19')

    for tweet in tweet_list:
        risk = find_risk(tweet['text'], tone_analyzer)
        tweet['risk'] = risk
        if testing == True:
            print(tweet['text'],'\n',risk)

    return tweet_list

def main():

    # load_dotenv(find_dotenv())
    # tone_analyzer = ToneAnalyzerV3(
    #    username=os.environ.get("TONE_USERNAME"),
    #    password=os.environ.get("TONE_PASSWORD"),
    #    version='2016-05-19')
    #
    # # test_tweet = 'suicide die pain misery myself me I'
    # # test_tweet = 'ight. "hello there, elizabe'
    # test_tweet = 'anger sadness'
    # print(find_risk(test_tweet, tone_analyzer, testing=True))


    test_list = [{'name':'bob', 'text':'first tweet', 'date_time':'20170326', 'location':'<street adress>'},
    {'name':'bob', 'text':'i am posting another tweet', 'date_time':'20170326', 'location':'<street adress>'},
    {'name':'bob', 'text':'i feel sad', 'date_time':'20170326', 'location':'<street adress>'},
    {'name':'bob', 'text':'misery!!!', 'date_time':'20170326', 'location':'<street adress>'},
    {'name':'bob', 'text':'my friend invited me to a picnic, and now I am happy', 'date_time':'20170326', 'location':'<street adress>'}]

    process_feed(test_list, testing=True)


if __name__ == '__main__':
    main()
