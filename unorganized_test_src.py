from songfinder.src import *

#%%
test_connector  = SpotifyConnector()
#%%
test_user       = SpotifyUserExplorer()
test_user.list_playlist_names()
test_user.get_playlist_id_from_name('nn')

#%%
audio_db        = DatabaseSpotifyAudio()

test_list       = TrackListSpotify()
test_list.add_tracks_from_public_user_playlist
test_list.load_list_from_db('cocjin_all_v2') # need to write the list to the db

db_list         = TrackListSpotify()
test_list.load_list_from_db('nn') # need to write the list to the db

#%%


featurizer = MusicnnFeaturizer()
#%%
features_records = featurizer.get_features_for_tracks(['0ac2BxpvOntMSC5zfLzU2i', '0ac2BxpvOntMSC5zfLzU2i'], recalculate = False)
import pandas as pd
features_df      = pd.DataFrame.from_records(features_records)
#%%
