import os
import json
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CREDENTIALS_PATH = os.path.join(DATA_DIR, "spotify_credentials.json")
TOKEN_PATH = os.path.join(DATA_DIR, "spotify_token.json")

# Default redirect URI and scope
DEFAULT_REDIRECT_URI = "http://127.0.0.1:8888/"
DEFAULT_SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

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
    
    def __init__(self, cache_dir="data"):
        """Initialize the auth manager."""
        os.makedirs(DATA_DIR, exist_ok=True)
        self.credentials_path = CREDENTIALS_PATH
        self.token_path = TOKEN_PATH
        
        # Get or create credentials
        self.credentials = self._get_or_create_credentials()
        
        self.sp_oauth = SpotifyOAuth(
            client_id=self.credentials["client_id"],
            client_secret=self.credentials["client_secret"],
            redirect_uri=self.credentials["redirect_uri"],
            scope=self.credentials["scope"],
            cache_path=self.token_path
        )
        
    def _get_or_create_credentials(self):
        """Get credentials from file or prompt user to enter them."""
        credentials = self._load_credentials()
        
        # If credentials are empty or incomplete, prompt user to enter them
        if not credentials or not credentials.get("client_id") or not credentials.get("client_secret"):
            print("\n=== Spotify API Credentials Setup ===")
            print("You need to create a Spotify Developer application to use LoopSpot.")
            print("Follow these steps:")
            print("1. Go to https://developer.spotify.com/dashboard")
            print("2. Log in with your Spotify account")
            print("3. Click 'Create app'")
            print("4. Fill in the app details:")
            print("   - Name: 'LoopSpot' (or any name you prefer)")
            print("   - Description: Enter anything (this is just for your reference)")
            print("   - Redirect URI: http://127.0.0.1:8888/")
            print("   - IMPORTANT: Select the 'Web API' option (make sure this box is checked)")
            print("5. Check 'I understand and agree with Spotify's Developer Terms' and click 'Save'")
            print("6. Copy the Client ID and Client Secret from the app dashboard")
            
            # Get credentials from user
            client_id = input("\nEnter your Spotify Client ID: ").strip()
            client_secret = input("Enter your Spotify Client Secret: ").strip()
            
            # Create/update credentials file
            credentials = {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": DEFAULT_REDIRECT_URI,
                "scope": DEFAULT_SCOPE
            }
            
            # Save credentials
            self._save_credentials(credentials)
            print("Credentials saved successfully!")
            
        return credentials
    
    def _load_credentials(self):
        """Load credentials from file."""
        try:
            if os.path.exists(self.credentials_path):
                with open(self.credentials_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading credentials: {e}")
        
        return None
    
    def _save_credentials(self, credentials):
        """Save credentials to file."""
        try:
            with open(self.credentials_path, 'w') as f:
                json.dump(credentials, f, indent=4)
        except Exception as e:
            print(f"Error saving credentials: {e}")
    
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
    
    def reset_credentials(self):
        """Clear stored credentials and prompt for new ones."""
        if os.path.exists(self.credentials_path):
            os.remove(self.credentials_path)
        
        # Also remove token to force new authentication
        if os.path.exists(self.token_path):
            os.remove(self.token_path)
            
        print("Credentials and session reset. You will be prompted for new credentials next time.")
        
        # Reinitialize credentials
        self.credentials = self._get_or_create_credentials()
        
        # Recreate OAuth object with new credentials
        self.sp_oauth = SpotifyOAuth(
            client_id=self.credentials["client_id"],
            client_secret=self.credentials["client_secret"],
            redirect_uri=self.credentials["redirect_uri"],
            scope=self.credentials["scope"],
            cache_path=self.token_path
        ) 