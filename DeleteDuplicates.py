import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up credentials
SPOTIPY_CLIENT_ID = 'YOUR CLIENT ID'
SPOTIPY_CLIENT_SECRET = 'YOUR CLIENT SECRET'
SPOTIPY_REDIRECT_URI = 'REDIRECT URL'
playlist_id = 'SPOTIFY PLAYLIST LINK'

scope = 'playlist-modify-private playlist-modify-public playlist-read-private'

# Authenticate with Spotify using OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

# Function to find and display duplicate tracks from a playlist
def find_duplicate_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    unique_tracks = {}
    duplicates = []

    for idx, track in enumerate(tracks):
        track_name = track['track']['name']
        track_artist = track['track']['artists'][0]['name']
        track_uri = track['track']['uri']

        track_key = (track_name.lower(), track_artist.lower())
        
        if track_key in unique_tracks:
            # Mark as duplicate
            duplicates.append({
                'name': track_name,
                'artist': track_artist,
                'uri': track_uri,
                'index': idx
            })
        else:
            unique_tracks[track_key] = track_uri

    return duplicates

def remove_duplicate_tracks(playlist_id, duplicates):
    tracks_to_remove = [{
        'uri': track['uri'],
        'positions': [track['index']]
    } for track in duplicates]

    # Remove duplicate tracks
    sp.playlist_remove_specific_occurrences_of_items(playlist_id, tracks_to_remove)
    print(f"Removed {len(tracks_to_remove)} duplicate tracks.")

# display duplicates, and ask for confirmation
def manage_duplicates(playlist_id):
    duplicates = find_duplicate_tracks(playlist_id)

    if duplicates:
        print(f"Found {len(duplicates)} duplicate tracks:")
        for i, track in enumerate(duplicates):
            print(f"{i+1}. {track['name']} by {track['artist']}")
        
        # Ask user if they want to remove duplicates
        confirm = input("Do you want to remove these duplicates? (yes/no): ").strip().lower()
        if confirm == 'yes':
            remove_duplicate_tracks(playlist_id, duplicates)
        else:
            print("No tracks were removed.")
    else:
        print("No duplicate tracks found.")

# Call the function to manage duplicates
manage_duplicates(playlist_id)
