#%%
from src import *
import os
import pandas as pd
import numpy as np

feat_msd = FeaturizerMusicnn('MSD_musicnn')
print(feat_msd.tags)

feat_mtt = FeaturizerMusicnn('MTT_musicnn')
print(feat_mtt.tags)

#%%
spot_data_path  = os.path.join('/home/ubuntu','insight','spot_datasets')
results_path  = os.path.join(spot_data_path, 'results_cats.csv')

results_df = pd.read_csv(results_path)

id0 = results_df['k'] < 101
id1 = ~results_df['model_type'].str.match('MTT_vgg')
id2 = ~results_df['model_type'].str.match('MSD_vgg')
sub_df = results_df.loc[id0 & id1 & id2]
sub_df.sort_values(by = 'recall_at_k', ascending = False, inplace = True)
sub_df.groupby(['k','model_type']).head(2).sort_values(by = ['k', 'model_type'])
#%%
