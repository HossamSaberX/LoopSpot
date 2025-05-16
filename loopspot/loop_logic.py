import threading
import time

class LoopController:
    """Control the AB looping logic."""
    
    def __init__(self, spotify_player):
        """Initialize with a Spotify player."""
        self.player = spotify_player
        self.point_a = None
        self.point_b = None
        self.current_track_id = None
        self.active = False
        self.loop_thread = None
        self.stop_event = threading.Event()
        self.ui_refresh_callback = None  # Callback for UI refresh
    
    def set_ui_refresh_callback(self, callback):
        """Set callback function to refresh UI after seeking."""
        self.ui_refresh_callback = callback
    
    def set_point_a(self):
        """Set point A to the current playback position."""
        track = self.player.get_current_track()
        if not track:
            print("No track is currently playing.")
            return False
        
        position = track['progress_ms']
        self.point_a = position
        self.current_track_id = track['id']
        
        formatted_time = self.player.format_time(position)
        print(f"Point A set at {formatted_time}")
        return True
    
    def set_point_a_timestamp(self, timestamp):
        """Set point A to a specific timestamp (mm:ss format)."""
        track = self.player.get_current_track()
        if not track:
            print("No track is currently playing.")
            return False
        
        try:
            # Parse mm:ss format into milliseconds
            parts = timestamp.strip().split(':')
            if len(parts) != 2:
                print("Invalid timestamp format. Please use mm:ss format.")
                return False
            
            minutes = int(parts[0])
            seconds = int(parts[1])
            position_ms = (minutes * 60 + seconds) * 1000
            
            # Validate the timestamp
            if position_ms < 0 or position_ms > track['duration_ms']:
                print(f"Timestamp out of range. Track duration is {self.player.format_time(track['duration_ms'])}.")
                return False
            
            self.point_a = position_ms
            self.current_track_id = track['id']
            
            formatted_time = self.player.format_time(position_ms)
            print(f"Point A set at {formatted_time}")
            return True
            
        except ValueError:
            print("Invalid timestamp format. Please use mm:ss format.")
            return False
    
    def set_point_b(self):
        """Set point B to the current playback position."""
        track = self.player.get_current_track()
        if not track:
            print("No track is currently playing.")
            return False
        
        if not self.point_a:
            print("Please set point A first.")
            return False
        
        if track['id'] != self.current_track_id:
            print("Track has changed. Please set point A again.")
            self.point_a = None
            return False
        
        position = track['progress_ms']
        
        # Ensure point B is after point A
        if position <= self.point_a:
            print("Point B must be after point A.")
            return False
        
        self.point_b = position
        formatted_time = self.player.format_time(position)
        print(f"Point B set at {formatted_time}")
        return True
    
    def set_point_b_timestamp(self, timestamp):
        """Set point B to a specific timestamp (mm:ss format)."""
        track = self.player.get_current_track()
        if not track:
            print("No track is currently playing.")
            return False
        
        if not self.point_a:
            print("Please set point A first.")
            return False
        
        if track['id'] != self.current_track_id:
            print("Track has changed. Please set point A again.")
            self.point_a = None
            return False
        
        try:
            # Parse mm:ss format into milliseconds
            parts = timestamp.strip().split(':')
            if len(parts) != 2:
                print("Invalid timestamp format. Please use mm:ss format.")
                return False
            
            minutes = int(parts[0])
            seconds = int(parts[1])
            position_ms = (minutes * 60 + seconds) * 1000
            
            # Validate the timestamp
            if position_ms < 0 or position_ms > track['duration_ms']:
                print(f"Timestamp out of range. Track duration is {self.player.format_time(track['duration_ms'])}.")
                return False
            
            # Ensure point B is after point A
            if position_ms <= self.point_a:
                print("Point B must be after point A.")
                return False
            
            self.point_b = position_ms
            formatted_time = self.player.format_time(position_ms)
            print(f"Point B set at {formatted_time}")
            return True
            
        except ValueError:
            print("Invalid timestamp format. Please use mm:ss format.")
            return False
    
    def clear_points(self):
        """Clear the current loop points."""
        self.point_a = None
        self.point_b = None
        self.current_track_id = None
        print("Loop points cleared.")
    
    def get_current_points(self):
        """Get the current loop points."""
        if self.point_a is not None and self.point_b is not None:
            return {
                'track_id': self.current_track_id,
                'point_a': self.point_a,
                'point_b': self.point_b,
                'point_a_formatted': self.player.format_time(self.point_a),
                'point_b_formatted': self.player.format_time(self.point_b)
            }
        return None
    
    def start_loop(self):
        """Start the looping process."""
        if not self.point_a or not self.point_b:
            print("Both points A and B must be set before starting the loop.")
            return False
        
        track = self.player.get_current_track()
        if not track or track['id'] != self.current_track_id:
            print("Track has changed. Please set points again.")
            self.clear_points()
            return False
        
        if self.active:
            print("Loop is already active.")
            return True
        
        # If track is paused, start at point A and resume playback
        if not track['is_playing']:
            print(f"Track is paused. Seeking to point A and resuming playback.")
            self.player.seek_to_position_and_play(self.point_a)
        # If track is already playing but outside loop range, seek to point A
        elif track['progress_ms'] < self.point_a or track['progress_ms'] >= self.point_b:
            print(f"Playback outside loop range. Seeking to point A.")
            self.player.seek_to_position(self.point_a)
        
        # Start the loop thread
        self.active = True
        self.stop_event.clear()
        self.loop_thread = threading.Thread(target=self._loop_monitor)
        self.loop_thread.daemon = True
        self.loop_thread.start()
        
        print(f"Loop started: {self.player.format_time(self.point_a)} - {self.player.format_time(self.point_b)}")
        return True
    
    def stop_loop(self):
        """Stop the looping process."""
        if not self.active:
            print("No active loop to stop.")
            return False
        
        self.active = False
        self.stop_event.set()
        
        if self.loop_thread and self.loop_thread.is_alive():
            self.loop_thread.join(timeout=1.0)
        
        print("Loop stopped.")
        return True
    
    def load_loop(self, loop_data):
        """Load loop points from saved data."""
        if not loop_data:
            return False
        
        track = self.player.get_current_track()
        if not track or track['id'] != loop_data.get('track_id'):
            print("This loop is for a different track.")
            return False
        
        self.point_a = loop_data.get('point_a')
        self.point_b = loop_data.get('point_b')
        self.current_track_id = loop_data.get('track_id')
        
        print(f"Loop loaded: {self.player.format_time(self.point_a)} - {self.player.format_time(self.point_b)}")
        return True
    
    def _loop_monitor(self):
        """Background thread that monitors playback position and performs looping."""
        print("Loop monitor started.")
        
        while not self.stop_event.is_set():
            try:
                # Check if track is still the same
                track = self.player.get_current_track()
                if not track or track['id'] != self.current_track_id:
                    print("Track changed. Stopping loop.")
                    self.active = False
                    break
                
                # Check if track is paused
                if not track['is_playing']:
                    # Don't do anything while paused, just keep checking
                    time.sleep(0.5)
                    continue
                
                # Check playback position
                position = track['progress_ms']
                
                # STRICT LOOPING: Check if current position is outside our loop range
                if position < self.point_a or position >= self.point_b:
                    # If it's before point A or after/at point B, jump back to point A
                    print(f"Playback outside loop range. Returning to {self.player.format_time(self.point_a)}")
                    self.player.seek_to_position_and_play(self.point_a)
                    
                    # Give the seek a moment to take effect
                    time.sleep(0.5)
                    
                    # Call UI refresh callback if set
                    if self.ui_refresh_callback:
                        self.ui_refresh_callback()
                
                # Sleep for a short time to avoid excessive API calls
                time.sleep(0.3)
                
            except Exception as e:
                print(f"Error in loop monitor: {e}")
                time.sleep(1)  # Wait a bit longer if there's an error
        
        print("Loop monitor stopped.") 