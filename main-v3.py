# This version uses Python lists instead of pandas dataframe to to do the comparisons
# It should be a bit faster...

# Imports
import pandas as pd
from whoswho import who
from difflib import SequenceMatcher
import time

# Insert row_limit (how many names to use from each dataset)
# If no limit, comment out this line:
row_limit = 200

# File directories and file names
dir1 = '/Users/henrihapponen/Desktop/'
file_master = 'authors.csv'

dir2 = '/Users/henrihapponen/Desktop/'
file_new = 'coauthors.csv'

dir_output = '/Users/henrihapponen/Desktop/'
file_output = 'Output.csv'
file_matches = 'Matches.csv'

# Start timer
start_time = time.time()

# Load data sets
df_master = pd.read_csv(dir1 + file_master)
df_master['Name'] = df_master['author_name']
df_master['Source'] = 'Master Dataset'
del df_master['author_name']

df_new = pd.read_csv(dir2 + file_new)
df_new['Name'] = df_new['coauthor_name']
df_new['Source'] = 'New Dataset'
del df_new['coauthor_name']

# If row_limit, then subset datasets
if 'row_limit' in globals():
    df_master = df_master[:row_limit]
    df_new = df_new[:row_limit]
else:
    pass

# Make a full list of names
master_list = df_master['Name'].tolist()
new_list = df_new['Name'].tolist()
full_list = master_list + new_list

print(f'Length of full list before dropping identical matches: {len(full_list)}')

# First remove all duplicates that are identical matches
full_list = list(dict.fromkeys(full_list))

print(f'Length of full list after dropping identical duplicates: {len(full_list)}')

fuzzy_matches = []

# Then remove duplicates based on a high similarity ratio
for index1, name1 in enumerate(full_list):
    for index2, name2 in enumerate(full_list):

        if index2 > index1:
            similarity_ratio = SequenceMatcher(None, name1, name2).ratio()
            similarity_score = who.ratio(name1, name2)

            if similarity_ratio > 0.75 and similarity_score > 75:
                fuzzy_matches.append({'Index1': index1,
                                      'Name1': name1,
                                      'Index2': index2,
                                      'Name2': name2})
                del full_list[index2]
            else:
                continue
        else:
            continue

print(f'Length of full list after dropping fuzzy duplicates: {len(full_list)}')

# Create a dataframe for the resulting list
df_out = pd.DataFrame()
df_out['author_name'] = full_list

# Also create a dataframe of all the fuzzy matches
df_matches = pd.DataFrame(fuzzy_matches)
print(f'Number of fuzzy matches found: {len(df_matches)}')

# Save output as CSV
df_out.to_csv(dir_output + file_output, index=False)
df_matches.to_csv(dir_output + file_matches, index=False)

time_elapsed_minutes = int((time.time() - start_time) / 60)
time_elapsed_seconds = round((time.time() - start_time) % 60, 2)
print(f'Time elapsed: {str(time_elapsed_minutes)} minutes and {str(time_elapsed_seconds)} seconds')
