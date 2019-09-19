# NOTE TO SELF: this was run at the top level insight directory

# file system and environment
import os
import sys

# reporting
import streamlit as st

# generic data manipulation
import numpy as np
import pandas as pd

# music specific
import musicnn 
import billboard
import spotipy
import pkgs.autoencoda.autoencoda as ae

# start by preparing environment
import spotipy
keys_path = os.path.join('~','insight','keys.csv')
keys_df   = pd.read_csv(keys_path)

# let's start by testing some package things...
st.write(os.environ['PYTHONPATH'])
st.write(sys.path)
st.write(keys_df['CLII'])
# st.write(billboard.charts())
st.write(os.getcwd())

st.write(keys_df.loc[0,'CLII'])
st.write(keys_df.loc[0,'CLIS'])

st.header('Open our spotipy instance')
spotify = ae.ingest.get_spotify_instance(keys_df.loc[0,'CLII'], keys_df.loc[0,'CLIS'])
st.write(spotify)

st.text('Define our artist and track')
track_URI, artist_URI = ae.ingest.get_spotify_from_billboard('Honey', 'Kehlani', spotify)

st.header('Does it have an mp3 preview?')
st.write(track_URI)
st.write(ae.ingest.has_mp3_preview(track_URI,spotify))
st.write('')
def build_track(track_URI, artist_URI, spotify, dir_mp3):
  track_info_from_spotify = spotify.track(track_URI)
  track = {
      'track_id': track_URI,
      'artist_id': artist_URI,
      'info': track_info_from_spotify
  }
  return track

st.header('Download our mp3')
track = build_track(track_URI, artist_URI, spotify, './test_song.mp3')
import wget
# wget.download(track['info']['preview_url'],'./test_song.mp3')

from musicnn.tagger import top_tags
st.write(top_tags('./test_song.mp3', model = 'MTT_musicnn', topN = 10))

st.header('Test out using boto!')
import boto3 
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    st.write(bucket.name)

## now try to put something on boto...
# s3.Object('songfinder', 'test_song.mp3').put(Body = open('test_song.mp3', 'rb'))
# able to put stuff on boto!!

# what about reading from boto?
from boto3 import client
conn = client('s3')
for key in conn.list_objects(Bucket='songfinder')['Contents']:
    st.write(key['Key'])

resource = boto3.resource('s3')
my_bucket = resource.Bucket('songfinder')
my_bucket.download_file('test_song.mp3', 'boto_test_song.mp3')
import librosa
song_mp3 = librosa.core.load('boto_test_song.mp3')
st.write(song_mp3)

# well. now we can both read and write from boto...

# what I want to do now is...

# [1] generate a synthetic data set for this

# need to make a LOT of progress on this thing today and tomorrow. 
# gotta be more stressed about this...
# how to do my work...

# let's take a look 
# [1] 
# [2] 
# [3] 

# let's get this system up and running!

# let's see if we can pull a dataset from the... data set...
# something like that...

# is it going to be guaranteed to actually lie closer in spcae? 
# or will it not? 

# what am I doing and how am I going to do it? 

# let's start scraping my list of music now!

# let's see... billboard
st.write(billboard.charts())

# define new songs

# date_to_choose = st.slider('year', 1990, 2019, 29) 
def get_songs(year, month = '01', day = '01', genre = 'hot-100'):
    chart = billboard.ChartData(genre, date = str(year) + '-' + month + '-' + day)
    return chart
    # songs_list = [(elem.title, elem.artist) for elem in chart]
    # # st.write(songs_list)
    # return songs_list

# list songs that have been downloaded from the database

# now... I have my chart
# should I convert that into a pandas dataframe? 

# pandas data frame with the following...
# title, artist, image, weeks, rank, isNew --- data of interest
# others: peakPos, lastPos

# make my own database
# [1] billboard metadata                  - csv
# [2] spotify metadata for unique songs   - csv
# [3] download preview mp3s from spotify  - [artist]-[song].mp3

# for now, i'll start with this piece of the problem....


st.header('HOT 100 SET')
test_set = ae.billboard_query.get_hot_100_set('2019-01-01','hot-100')
st.write(test_set)
#  test_inputs
# /data/
# /
# create a database of data
# db/[genre]-[date]-[artist]-[song]

genres = []
years  = [2010]

# 100 * 12 * 

chart = billboard.ChartData('hot-100','2018-01-01')
st.write(help(chart))
# grab the top songs 
# st.write(get_songs_from_year(1990))

# st.write()
# get_songs_from_year(date_to_choose)

# # define a list of all songs from billboard charts
# data_load_state = st.text('Loading data...')
# data = load_data(10000)
# data_load_state.text('Loading data... done!')

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# alright, let's start by creating our data set
# let's figure out how to create this data set...