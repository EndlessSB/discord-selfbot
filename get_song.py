import requests
import re

def get_current_song(spotify_token):
    """Gets the current song from Spotify using the overlay API"""
    try:
        # Get the song data from the overlay API using the token
        response = requests.get(
            f"https://spotify-overlay.raphaelmarco.com/now_playing?accessToken={spotify_token}"
        )
        
        if response.status_code != 200:
            return "Failed to get current song"
            
        # Parse the HTML response
        html_text = response.text
        
        # Extract song name and artist from HTML
        # Look for text between title tags
        title_match = re.search(r'<title>(.*?)</title>', html_text)
        if title_match:
            title_text = title_match.group(1)
            # Title format is usually "Song Name - Artist"
            parts = title_text.split(' - ')
            if len(parts) == 2:
                song_name = parts[0].strip()
                artist = parts[1].strip()
                return f"{song_name} by {artist}"
        
        return "Could not parse song info"
        
    except Exception as e:
        return f"Error getting current song: {str(e)}"
