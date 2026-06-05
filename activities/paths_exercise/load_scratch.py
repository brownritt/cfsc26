# load_scratch.py
#
# Part of Paths Exercise:
#   https://github.com/brownritt/cfsc26/blob/main/activities/paths_exercise/files_exercise.md
#
# Part of the Computational Fluency Short Course 2026, in the Carney Institute for 
# Brain Science at Brown University.
# 
# Provides template code for accessing files and loading into arrays. Should be
# modified in your own code to load the BIDS data set in the activity folder.
#
# This code will not run on your machine as written !

# %% Initializations and imports

import os

# As a diagnostic, print the working directory
print(f"The code's current working directory is {os.getcwd()}")
print(f"The current working directory's content is {os.listdir( os.getcwd() )}")

# %% Open a single file, read all lines, then print each line

# Define a path to a data file
data_dir = r'/Users/jritt/Expts/fMRI_study/food_ranking'
file_name = r'data.txt'
FILEPATH = os.path.join(data_dir, file_name)

with open(FILEPATH, 'r') as f:
    lines_all = f.readlines()
    for line in lines_all:
        print(line)

# Aside: with...as uses a "context manager" to open the file.
# This motif provides some convenience and also protection 
# against possible file handling errors (files will "close
# cleanly" even if something inside the `with` block throws
# an error).

# %% Loop thorugh a file list

list_of_files = ['file1.txt', 'file2.txt', 'file3.txt']

data_list = []
for file_idx, file_name in enumerate(list_of_files):
    print(f'Working on file number {file_idx}')
    FILEPATH = os.path.join(data_dir, file_name)
    with open(FILEPATH, 'r') as f:
        rank_list = []
        lines_all = f.readlines()
        for line in lines_all:
            rank_list.append(line)
    data_list.append( rank_list ) 

# Note this "list within a list" structure. You can nest more
# loops if it makes sense 