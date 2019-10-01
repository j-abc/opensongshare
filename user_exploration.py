import streamlit as st 
from src import * 
import pandas as pd

class StreamlitInterface:
    def __init__(self, use_streamlit = True, display_instructions = True):
        self.use_streamlit = use_streamlit
        self.display_instructions = display_instructions

    def select_user(self, instructions = ''):
        default_user = ''
        user_id = default_user
        if self.use_streamlit:
            user_id = st.text_input(label = instructions, value = default_user)
        return user_id

    def write(self, *inputs):
        if self.use_streamlit:
            st.write(*inputs)
        else: 
            print(*inputs)

    def select_single_playlist_from_user(self, user_id, instructions = 'Select a playlist of interest'):
        user_explorer = SpotifyUserExplorer(user_id)
        playlists = user_explorer.list_playlist_names().tolist()
        if self.use_streamlit:
            index = st.selectbox(instructions, ['', 'all playlists'] + playlists)
            if index == 0:
                playlist_name = ''
                playlist_id   = ''
            elif index == 1:
                playlist_name = 'all playlists'
                playlist_id = 'all'
            else:
                playlist_name = playlists[index-2]
                playlist_id   = user_explorer.get_playlist_id_from_name(playlist_name)
            return playlist_id, playlist_name

    def display_tracks_in_tracklist(self, tracklist):
        st.write(tracklist.dataframe.loc[:,['name', 'artist_names']])


while True: 
    my_interface = StreamlitInterface(use_streamlit = True)

    ##### DEFINING OUR USERS
    users = {}
    users['1'] = {}
    users['2'] = {}

    st.header('OpenSongShare')
    st.subheader('Helping friends share music')

    st.markdown('***')
    st.subheader('First, enter your and your friend\'s Spotify user ids.')
    users['1']['id'] = my_interface.select_user('Enter your Spotify user id:')
    try:
        users['1']['explorer'] = SpotifyUserExplorer(users['1']['id'])    
        users['1']['valid_user'] = True
    except: 
        users['1']['valid_user'] = False
        if users['1']['id']:
            st.write('Your specified spotify id does not exist, please enter another.')

    users['2']['id'] = my_interface.select_user('Enter your friend\'s Spotify user id:')
    try:
        users['2']['explorer'] = SpotifyUserExplorer(users['2']['id'])    
        users['2']['valid_user'] = True
    except: 
        users['2']['valid_user'] = False
        if users['2']['id']:
            st.write('Your friend\'s specified spotify id does not exist, please enter another.')
    
    if not users['1']['valid_user'] or not users['2']['valid_user']:
        break

    ##### DEFINING SEED AND DATABASE
    
    st.subheader('Who is recommending songs to whom?')
    sel_idx = st.selectbox('', ['---','I am recommending songs to my friend.', 'My friend is recommending songs to me.'], value = 0)

    if sel_idx == 0:
        break

    st.markdown('***')
    st.subheader('Which playlist would you like to compare?')
    st.write("Or, if you want, you can compare against all recent playlists by selecting the ''all recent playlists'' option")


    users['1']['sel_play_id'], users['2']['sel_play_name'] = my_interface.select_single_playlist_from_user(users['1']['id'], 
    'Select one of your playlists')

    users['2']['sel_play_id'], users['2']['sel_play_name'] = my_interface.select_single_playlist_from_user(users['2']['id'], 
    "Select one of your friend's playlists")

    if not users['1']['sel_play_id'] or not users['2']['sel_play_id']:
        break
    
    # now get all of the tracks from this playlist
    for idx in ['1', '2']:
        users[idx]['tracklist'] = TrackListSpotify(user = users[idx]['id'])
        if users[idx]['sel_play_id'] == 'all':
            users[idx]['tracklist'].add_all_tracks_from_public_user()
        else:
            users[idx]['tracklist'].add_tracks_from_public_user_playlist(users[idx]['sel_play_id'])
        users[idx]['tracklist'].remove_tracks_with_missing_previews()
        users[idx]['tracklist'].remove_duplicate_tracks()

    st.write('Here are the songs in your playlist!')
    my_interface.display_tracks_in_tracklist(users['1']['tracklist'])

    st.write("And in your friend's playlist!")
    my_interface.display_tracks_in_tracklist(users['2']['tracklist'])


    feat_musicnn   = FeaturizerMusicnn()
    for idx in ['1', '2']:
        track_ids      = users[idx]['tracklist'].dataframe['id'].values
        track_features = feat_musicnn.get_features_for_tracks(track_ids)
        features_df    = pd.DataFrame.from_records(track_features)
        # tagmat         = np.vstack(features_df['taggram'].values)
        # tag_df         = pd.DataFrame(data = tagmat, columns = feat_musicnn.tags)
        # tag_df['id']   = features_df['id']
        users[idx]['feat_df'] = features_df

    from sklearn.metrics.pairwise import pairwise_distances
    import numpy as np

    def rank_db_from_playlist(pl_feat_df, db_feat_df, db_list_df, feature_name = 'taggram', metric = 'euclidean', num_songs = 20): 
            pl_feat_array = np.vstack(pl_feat_df[feature_name].values)
            db_feat_array = np.vstack(db_feat_df[feature_name].values)

            dmat = pairwise_distances(X = db_feat_array, Y = pl_feat_array, metric = metric)

            collapse_dmat = np.mean(dmat, axis = 1)
            print(collapse_dmat.shape)

            sorted_db_idx = np.argsort(collapse_dmat)
            # sorted_db_idx = sorted_db_idx[::-1] # turn on for euclidean to get worst songs
            # top 5 and bottom 5 - and user assessment
            which_db_songs = sorted_db_idx[:num_songs]
            id_df = db_feat_df.loc[which_db_songs,['id']]
            id_df.insert(1, "rank", [i for i in range(id_df.shape[0])], True)
            return pd.merge(id_df, db_list_df, on = 'id')

    if sel_idx == 0:
        pl_id = '1'
        db_id = '2'
    else:
        pl_id = '2'
        db_id = '1'


    which_prompt = ['Here are the songs that you should give to your friend!', "Here are songs that you may like in your friend's playlist!"]
    st.subheader(which_prompt[sel_idx])
    rank_df = rank_db_from_playlist(users[pl_id]['feat_df'], users[db_id]['feat_df'], users[db_id]['tracklist'].dataframe)
    st.write(rank_df)

    # let's look at this in latent dimensional space!
    

    break
