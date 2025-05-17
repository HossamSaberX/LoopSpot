import os
import json
import sys
from datetime import datetime
from .utils import get_application_path

class LoopStorage:
    """Handle storage of loop points."""
    
    def __init__(self, storage_dir="data"):
        """Initialize storage."""
        self.storage_dir = get_application_path()
        self.storage_path = os.path.join(self.storage_dir, storage_dir, "loop_points.json")
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.loops = self._load_loops()
    
    def _load_loops(self):
        """Load loops from storage file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading loops: {e}")
                return {}
        return {}
    
    def _save_loops(self):
        """Save loops to storage file."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.loops, f, indent=2)
        except Exception as e:
            print(f"Error saving loops: {e}")
    
    def save_loop(self, track_id, track_name, artist, point_a, point_b, name=None):
        """Save a loop for a track."""
        if track_id not in self.loops:
            self.loops[track_id] = []
        
        # Create a new loop entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        loop_name = name or f"Loop {len(self.loops[track_id]) + 1}"
        
        loop = {
            "name": loop_name,
            "track_name": track_name,
            "artist": artist,
            "point_a": point_a,
            "point_b": point_b,
            "created": timestamp,
            "last_used": timestamp
        }
        
        # Add the loop to the list
        self.loops[track_id].append(loop)
        self._save_loops()
        return loop
    
    def get_loops_for_track(self, track_id):
        """Get all loops for a track."""
        return self.loops.get(track_id, [])
    
    def get_loop(self, track_id, loop_index):
        """Get a specific loop by index."""
        loops = self.get_loops_for_track(track_id)
        if 0 <= loop_index < len(loops):
            return loops[loop_index]
        return None
    
    def update_loop(self, track_id, loop_index, point_a=None, point_b=None, name=None):
        """Update an existing loop."""
        loop = self.get_loop(track_id, loop_index)
        if loop:
            if point_a is not None:
                loop["point_a"] = point_a
            if point_b is not None:
                loop["point_b"] = point_b
            if name:
                loop["name"] = name
            
            loop["last_used"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._save_loops()
            return True
        return False
    
    def delete_loop(self, track_id, loop_index):
        """Delete a loop."""
        loops = self.get_loops_for_track(track_id)
        if 0 <= loop_index < len(loops):
            loops.pop(loop_index)
            self._save_loops()
            return True
        return False
    
    def get_all_loops(self):
        """Get all loops, grouped by track."""
        result = []
        for track_id, loops in self.loops.items():
            if loops:  # Only add tracks that have loops
                track_name = loops[0]["track_name"]
                artist = loops[0]["artist"]
                result.append({
                    "track_id": track_id,
                    "track_name": track_name,
                    "artist": artist,
                    "loops": loops
                })
        return result 