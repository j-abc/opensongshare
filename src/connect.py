import argparse
import librosa
import logging
import os
import pickle
import random
import spotipy
import sys
import time
import wget

# import .preprocess

import numpy as np
import os.path as path
import spotipy.util as su


def get_spotify_instance(client_id, client_secret):
    """Get a Spotify instance that can pull information from the Spotify API.

    Args:
        client_id (str): Client ID for accessing Spotify API.
        client_secret (str): Secret client ID (key) for accessing Spotify API.

    Returns:
        S: A Spotify instance that can be used to query the Spotify API.
    """
    token = su.oauth2.SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    cache_token = token.get_access_token()
    try:
        S = spotipy.Spotify(cache_token)
    except SpotifyOauthError:
        logging.exception('Make sure you are using the right Spotify \
                          credentials.')
    return S
