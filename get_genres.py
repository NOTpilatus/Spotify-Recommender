import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

c = 'GETSONG_CLIENT'
d = 'GETSONG_SECRET'
cl = os.getenv(c)
sec = os.getenv(d)
print(cl,d)
# set open_browser=False to prevent Spotipy from attempting to open the default browser
client_credentials_manager = SpotifyClientCredentials(client_id=cl, client_secret=sec)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

r = sp.recommendation_genre_seeds()
result = sorted(list(r['genres']))

#print(r)