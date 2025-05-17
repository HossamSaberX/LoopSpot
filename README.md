# LoopSpot - Spotify AB Looper (CLI Version)

A command-line application that allows setting A/B loop points for Spotify tracks, enabling seamless practice or focused listening of specific parts of songs.

## Features

- Set loop points A and B at current playback positions
- Manually enter custom timestamps for precise loop points
- Automatically loop between points A and B during playback
- Save and load loop points for your favorite tracks
- Simple command-line interface
- Quick setup with Spotify API credentials

## Requirements

- Python 3.6 or higher
- **Spotify Premium account** (required for the API to seek to specific timestamps)
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
   - App description: Enter anything (this is just for your reference)
   - Redirect URI: `http://127.0.0.1:8888/`
   - **Important**: Select the "Web API" option (make sure this box is checked)
   ![Web API Selection](https://developer.spotify.com/assets/WebAPI.png)
4. Check "I understand and agree with Spotify's Developer Terms" and click "Save"
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

- Loop accuracy may vary depending on network conditions
- You must have an active Spotify playback session on any device
- The HTTP server uses port 8888 for the OAuth callback 
- **Spotify Premium is required** for the seeking functionality to work properly

## Releases & Executable Builds

LoopSpot uses GitHub Actions to automatically build executables for Windows and Linux. These executables are attached to GitHub releases when a new version tag is pushed.

### Downloading Executables

1. Go to the [Releases](https://github.com/yourusername/loopspot/releases) page
2. Download the appropriate executable for your platform:
   - `loopspot.exe` for Windows
   - `loopspot` for Linux

### Running the Executable

#### Windows
- Simply double-click the `loopspot.exe` file to run the application

#### Linux
- After downloading, make the file executable:
  ```
  chmod +x loopspot
  ```
- Then run it from the terminal:
  ```
  ./loopspot
  ```

### Triggering New Builds

For repository maintainers:

1. Make your changes and commit them
2. Tag the commit with a version number:
   ```
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. The GitHub Action will automatically:
   - Build executables for Windows and Linux
   - Create a new release with these executables
   - Generate release notes from commit messages

You can also manually trigger builds from the GitHub Actions tab by using the "workflow_dispatch" trigger. 