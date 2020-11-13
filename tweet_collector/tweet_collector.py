import config
import sys
import os
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
from sqlalchemy import create_engine 
import psycopg2


# postgres authentification

HOST = os.getenv('PG_HOST')
USERNAME = os.getenv('PG_USERNAME')
PORT = os.getenv('PG_PORT')
DB = os.getenv('PG_DB')
PASSWORD = os.getenv('PG_PASSWORD')

#postgres engine
engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')

# Delete old table

DELETE_QUERY = ''' DROP TABLE IF EXISTS tweets ; '''
engine.execute(DELETE_QUERY) 

#Create table in the Postgres Database

CREATE_QUERY = ''' CREATE TABLE IF NOT EXISTS tweets
                   (
                    id SERIAL,
                    username VARCHAR(50),
                   text VARCHAR(500)
                   );'''

engine.execute(CREATE_QUERY)

INSERT_QUERY = 'INSERT INTO tweets (username, text) VALUES (%s, %s)'

# get ENV Variable that contains the user input (which tweets to search)


def authenticate():
    """Function for handling Twitter Authentication.
    """
    auth = OAuthHandler(config.CONSUMER_API_KEY, config.CONSUMER_API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) #t is just a regular python dictionary.
        #print(t)
        tweet = {
        'text': t['text'],
        'username': t['user']['screen_name']
        }

        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')
        engine.execute(INSERT_QUERY, (tweet['username'], tweet['text'],))


    def on_error(self, status):

        if status == 420:
            print(status)
            return False


key = 'TRACK'
track = os.getenv(key)
print(track)


if __name__ == '__main__':
    
    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    stream.filter(track=[track], languages=['en'])
