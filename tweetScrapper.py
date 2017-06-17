import tweepy
import json
import sqlite3
import matplotlib.pyplot as plt
import config
import argparse

from google.cloud import language

CONSUMER_API_KEY = 'hTTAZaDzlEI1DBRMxZveZZo4u'
CONSUMER_API_KEY_SECRET = 'T128r6tfAheQaE2FlJHy40z05Jbtj0kMuHgmP1VxaQiCDIMyru'

TOKEN_KEY = '113699063-3CvqvLNgloQCRi3Fh0xbuOmDquAs4A8BNj5gpvSX'
TOKEN_KEY_SECRET ='Lt9Way7b6RVuEIHi7Qcon7tGWfxeef4FImwX6Y5o6U36W'

conn = sqlite3.connect('Madridtweets.db')

positives = 0
negetives = 0


class sentimentAnalyser:
    @staticmethod
    def print_result(annotations):
        score = annotations.sentiment.score
        magnitude = annotations.sentiment.magnitude

        for index, sentence in enumerate(annotations.sentences):
            sentence_sentiment = sentence.sentiment.score
            print('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))

        print('Overall Sentiment: score of {} with magnitude of {}'.format(score, magnitude))
        return 0

    @staticmethod
    def analyze(tweet_text):
        language_client = language.Client()

        document = language_client.document_from_text(tweet_text.decode('utf-8'))

        # Detects sentiment in the document.
        #annotations = document.annotate_text(include_sentiment=True,include_syntax=False,include_entities=False)

        sentiment = document.analyze_sentiment().sentiment

        global positives, negetives
        if(sentiment.score > 0):
            positives= positives+1
        else:
            negetives=negetives+1


        print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
        # Print the results
        #obj = sentimentAnalyser()
        #obj.print_result(annotations)
        return True



# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        tweet_text = decoded['text'].encode('ascii', 'ignore')
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print('@%s: %s' % (decoded['user']['screen_name'], tweet_text ))
        obj = sentimentAnalyser()
        obj.analyze(tweet_text)
        print('')
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_API_KEY_SECRET)
    auth.set_access_token(TOKEN_KEY, TOKEN_KEY_SECRET)

    print("Showing all new tweets for the filtered channel" )
        # There are different kinds of streams: public stream, user stream, multi-user streams
    stream = tweepy.Stream(auth, l)
    stream.filter(track=config.TRACK_TERMS)


    labels = 'Positive', 'Negetive'
    sizes = [positives, negetives]
    explode = (0.1, 0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.pause(0.05)







