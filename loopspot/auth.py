import os
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Constants
CLIENT_ID = "feab870bd2f048a6baf7ad087f97546b"
# You should replace this with your actual client secret from the Spotify Dashboard
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET", "")  # Get secret from environment variable
REDIRECT_URI = "http://127.0.0.1:8888/"
SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
TOKEN_PATH = "data/spotify_token.json"

class AuthCallbackHandler(BaseHTTPRequestHandler):
    """Handler for OAuth callback."""
    
    def do_GET(self):
        """Handle GET request with authorization code."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Extract the authorization code from the query parameters
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        if 'code' in params:
            self.server.auth_code = params['code'][0]
            response = "<html><body><h1>Authentication successful!</h1><p>You can close this window now.</p></body></html>"
        else:
            self.server.auth_code = None
            response = "<html><body><h1>Authentication failed!</h1><p>Please try again.</p></body></html>"
        
        self.wfile.write(response.encode())
        
    def log_message(self, format, *args):
        """Suppress server logs."""
        return

class SpotifyAuth:
    """Handle Spotify authentication."""
    
    def __init__(self, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, cache_dir="data"):
        """Initialize the auth manager."""
        os.makedirs(cache_dir, exist_ok=True)
        self.token_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), TOKEN_PATH)
        
        if not client_secret:
            print("ERROR: No client secret provided. Set the SPOTIPY_CLIENT_SECRET environment variable.")
            print("You can get your client secret from the Spotify Developer Dashboard.")
            print("Instructions:")
            print("1. Go to https://developer.spotify.com/dashboard")
            print("2. Open your LoopSpot application")
            print("3. Copy the 'Client Secret'")
            print("4. Run this command before starting LoopSpot:")
            print("   export SPOTIPY_CLIENT_SECRET='your_client_secret_here'")
        
        self.sp_oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=self.token_path
        )
        
    def get_spotify_client(self):
        """Get an authenticated Spotify client."""
        token_info = self._get_token_info()
        
        if not token_info:
            token_info = self._authenticate()
            
        if token_info:
            return spotipy.Spotify(auth=token_info['access_token'])
        return None
    
    def _get_token_info(self):
        """Get token info from cache."""
        try:
            if os.path.exists(self.token_path):
                with open(self.token_path, 'r') as f:
                    token_info = json.load(f)
                
                # Check if the token is expired and refresh if needed
                if self.sp_oauth.is_token_expired(token_info):
                    token_info = self.sp_oauth.refresh_access_token(token_info['refresh_token'])
                    with open(self.token_path, 'w') as f:
                        json.dump(token_info, f)
                return token_info
        except Exception as e:
            print(f"Error reading token: {e}")
        return None
    
    def _authenticate(self):
        """Perform the OAuth flow."""
        auth_url = self.sp_oauth.get_authorize_url()
        print("Please visit this URL to authorize the application:")
        print(auth_url)
        webbrowser.open(auth_url)
        
        # Start a simple HTTP server to receive the callback
        server = HTTPServer(('127.0.0.1', 8888), AuthCallbackHandler)
        server.auth_code = None
        server.timeout = 60
        
        # Wait for the callback
        print("Waiting for authentication...")
        server.handle_request()
        
        # Process the received authorization code
        if server.auth_code:
            token_info = self.sp_oauth.get_access_token(server.auth_code)
            with open(self.token_path, 'w') as f:
                json.dump(token_info, f)
            return token_info
        
        print("Authentication failed.")
        return None
    
    def logout(self):
        """Remove stored token."""
        if os.path.exists(self.token_path):
            os.remove(self.token_path)
            print("Logged out successfully.")
        else:
            print("No active session found.") 