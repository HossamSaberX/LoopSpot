import os
import sys
import time
from .auth import SpotifyAuth
from .spotify_api import SpotifyPlayer
from .storage import LoopStorage
from .loop_logic import LoopController

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

class LoopSpotCLI:
    """Command-line interface for LoopSpot."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.auth = SpotifyAuth()
        self.sp = None
        self.player = None
        self.storage = LoopStorage()
        self.loop_controller = None
        self.running = True
    
    def initialize(self):
        """Initialize the Spotify client and other components."""
        print("Initializing LoopSpot CLI...")
        self.sp = self.auth.get_spotify_client()
        
        if not self.sp:
            print("Failed to authenticate with Spotify.")
            return False
        
        self.player = SpotifyPlayer(self.sp)
        self.loop_controller = LoopController(self.player)
        
        # Set UI refresh callback
        self.loop_controller.set_ui_refresh_callback(self.refresh_ui)
        
        return True
    
    def refresh_ui(self):
        """Refresh the UI after loop monitor actions."""
        # Clear the screen and redraw the UI
        clear_screen()
        self.print_header()
        self.print_current_track()
        self.print_menu()
        sys.stdout.flush()  # Ensure output is displayed
    
    def print_header(self):
        """Print the application header."""
        clear_screen()
        print("=" * 60)
        print("LoopSpot - Spotify AB Looper (CLI Version)")
        print("=" * 60)
    
    def print_current_track(self):
        """Print information about the current track."""
        print("\nCurrent Track:")
        print(self.player.get_pretty_playback_status())
        
        # Print loop points if set
        points = self.loop_controller.get_current_points()
        if points:
            print(f"Loop Points: A={points['point_a_formatted']} B={points['point_b_formatted']}")
            if self.loop_controller.active:
                print("Loop Status: ACTIVE")
            else:
                print("Loop Status: INACTIVE")
    
    def print_menu(self):
        """Print the main menu."""
        print("\nCommands:")
        print("  1. Set point A (current position)")
        print("  2. Set point B (current position)")
        print("  3. Set point A (manual timestamp)")
        print("  4. Set point B (manual timestamp)")
        print("  5. Start loop")
        print("  6. Stop loop")
        print("  7. Save current loop")
        print("  8. List saved loops")
        print("  9. Load a saved loop")
        print("  10. Delete a saved loop")
        print("  11. Refresh current track")
        print("  0. Exit")
        print("\nEnter command: ", end="")
    
    def list_saved_loops(self):
        """List all saved loops."""
        clear_screen()
        print("Saved Loops:")
        print("=" * 60)
        
        all_loops = self.storage.get_all_loops()
        
        if not all_loops:
            print("No saved loops found.")
            input("\nPress Enter to continue...")
            return
        
        # Check if current track has loops
        current_track = self.player.get_current_track()
        current_track_loops = None
        
        if current_track:
            for track in all_loops:
                if track['track_id'] == current_track['id']:
                    current_track_loops = track
                    break
        
        # Display loops for current track first
        if current_track_loops:
            print(f"\nCurrent Track: {current_track_loops['track_name']} - {current_track_loops['artist']}")
            for i, loop in enumerate(current_track_loops['loops']):
                print(f"  {i+1}. {loop['name']}: {self.player.format_time(loop['point_a'])} - {self.player.format_time(loop['point_b'])}")
        
        # Display other tracks
        print("\nOther Tracks:")
        other_tracks = [track for track in all_loops if not (current_track and track['track_id'] == current_track['id'])]
        
        for track in other_tracks:
            print(f"\n{track['track_name']} - {track['artist']}")
            for i, loop in enumerate(track['loops']):
                print(f"  {i+1}. {loop['name']}: {self.player.format_time(loop['point_a'])} - {self.player.format_time(loop['point_b'])}")
        
        input("\nPress Enter to continue...")
    
    def save_current_loop(self):
        """Save the current loop."""
        points = self.loop_controller.get_current_points()
        if not points:
            print("No loop points set to save.")
            time.sleep(1)
            return
        
        track = self.player.get_current_track()
        if not track:
            print("No track is currently playing.")
            time.sleep(1)
            return
        
        name = input("Enter a name for this loop (or press Enter for default): ")
        if not name:
            name = None  # Use default naming
        
        self.storage.save_loop(
            track_id=track['id'],
            track_name=track['name'],
            artist=track['artist'],
            point_a=points['point_a'],
            point_b=points['point_b'],
            name=name
        )
        
        print("Loop saved successfully.")
        time.sleep(1)
    
    def load_saved_loop(self):
        """Load a saved loop for the current track."""
        track = self.player.get_current_track()
        if not track:
            print("No track is currently playing.")
            time.sleep(1)
            return
        
        loops = self.storage.get_loops_for_track(track['id'])
        if not loops:
            print("No saved loops for the current track.")
            time.sleep(1)
            return
        
        clear_screen()
        print(f"Saved Loops for: {track['name']} - {track['artist']}")
        print("=" * 60)
        
        for i, loop in enumerate(loops):
            print(f"{i+1}. {loop['name']}: {self.player.format_time(loop['point_a'])} - {self.player.format_time(loop['point_b'])}")
        
        try:
            choice = int(input("\nEnter loop number to load (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(loops):
                loop_data = {
                    'track_id': track['id'],
                    'point_a': loops[choice-1]['point_a'],
                    'point_b': loops[choice-1]['point_b']
                }
                self.loop_controller.load_loop(loop_data)
            else:
                print("Invalid selection.")
                time.sleep(1)
        except ValueError:
            print("Invalid input.")
            time.sleep(1)
    
    def delete_saved_loop(self):
        """Delete a saved loop."""
        track = self.player.get_current_track()
        if not track:
            print("No track is currently playing.")
            time.sleep(1)
            return
        
        loops = self.storage.get_loops_for_track(track['id'])
        if not loops:
            print("No saved loops for the current track.")
            time.sleep(1)
            return
        
        clear_screen()
        print(f"Saved Loops for: {track['name']} - {track['artist']}")
        print("=" * 60)
        
        for i, loop in enumerate(loops):
            print(f"{i+1}. {loop['name']}: {self.player.format_time(loop['point_a'])} - {self.player.format_time(loop['point_b'])}")
        
        try:
            choice = int(input("\nEnter loop number to delete (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(loops):
                if self.storage.delete_loop(track['id'], choice-1):
                    print("Loop deleted.")
                else:
                    print("Failed to delete loop.")
            else:
                print("Invalid selection.")
            
            time.sleep(1)
        except ValueError:
            print("Invalid input.")
            time.sleep(1)
    
    def set_point_a(self):
        """Set point A at current position with confirmation if already set."""
        # Check if points are already set
        if self.loop_controller.point_a is not None:
            current_a = self.player.format_time(self.loop_controller.point_a)
            print(f"Point A is currently set at {current_a}")
            confirm = input("Do you want to change it? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Operation cancelled.")
                time.sleep(1)
                return
        
        # Set point A
        self.loop_controller.set_point_a()
    
    def set_point_b(self):
        """Set point B at current position with confirmation if already set."""
        # Check if point B is already set
        if self.loop_controller.point_b is not None:
            current_b = self.player.format_time(self.loop_controller.point_b)
            print(f"Point B is currently set at {current_b}")
            confirm = input("Do you want to change it? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Operation cancelled.")
                time.sleep(1)
                return
        
        # Set point B
        self.loop_controller.set_point_b()
    
    def set_point_a_manual(self):
        """Set point A with a manually entered timestamp."""
        track = self.player.get_current_track()
        if not track:
            print("No track is currently playing.")
            time.sleep(1)
            return
        
        # Check if point A is already set
        if self.loop_controller.point_a is not None:
            current_a = self.player.format_time(self.loop_controller.point_a)
            print(f"Point A is currently set at {current_a}")
            confirm = input("Do you want to change it? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Operation cancelled.")
                time.sleep(1)
                return
        
        print(f"\nCurrent track: {track['name']} - {track['artist']}")
        print(f"Track duration: {self.player.format_time(track['duration_ms'])}")
        
        timestamp = input("\nEnter point A timestamp (mm:ss format): ")
        self.loop_controller.set_point_a_timestamp(timestamp)
        time.sleep(1)
    
    def set_point_b_manual(self):
        """Set point B with a manually entered timestamp."""
        track = self.player.get_current_track()
        if not track:
            print("No track is currently playing.")
            time.sleep(1)
            return
        
        if self.loop_controller.point_a is None:
            print("Please set point A first.")
            time.sleep(1)
            return
        
        # Check if point B is already set
        if self.loop_controller.point_b is not None:
            current_b = self.player.format_time(self.loop_controller.point_b)
            print(f"Point B is currently set at {current_b}")
            confirm = input("Do you want to change it? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Operation cancelled.")
                time.sleep(1)
                return
        
        print(f"\nCurrent track: {track['name']} - {track['artist']}")
        print(f"Track duration: {self.player.format_time(track['duration_ms'])}")
        print(f"Point A: {self.player.format_time(self.loop_controller.point_a)}")
        
        timestamp = input("\nEnter point B timestamp (mm:ss format): ")
        self.loop_controller.set_point_b_timestamp(timestamp)
        time.sleep(1)
    
    def process_command(self, command):
        """Process a user command."""
        if command == '1':  # Set point A (current)
            self.set_point_a()
        elif command == '2':  # Set point B (current)
            self.set_point_b()
        elif command == '3':  # Set point A (manual)
            self.set_point_a_manual()
        elif command == '4':  # Set point B (manual)
            self.set_point_b_manual()
        elif command == '5':  # Start loop
            self.loop_controller.start_loop()
        elif command == '6':  # Stop loop
            self.loop_controller.stop_loop()
        elif command == '7':  # Save current loop
            self.save_current_loop()
        elif command == '8':  # List saved loops
            self.list_saved_loops()
        elif command == '9':  # Load a saved loop
            self.load_saved_loop()
        elif command == '10':  # Delete a saved loop
            self.delete_saved_loop()
        elif command == '11':  # Refresh current track
            # Nothing to do, will refresh on next loop
            pass
        elif command == '0':  # Exit
            self.running = False
            if self.loop_controller and self.loop_controller.active:
                self.loop_controller.stop_loop()
            print("Exiting LoopSpot. Goodbye!")
        else:
            print("Invalid command.")
            time.sleep(1)
    
    def run(self):
        """Run the main CLI loop."""
        if not self.initialize():
            return False
        
        while self.running:
            self.print_header()
            self.print_current_track()
            self.print_menu()
            
            command = input()
            self.process_command(command)
        
        return True 