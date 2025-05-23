import time

class SpotifyPlayer:
    """Wrapper for Spotify API player functions."""
    
    def __init__(self, spotify_client):
        """Initialize with a Spotify client."""
        self.sp = spotify_client
        
    def get_current_playback(self):
        """Get the current playback state."""
        try:
            return self.sp.current_playback()
        except Exception as e:
            print(f"Error getting playback: {e}")
            return None
    
    def get_current_track(self):
        """Get information about the currently playing track."""
        try:
            playback = self.get_current_playback()
            if playback and playback['item']:
                track = playback['item']
                return {
                    'id': track['id'],
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'duration_ms': track['duration_ms'],
                    'is_playing': playback['is_playing'],
                    'progress_ms': playback['progress_ms']
                }
        except Exception as e:
            print(f"Error getting track: {e}")
        return None
    
    def get_playback_position(self):
        """Get the current playback position in milliseconds."""
        try:
            playback = self.get_current_playback()
            if playback:
                return playback['progress_ms']
        except Exception as e:
            print(f"Error getting position: {e}")
        return None
    
    def seek_to_position(self, position_ms):
        """Seek to a specific position in the current track."""
        try:
            self.sp.seek_track(position_ms)
            return True
        except Exception as e:
            print(f"Error seeking: {e}")
            return False
    
    def format_time(self, milliseconds):
        """Format milliseconds as mm:ss."""
        if milliseconds is None:
            return "00:00"
        
        seconds = milliseconds // 1000
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_pretty_playback_status(self):
        """Get a formatted string with current playback information."""
        track = self.get_current_track()
        
        if not track:
            return "No track is currently playing."
        
        progress = self.format_time(track['progress_ms'])
        duration = self.format_time(track['duration_ms'])
        status = " ▶️  Playing" if track['is_playing'] else " ⏸️  Paused"
        
        return f"{status}: {track['name']} - {track['artist']} [{progress}/{duration}]"
    
    def play_track(self, track_uri):
        """Play a specific track."""
        try:
            self.sp.start_playback(uris=[f"spotify:track:{track_uri}"])
            # Wait a short time for playback to start
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"Error playing track: {e}")
            return False
    
    def resume_playback(self):
        """Resume playback if it's paused."""
        try:
            playback = self.get_current_playback()
            if playback and not playback['is_playing']:
                self.sp.start_playback()
                return True
            return False  # Already playing
        except Exception as e:
            print(f"Error resuming: {e}")
            return False
            
    def seek_to_position_and_play(self, position_ms):
        """Seek to a specific position and ensure playback is active."""
        try:
            # First seek to the position
            success = self.seek_to_position(position_ms)
            if not success:
                return False
                
            # Then make sure playback is active
            self.resume_playback()
            return True
        except Exception as e:
            print(f"Error seeking and playing: {e}")
            return False 