from flask import Flask, render_template, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# Spotify API credentials (You can also set these as environment variables)
SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'
SPOTIPY_REDIRECT_URI = 'your_redirect_uri'
scope = 'playlist-modify-private playlist-modify-public playlist-read-private'

# Authenticate with Spotify using OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove_duplicates', methods=['POST'])
def remove_duplicates():
    # Get form data
    client_id = request.form['clientId']
    client_secret = request.form['clientSecret']
    redirect_uri = request.form['redirectUri']
    playlist_id = request.form['playlistId']

    # Authenticate with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))

    # Find duplicate tracks (implement your logic here)
    duplicates = find_duplicate_tracks(playlist_id)

    # Remove duplicates (implement your logic here)
    for track in duplicates:
        sp.playlist_remove_all_occurrences_of_items(playlist_id, [track['uri']])

    return jsonify({'message': 'Duplicates removed successfully!'})

def find_duplicate_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    unique_tracks = {}
    duplicates = []

    for track in tracks:
        track_name = track['track']['name']
        track_artist = track['track']['artists'][0]['name']
        track_uri = track['track']['uri']

        track_key = (track_name.lower(), track_artist.lower())

        if track_key in unique_tracks:
            duplicates.append({
                'name': track_name,
                'artist': track_artist,
                'uri': track_uri
            })
        else:
            unique_tracks[track_key] = track_uri

    return duplicates

if __name__ == '__main__':
    app.run(debug=True)
