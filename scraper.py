import settings
import tweepy
import sqlite3
import dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError
import json

#db = dataset.connect(settings.CONNECTION_STRING)
create_table = "CREATE TABLE IF NOT EXISTS {} (userID text, tweet_text text, retweet text, polarity text, subjectivity text)".format(settings.TABLE_NAME)
conn = sqlite3.connect("CR7tweets.db")
cursor = conn.cursor()
if (cursor.execute(create_table)):
    print("Table created successfully")

class StreamListener(tweepy.StreamListener):
    def on_data(self, raw_data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(raw_data)
        tweet = json.loads(raw_data.strip())
        print("text : {} ".format(tweet.get('text')))
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users

    def on_status(self, status):
        if status.retweeted:
            return
        description = status.user.description
        #loc = status.user.location
        text = status.text
       # coords = status.coordinates
       # geo = status.geo
        name = status.user.screen_name
       # user_created = status.user.created_at
        #followers = status.user.followers_count
      #  id_str = status.id_str
       # created = status.created_at
        retweets = status.retweet_count
      #  bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment

        table = settings.TABLE_NAME
        try:
            insert_data = "INSERT INTO {} (userId, tweet_text,retweet, polarity, subjectivity) " \
                          "VALUES (?,?,?,?)"

            cursor.execute(insert_data, (1,text,retweets,sent.polarity, sent.subjectivity))
            conn.commit()
            conn.close()

        except ProgrammingError as err:
            print(err)

    def on_error(self, status_code):
        if status_code == 420:
            print("Stream disconnected")
            #returning False in on_data disconnects the stream
            return False

auth = tweepy.OAuthHandler(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
auth.set_access_token(settings.TWITTER_KEY, settings.TWITTER_SECRET)
api = tweepy.API(auth)

stream_listener = StreamListener()
stream = tweepy.Stream(auth=auth, listener=stream_listener)
stream.filter(track=settings.TRACK_TERMS, async=True)