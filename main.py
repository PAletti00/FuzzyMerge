# Imports
import pandas as pd
from difflib import SequenceMatcher


# File directories and file names
dir1 = 'filepath1'
file_master = 'all_authors_list_top50.csv'

dir2 = 'filepath2'
file_new = 'authorsonly.csv'

dir_output = 'filepath3'
file_output = 'Output.csv'

# Load data sets
df_master = pd.read_csv(dir1 + file_master)
df_master[['Name', 'Frequency']] = df_master['author,_freq'].str.split(',', expand=True)
df_master['Source'] = 'Master Dataset'
del df_master['author,_freq']

df_new = pd.read_csv(dir2 + file_new)
df_new[['Name', 'Frequency']] = df_new['coauthor,_freq'].str.split(',', expand=True)
df_new['Source'] = 'New Dataset'
del df_new['coauthor,_freq']


# Merge the two data sets
df_merged = pd.concat([df_master, df_new])


# First remove all duplicates that are identical matches
df_merged.drop_duplicates(subset='Name', keep="first", inplace=True)
df_merged.reset_index(drop=True, inplace=True)


# Then remove duplicates based on a high similarity ratio (>0.75)
for index1, row1 in df_merged.iterrows():
    name1 = row1['Name']

    for index2, row2 in df_merged.iterrows():
        name2 = row2['Name']

        if index2 > index1:
            similarity_score = SequenceMatcher(None, name1, name2).ratio()

            if similarity_score > 0.75:
                df_merged.drop(index2, inplace=True)
            else:
                pass

              
# Save output as CSV
df_merged.to_csv(dir_output + file_output, index=False)
