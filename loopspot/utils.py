import os
import sys

def get_application_path():
    """Get the correct application base path whether running from source or frozen executable."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running as a PyInstaller bundle (frozen)
        base_dir = os.path.dirname(sys.executable)
        # Create the data directory if it doesn't exist
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        return base_dir
    else:
        # Running as a normal Python script
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 