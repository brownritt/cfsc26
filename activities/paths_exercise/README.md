# Paths to data activity

This activity ties together working with paths to load data, using a simmulated data set in the [BIDS](https://bids-specification.readthedocs.io/en/stable/index.html) format. BIDS is very widely used in non-invasive human subjects imaging (fMRI, EEG, NIRS, etc), and increasingly as a systematic way to organize files even from other data sources. It is not a *file type*, but instead allows almost any type of data file to be used; BIDS specifies the way those files should be named and organized to form a cohesive *data set*.

- Make a new folder to contain with a sensible name for this project
- Download the data ZIP archive `food-ranks.zip` into that folder and uncompress it
- Browse through the data set to get a sense of its structure
- Create a python script `load_rank_data.py` that loops through all the data files and accumulates their contents into a list
  - Consider your options for how you want your code and data to be related in the filesystem, as discussed in class
  - Consider how the list should be structured given the structure of the data
  - Set appropriate paths to get to each data file
  - Troubleshooting is part of the exercise! Make a plan, try it, then evaluate if you need to make changes
- You can use the skeleton code in `load_scratch.py` as a guide for file opening and list construction
