# LoopSpot - Spotify AB Looper (CLI Version)

A proof-of-concept command-line application that allows setting A/B loop points for Spotify tracks.

## Features

- Set loop points A and B at current playback positions
- Manually enter custom timestamps for precise loop points
- Automatically loop between points A and B during playback
- Save and load loop points for your favorite tracks
- Simple command-line interface

## Requirements

- Python 3.6 or higher
- Spotify Premium account
- Active Spotify playback on any device
- Spotify application registered with the Spotify Developer Dashboard

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/loopspot.git
   cd loopspot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Spotify Client Secret:
   ```
   export SPOTIPY_CLIENT_SECRET='your_client_secret_from_spotify_dashboard'
   ```
   
   You can get your client secret from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard):
   - Go to your LoopSpot application
   - Copy the "Client Secret" value
   - For Windows, use `set SPOTIPY_CLIENT_SECRET=your_secret` instead
   
4. Configure your Spotify app:
   - Go to your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Select your LoopSpot application
   - Click "Edit Settings"
   - Add `http://127.0.0.1:8888/` to the Redirect URIs section
   - Save changes

## Usage

1. Run the application:
   ```
   python run_loopspot.py
   ```

2. Authenticate with your Spotify account when prompted.

3. Use the command-line interface to set loop points and control playback:
   - Set point A at the current playback position
   - Set point B at the current playback position
   - Start/stop the loop
   - Save loops for future use
   - Load previously saved loops

## How It Works

LoopSpot monitors your Spotify playback position in real-time. When the playback position reaches your defined point B, it automatically seeks back to point A, creating a seamless loop.

## Commands

- **1**: Set point A (current position)
- **2**: Set point B (current position)
- **3**: Set point A (manual timestamp)
- **4**: Set point B (manual timestamp)
- **5**: Start loop
- **6**: Stop loop
- **7**: Save current loop
- **8**: List saved loops
- **9**: Load a saved loop
- **10**: Delete a saved loop
- **11**: Refresh current track
- **0**: Exit

## Notes

- This is a proof-of-concept application
- Loop accuracy may vary depending on network conditions
- You must have an active Spotify playback session on any device
- The HTTP server uses port 8888 for the OAuth callback 