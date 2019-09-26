from src import * 
#%%
audio_db        = DatabaseSpotifyAudio()
test_connector  = SpotifyConnector()
test_user       = SpotifyUserExplorer()

test_user.list_playlist_names()
playlist_id = test_user.get_playlist_id_from_name('nn')

test_list       = TrackListSpotify()
test_list.add_tracks_from_public_user_playlist(playlist_id)
test_list.remove_tracks_with_missing_previews()

musicnn_featurizer = FeaturizerMusicnn()
test_feat = musicnn_featurizer.get_features_for_track('2XMTqoHHSH0lvuXrvIEdco')

#%%
test_connector  = SpotifyConnector()

#%%
spot_featurizer    = FeaturizerSpotify()
test_feature = spot_featurizer.get_features_for_track('2XMTqoHHSH0lvuXrvIEdco')

#%%

#%%
features_records = featurizer.get_features_for_tracks(['0ac2BxpvOntMSC5zfLzU2i', '0ac2BxpvOntMSC5zfLzU2i'], recalculate = False)
import pandas as pd
features_df      = pd.DataFrame.from_records(features_records)
#%%
from songfinder.src import *

#%%

db_list = TrackListSpotify()

#%%
