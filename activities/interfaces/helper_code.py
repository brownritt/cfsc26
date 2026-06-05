# Example of a "helper" module
#
# Usually these are a bunch of function defintions meant to be imported by
# a different "main" code file.

# Example of imports that will or won't work depending on the environment:
#import numpy as np

# %%
def square(x):
    return x**2

# %% Example of including tests

assert square(0)==0
assert square(-1)==1
assert square(2)==4
#assert square(3)==1  # Uncomment to see the test fail
