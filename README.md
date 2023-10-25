# macos-spotify-lyrics

Short script to get the currently playing song from Spotify, scrape its lyrics from SGAPI and print the lyrics on your macOS terminal.

Note that the script only works on macOS because Applescript is used to communicate with Spotify.

Put your SGAPI key in the field `SG_KEY` in the `.env` file. [See here](https://api.shangui.cc/) for details on getting an API key.

## Usage
1. pip install git+https://github.com/aiyogg/macos-spotify-lyrics.git
2. export SG_KEY=your_sgapi_key
