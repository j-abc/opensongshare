class ModelEvaluator:
    def __init__(self, recommender, playlist_ids, database_ids):
        # take in a dataframe of...
            # input_data         ---> playlist_id, track_id, input track data
            # database_track_ids ---> unique track_ids, database itself
            # database_labels    ---> playlist_id, track_id, database ground truth 
        # evaluates... 
            # mean average precision - definitely
            # mean average recall    - definitely
            # MAE? RMSE?
        pass

    # for each playlist, 
        # feed playlist track ids and database track ids into the recommender

    def precision :
        pass

    # feature_weightings
        # 
        # 

    # switch rank type
        # KNN - nearest neighbors to the input data set at all 
            # distance to 
            # https://gis.stackexchange.com/questions/297540/performing-knn-between-two-3d-sets-of-points-pointclouds
        # MeanDistance
        # SingleCentroid
        # icaCentroid

    # mean distnace - implemented!!!
        # KNN to the dataset 
        # SingleCentroid
        # icaCentroid

# two things to do:
    # taken from agglomerative clustering 
    # 1] KNN - nearest neighbors to the input data
         # single linkage
         # complete linkage
         # mean linkage 
    # 2] Centroid
    # 3] ICA Centroids
        # single linkage
        # complete linkage
        # mean linkage
    # 4] PCA Centroids
        # single linkage
        # complete linkage
        # mean linkage
    
# top5% and top10% metrics
    # then try it on the validation set
# did it perform as we expect for the validation set? 
    # we tried 3 + 1 + 3 + 3 crossed with 
    # 2 models * 2 tag sets * 2 possible layers 





class ModelEvaluator:
    def __init__(self):
        pass

# recommender system recall
# recommender system precision 
# https://towardsdatascience.com/recommendation-systems-models-and-evaluation-84944a84fb8e

# show the recall and precision 
# mean accuracy error
# 1 - 1
# 1 - 0 
# RMSE
# correlation? 

# accurayc metric of the 
# https://towardsdatascience.com/recommendation-systems-models-and-evaluation-84944a84fb8e
# https://www.kaggle.com/gspmoreira/recommender-systems-in-python-101

# basically, what I got out of that is that we can analyze features of the songs. 
# 5 seconds - not really useful right now.
    # time to move on!

# building the recommender system itself...
# how do we do this reasonably? 


# recall at k: # of our recommendations that are relevant/# of all possible relevant items
# preceision at k: # of our recommendations that are relevant/ # of items that we recommended

# https://medium.com/@armandj.olivares/building-nlp-content-based-recommender-systems-b104a709c042

# target: recall and precision, 
# decision support metrics

# https://github.com/microsoft/recommenders

# code for recommendation engine

# train/test split


# content based recommendation is actually formulated as...
# user, song, score
# user, song, score
# user, song, score

# so... in the training process, I am asking:

# database: toss 1000 songs into the database, from all playlists
# train set: 40 playlists, 10 songs each = 350 songs
# test set:  10 playlists, 10 songs each = 150 songs

# training the algorithm? 

# okay.. this finally makes sense
# how do we learn a user profile? 

# what is the user embedding space? 
# how do we learn a user profile? 
# in this case, we have a fixed number of documents... 

# [user data] --> [user embedding] [compared with] [document embedding] --> [document]

# what is the training? 
# the training is a bit silly...
# it's a stack of songs

# okay... well... how do I want to cast this? 

# can I find songs that belong? 

# what do all of you think is going to be relevant? 

# train a matrix factorization
# and then choose the songs that are highest rated among all of you 

# we would need more user data for this purpose to actually do it...

# but we don't have that here...
# so we're dealing with the cold start problem.

# and in the cold start problem...

# what we have is...
# basically...

# the problem of...
# I'M NOT TOO SURE ABOUT THIS TBH. 
# what do I need to do and how do I need to do it. 

