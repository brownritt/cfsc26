# Hodgkin-Huxley simulation activity

Simulation of a Hodgkin–Huxley model of neural action potentials under constant applied current.

Your task is to get the notebook to run, and produce two figures: one of neural action potentials, and one that includes gating variables. In order to do so, you must set up the right subdirectory structure, create an environment file for the necessary packages, create the environment, and activate it.

- Create a new project directory 
- Inside that directory, create two new subdirectories, `notebooks` and `utils`
- Download [hh_model.py](hh_model.py) into `utils`
- Download [hh_simulation.ipynb](hh_simulation.ipynb) inot `notebooks`
- Look through both files and determine what packages they use
- Create a virtual environment and install these packages
  - If using pip:
    - Create a `requirements.txt` file that contains the dependencies
    - Create a local virtual environment with `python -m venv .venv`
    - Activate the environment with `source .venv/bin/activate`
    - Install the requirements with `pip install -r requirements.txt`
  - If using conda:
    - Make an `environment.yml` file that contains the dependencies
      - Note that YAML files need a little more structure than just a list of dependencies
      - At minimum, you will need to define an environment name
    - Create the environment and install the dependencies with `conda env create -f environment.yml`
    - Activate the environment with `conda activate NAME`, replacing `NAME` with the name you chose above
  - An alternative way to use conda is to manually install dependencies and then export the environment
    - `conda create -n NAME` (choose a sensible name)
    - `conda activate NAME`
    - `conda install DEPENDENCIES` (replace with the packages you identified above)
    - `conda env export --from-history environment.yml`
