import pandas as pd

#%%
test_list = TrackListSpotify()

#%%

#%%

#%%
# test out our spotify user data explorer
test_explorer = SpotifyUserExplorer()
test_explorer.list_playlist_names()
test_explorer.get_playlist_id_from_name('copy')

#%%
test_list = TrackListSpotify()
test_list.add_all_tracks_from_public_user()
test_list.set_list_name('cocjin_all')
test_list.write_list_to_db()
test_list.populate_audio_database()

#%%
tfdf = pd.DataFrame.from_records(tf)

#%%

#%%
#%%