# OpenSongShare 
OpenSongShare is an extensible and flexible system for recommending songs between public Spotify playlists. It takes in two playlists and ranks one according to the other. Slides for the project can be found [here](https://bit.ly/opensongshare-slides).

## Project
- **Source Code**: src. Contains classes for...
 - Interfacing with Spotify (SpotifyConnector, SpotifyUserExplorer)
 - Downloading audio previews from Spotify (DatabaseSpotifyAudio)
 - Defining lists of tracks (TrackList, TrackListSpotify)
 - Featurizing the songs/tracks (Featurizer, FeaturizerMusicnn, FeaturizerSpotify)
 - Building recommendation engines (Recommender)
- **Streamlit Web Interface**: streamlit_interface.py. For recommending songs between the playlists of two spotify users. 

## Environment Installation
To set up this repo on your local computer, you will want to use pip with 

```
pip install -r requirements.txt
```

and also download libav-tools
```
sudo apt-get install libav-tools
```

You will also want to get your own spotify user id, which you will use to connect to Spotify using the class SpotifyConnector. Your spotify ID can be found online at this webpage: [https://www.spotify.com/us/account/set-device-password/](https://www.spotify.com/us/account/set-device-password/). 

## Using the recommender
You can test the recommender out with streamlit_interface.py. If you follow its structure, you can also build your own customized recommendation engine for comparing songs between playlists!