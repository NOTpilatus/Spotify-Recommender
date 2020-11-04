import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import os
import time
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pprint import pprint
import pandas as pd
import spotipy.util as util
from json.decoder import JSONDecodeError
import json
import webbrowser
import get_genres

############################# VARIABLES #######################################################


# spotify credentials
client = cred.SPOTIPY_CLIENT_ID
secret = cred.SPOTIPY_CLIENT_SECRET
redirect = cred.SPOTIPY_REDIRECT_URI

scope = "user-read-private user-read-playback-state,user-modify-playback-state"
username = "pontze84"
# username = input('Please enter your Spotify - Username:')
os.system("clear")

# getting token
try:
    token = util.prompt_for_user_token(
        username, scope, client_id=client, client_secret=secret, redirect_uri=redirect
    )
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(
        username, scope, client_id=client, client_secret=secret, redirect_uri=redirect
    )

# instantiating spotipy object

spp = spotipy.Spotify(auth=token)

time.sleep(3)
user = spp.current_user()
displayName = user["display_name"]
follower = user["followers"]["total"]
all_genres = get_genres.result


# Vader Sentiment Analysis
s = SentimentIntensityAnalyzer()

#################################################### FUNCTIONS ##############################################################

def extract():
    """Extracts tweets from Postgres, returns them as a dataframe"""
    result = engine.execute(EXTRACT_QUERY)
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()

    return df


def transform(tweets):
    """perform sentiment analysis on extracted tweets - returns sentiment score (float)"""

    x = s.polarity_scores(tweets["text"])["compound"]

    # normalize to range 0 - 1
    sense = (x + 1) / 2

    return sense


def get_song(sentiment_score, genre):

    """ returns a (random) song from spotify with a valence according to sentiment_score """
    # Spotipy authentification for getting songs
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cred.getsong_client, client_secret=cred.getsong_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    if sentiment_score >= 0.9:
        min_v = 0.9
        max_v = 1
    else:
        min_v = sentiment_score
        max_v = sentiment_score + 0.2

    r = sp.recommendations(
        seed_genres=[genre], min_valence=min_v, max_valence=max_v, limit=1
    )

    title = r["tracks"][0]["name"]
    uri = r["tracks"][0]["uri"]
    artist = r["tracks"][0]["artists"][0]["name"]
    image = r["tracks"][0]["album"]["images"][0]["url"]
    # print(uris)
    return uri, title, artist, image


############################## USER INPUT: ##############################################################################


while True:

    print()
    print(">>> Welcome to Spotify, " + displayName + " :)")
    print(">>> You have " + str(follower) + " followers.")
    time.sleep(3)

    while res['devices'][0]['is_active'] == False :
        print('Please make sure your device is active.')
        time.sleep(3)
        os.system('clear')
        #spp = spotipy.Spotify(auth=token)
        res = spp.devices()
    time.sleep(2)
    print('Thank you.')
    time.sleep(3)
    os.system("clear")
    time.sleep(3)
    os.system("clear")
    print("The following genres are available:")
    time.sleep(2)
    print()
    pprint(all_genres, compact=True)
    print()
    genre_1 = input("please choose a genre from the list above: ")
    if genre_1 in all_genres:
        genre_2 = input("another one, please: ")
        if genre_2 in all_genres:
            genre_3 = input("and one last: ")
            if genre_3 in all_genres:
                break


os.system("clear")
time.sleep(1)
print()
print("Let's collect some tweets.")
time.sleep(1)
track = input("What would you like to search about?")
print()
print("Alright.")
os.system(f"echo TRACK={track} > ~/Spiced/spearmint-vector-student-code/FINAL/.env")
time.sleep(2)
os.system("clear")


os.system(
    "docker-compose -f /home/spiced/Spiced/spearmint-vector-student-code/FINAL/docker-compose.yml up -d"
)
print()
print()
print("Started tweet collection.")
time.sleep(2)
os.system("clear")
print("Please wait.")
print("...")
time.sleep(2)
print("...")
time.sleep(2)
print("...")
os.system("clear")
time.sleep(2)
print("Please wait.")
time.sleep(2)
print("...")
time.sleep(2)
print("...")
time.sleep(2)
os.system("clear")
print("Please wait.")
print("...")
time.sleep(2)
print("...")
time.sleep(2)
print("...")
time.sleep(2)
os.system("clear")
print("Please wait. :D")
time.sleep(2)
print("...")
time.sleep(2)
print("...")
time.sleep(2)
print("...")
os.system("clear")
time.sleep(2)

extracted_tweets = extract()
print("Using the following tweets:")
print()
time.sleep(2)
print()
pprint(extracted_tweets['text'], compact=True)
sentiment = transform(extracted_tweets)
time.sleep(2)
print()
print("Current overall sentiment:")
print()
print(sentiment)
print()
uri_1, title_1, artist_1, image_1 = get_song(sentiment, genre_1)
time.sleep(2)
print(f"You should listen to this: {title_1} by {artist_1}")
time.sleep(1)
spp.start_playback(uris=[uri_1])
webbrowser.open(image_1)
uri_2, title_2, artist_2, image_2 = get_song(sentiment, genre_2)
time.sleep(10)
print()
print(f"Or maybe this one: {title_2} by {artist_2}")
time.sleep(1)
spp.start_playback(uris=[uri_2])
webbrowser.open(image_2)
uri_3, title_3, artist_3, image_3 = get_song(sentiment, genre_3)
time.sleep(10)
print()
print(f"Or maybe this one?: {title_3} by {artist_3}")
time.sleep(1)
spp.start_playback(uris=[uri_3])
webbrowser.open(image_3)
print()
print("Enjoy.")
print()
print("Bye!")
time.sleep(3)
os.system(
    "docker-compose -f /home/spiced/Spiced/spearmint-vector-student-code/FINAL/docker-compose.yml down"
)
