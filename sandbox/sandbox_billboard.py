# NOTE TO SELF: this was run at the top level insight directory

# work with billboard now... and figure out what I need to write

#%%
import billboard
import logging

# get songs in a certain date range: definition 
chart_name  = 'hot-100'
start_date  = '2019-01-01'
end_date    = '2019-02-01'

# initialize chart
chart_list  = [billboard.ChartData(chart_name, date = end_date)]
ichart = 0
while chart_list[ichart].previousDate > start_date:
    logging.info('Date {:s}'.format(chart_list[ichart].previousDate))
    chart_list.append(billboard.ChartData(chart_name, date = chart_list[ichart].previousDate))
    ichart = ichart + 1
    print(ichart)

# takes a little bit of time to scrape data from a given date range
#%% 

#%%
chart = billboard.ChartData(chart_name, date = end_date)

# works in increments of weeks...
billboard.charts()
#%%
dir(chart)

#%%
# /data/billboard_aggregate/
#                          lists_available.txt(?)
#                          [list_name]/unique_artists_songs.csv
#                                     /search_criteria.txt
#                                     /charts/
#                                     /all_metadata.csv
#      /spotify_audio/
#                     [artist]-[song]/song.mp3
#                                    /spotify_processed.csv
# /test_cases/
#            /sample_user_lists/
#            /lists_available.txt
#            /[list_name]/       
# /features/
#          /feature_sets.csv
#          /features1/[artist]-[song].pkl
# /test_params/
#       /[billboard]_[genre]_[year]_against_[aggregate_lists].csv - results 

# class billboard_aggregate
#   description:
#       given a list of 'chart_names' and 'start' and 'end' dates
#   methods:
#       data
#           parameters
#           lists
#           df_charts
#           df_artists_songs
#           df_unique_artists_songs
#       __init__(chart_names, start_date, end_date, time_increment, db_name)
#           # get all of our charts
#           # extract data from charts into artists and songs df
#           # get unique artists and songs
#           
#       #### MAIN METHODS
#       get_charts(chart_names, start_date, end_date, time_increment)
#       convert_charts_to_charts_df(charts)
#       convert_charts_to_artists_songs_df(charts)
#       find_unique_artists_songs(artists_songs_df)
#       
#       #### METHODS FOR WRITING DATA
#       write_data_to_db(base_path, list_name)
#           # write charts_df
#           # write artists_songs_df
#           # write unique artists_songs
#       
#       #### METHODS FOR COMBINING DATA SETS
#       combine_database(base_path, list_names)
#           combine charts_df
#           combine artists_songs_df
#           combine unique artists_songs
#
#       get_list_data(chart_names, start_date, end_date, time_increment[for later])
#           # grab lists of interest
#           # charts_df: dataframe of charts
#           # artists_songs_df: list of songs and artists
#           # unique_artist_songs: unique artists and songs
#       write_list_data(list_name, db_base_path)
#       write_
#       _get_unique_artists_songs()
#       _song_start_dates (later)

# class featurizer 
# song + artist name + feature sets + features

# class billboard_database:
#   __init__()
#   __init__()

# spotify 

# class billboard_database_maker
#   fetch_database_maker()
#   add_to_database(genres, start_date, end_date) 

class spotify_list_generator


# pull my own spotify data...
# and see what I can do here...