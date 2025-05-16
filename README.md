# LoopSpot - Spotify AB Looper (CLI Version)

A proof-of-concept command-line application that allows setting A/B loop points for Spotify tracks.

## Features

- Set loop points A and B at current playback positions
- Manually enter custom timestamps for precise loop points
- Automatically loop between points A and B during playback
- Save and load loop points for your favorite tracks
- Simple command-line interface
- User-provided Spotify API credentials

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

3. Run the application:
   ```
   python run.py
   ```

4. First-time setup:
   - You'll be guided through the process of setting up your Spotify Developer credentials
   - Follow the on-screen instructions to create a Spotify application
   - Enter your Client ID and Client Secret when prompted

## Setting up Spotify Developer Credentials

When you first run LoopSpot, you'll need to set up your own Spotify Developer credentials:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in
2. Click "Create app"
3. Fill in the required fields:
   - App name: "LoopSpot" (or any name you prefer)
   - App description: "A/B loop controller for Spotify"
   - Redirect URI: `http://127.0.0.1:8888/`
   - Select appropriate API scopes
4. Accept the terms and conditions and create the app
5. Copy the Client ID and Client Secret from your app's dashboard
6. Enter these values when prompted by LoopSpot

## Usage

1. Run the application:
   ```
   python run.py
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
- **12**: Reset Spotify credentials
- **0**: Exit

## Data Storage

LoopSpot stores two types of data:
- **Spotify Credentials**: Stored in `data/spotify_credentials.json`
- **Access Tokens**: Stored in `data/spotify_token.json`
- **Loop Points**: Stored in `data/loop_points.json`

You can reset your credentials at any time using option 12 in the menu.

## Notes

- This is a proof-of-concept application
- Loop accuracy may vary depending on network conditions
- You must have an active Spotify playback session on any device
- The HTTP server uses port 8888 for the OAuth callback 