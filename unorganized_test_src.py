from songfinder.src import *

#%%
test_connector  = SpotifyConnector()
test_user       = SpotifyUserExplorer()
audio_db        = DatabaseSpotifyAudio()

test_list       = TrackListSpotify()
test_list.load_list_from_db('cocjin_all_v2') # need to write the list to the db

db_list         = TrackListSpotify()
test_list.load_list_from_db('nn') # need to write the list to the db

#%%
