# load_rank_data.py
#
# Script that provides an example completion of the Paths Activity:
#   https://github.com/brownritt/cfsc26/blob/main/activities/paths_exercise/files_exercise.md
#
# Part of the Computational Fluency Short Course 2026, in the Carney Institute for 
# Brain Science at Brown University.
#
# Loads a set of data files in a BIDS archive and accumulates the contents
# in a list of lists. See the BIDS archive README for experimental details.
#
# There are many different ways one could go about loading these
# files, and the code below is just an example. A key decision point
# is usually how general to make the code: it's often easier at first
# to hardcode file names and subdirectories, but then the code will not
# work if the data set changes (e.g. adds a new subject).
#
# Here we take a middle approach, where we use our knowledge of the data
# structure to set up nested loops and accumulate files into lists, but
# we use os.listdir to get hte subdirectory names, and do not assume how 
# many subjects there were, or how many sessions each subject did.

# %% Initializations and imports

import os

# Define a path to the top of the data set
data_dir = r'food-ranks'  # Relative to the current working directory

# Because of the way Windows uncompresses ZIP files, you might need
# to change the line to
# data_dir = r'food-ranks\food-ranks'

# If you put the data somewhere else, adjust the line with the correct
# absolute or relative path to the top level of the BIDS data set.

print(f'\n\nCurrent working directory is {os.getcwd()}')
print(f'  Will look for data in {data_dir}\n')

# The data is organized as
#
# data_dir/
#   Subject directories (sub-xx)/
#     Session directories (ses-xx)/
#       beh/
#         sub-xx_ses-xx_task-foodrank_beh.txt
#
# The seemingly extra "beh" directory is due to a BIDS convention
# to separate different types of data. "beh" refers to behavioral 
# data (the subjects' choice of rankings); had there been other
# data sources like EEG, those could go in separate subdirectories.


# %% Make a list of subject subdirectories

# The top of a BIDS archive contains files, generally known
# as "metadata", that contains information _about_ the data,
# such as demographic information about each subject. 
# We want to keep only the names that begine with 'sub'.

sub_dir_list = []
for name in os.listdir(data_dir):
    if name[:3]=='sub':
        sub_dir_list.append(name)
print(f'List of subject directories is {sub_dir_list}\n')

# %% Loop through subjects and sessions and load the data

# We now rely on the known structure of the data archive:
# For each subject, we loop through session directories, 
# each of which contains a subdirectory `beh` that contains
# only one data file.

# We will accumulate all the sessions for a given subject into a 
# list, and then append each subject within the full `data_list`.
#
# This "list of lists" approach preserves the hierarchical
# structure of the BIDS archive in the way we store it in memory.


print('Loading the data ...')

# Initialize a list into which we will accumulate all data
data_list = [] 

for sub_dir in sub_dir_list:
    # sub_dir is the name of the subdirectory, _not_ the
    # relative path to reach it from the current working 
    # directory. Make sure you understand why the next line
    # is necessary:
    sub_path = os.path.join(data_dir,sub_dir)

    # Now get the session directories within this subject:
    print(f'- Looking for sessions in {sub_path}:')
    ses_dir_list = os.listdir(sub_path)

    sub_list = [] # Initialize a list to hold this subject's sessions

    for ses_dir in ses_dir_list:
        # Check is actually a session directory
        if ses_dir[:3] == 'ses':

            # Again, we build a complete relative path from
            # the current working directory:
            ses_path = os.path.join(sub_path,ses_dir,'beh')
            print(f'- - Looking for data file in {ses_path}')

            file_list = os.listdir(ses_path)
            for file_name in file_list:
                # Check begins with the right name for a data file
                if file_name[:3] == 'sub': 
                    # Again need to define a complete relative path               
                    FILEPATH = os.path.join(ses_path,file_name)

                    print(f'- - - Getting rankings from {file_name}')
                    rank_list = [] # Initialize rank list for this session
                    with open(FILEPATH, 'r') as f:
                        lines_all = f.readlines()
                        for line in lines_all:
                            rank_list.append( line.strip() )
                            # .strip() is a flourish that removes the
                            # newline ('\n') characters from the data
                    # Add this session's rankings to this subject's list
                    sub_list.append( rank_list )

    # Now append this subject's list to the full data list
    data_list.append(sub_list)

print('... finished loading data')

print(f'\nThe loaded data set is:\n{data_list}')

# Note python is a "0-offset" language; indicies are one less than English usage
print(f'\nThe 4th subject in their 2nd session gave ranks:\n{data_list[3][1]}')

# %% Extra 1: What could a hardcoded "brute force" approach look like?

import os

data_dir=r'food-ranks'  # Relative to the current working directory

list_of_files = ['sub-01/ses-01/beh/sub-01_ses-01_task-foodrank_beh.txt',
                 'sub-01/ses-02/beh/sub-01_ses-02_task-foodrank_beh.txt',
                 'sub-02/ses-01/beh/sub-02_ses-01_task-foodrank_beh.txt',
                 'sub-02/ses-02/beh/sub-02_ses-02_task-foodrank_beh.txt',
                 'sub-03/ses-01/beh/sub-03_ses-01_task-foodrank_beh.txt',
                 'sub-03/ses-02/beh/sub-03_ses-02_task-foodrank_beh.txt',
                 'sub-04/ses-01/beh/sub-04_ses-01_task-foodrank_beh.txt',
                 'sub-04/ses-02/beh/sub-04_ses-02_task-foodrank_beh.txt',]

data_list = []
#print('Loading data...')
for file_idx, file_name in enumerate(list_of_files):
    #print(f'- Working on file number {file_idx}')
    FILEPATH = os.path.join(data_dir, file_name)
    with open(FILEPATH, 'r') as f:
        rank_list = []
        lines_all = f.readlines()
        for line in lines_all:
            rank_list.append( line.strip() )
            # .strip() is a flourish that removes the
            # newline ('\n') characters from the data
    data_list.append( [file_idx,rank_list] )
#print('... finished loading data')

# Now we have two "aligned" lists (the list of files, and the list of responses), 
# so to keep track of which rankings went with which sessions, we refer to the 
# index stored each time a file was loaded:

data_idx = 5  # Can be 0 to 7, for 4 subjects with 2 sessions each

file_idx = data_list[data_idx][0]  # First entry is index into file the data came from
ranking = data_list[data_idx][1]  # Second entry is the actual list of rankings
file_name = list_of_files[file_idx]  # Aligned list tells us where data came from

print(f'\nThe data file {file_name}\ncontains the ranks {ranking}\n')

# %% Extra 2: Building names with string conversion

# Yet another approach would hardcode the "tags" in the filenames, and use
# python string conversion to build filenames. For example, one could write
#
#   sub_num = 3 # Note: these are 1-offset, since they refer to BIDS names
#   ses_num = 1
#   file_name = f'sub-{sub_num:02d}_ses-{ses_num:02d}_task-foodrank_beh.txt'
#
# One would build the relative paths a similar way. The `:02d` is needed to
# add leading zeros, as in the BIDS convention file names.
#
# Completing this approach is left as an exercise.
