# Activity: Hodgkin-Huxley simulation

To create a virtual environment and install dependencies, do *only one* of the following conda or pip approaches.

### Conda approach

Copy [environment.yml](environment.yml) into the top of the repo.

Launch a terminal in the repository directory and do:

```
conda env create -f environment.yml
```

Then open the folder in VS Code, and within VS Code, open the notebook `hh_simulation.ipynb`.

Click on the python interpreter listed at the top right of the notebook, and use the menu to select the conda environment `hh-sim` that you just created from the environment file.

Run the notebook.

### Venv/Pip approach

Copy [requirements.txt](requirements.txt) into the top of the repo.

Launch a terminal in the repository directory and do:

```
python3 -m venv .venv
source .venv/bin/activate
#.\.venv\bin\activate # if on Windows
pip install -r requirements.txt
```

Then open the folder in VS Code, and within VS Code, open the notebook `hh_simulation.ipynb`.

Check the python interpreter listed at the top right of the notebook, and make sure it is from the (`.venv`) environment you just created.

Run the notebook.

### Additional Comments

If someone does not give you an environment file, you have to determine what needs to be installed on your own. For python, that usually means aggregating all the `import` statements to see what is imported. However, there are a few nuances.

The packages `os` and `sys` are part of the [standard python library](https://docs.python.org/3/library/index.html) and do not need to be installed separately (hence do not go in an environment file).

The line `from utils import hh_model` is referring to custom code within the same repo, and also does not need to be installed (though you may have to add code to get the module on the python search path).

The top level name goes in the environment file, even when only part of a package is being imported (e.g. only `scipy` when the import code is `from scipy.integrate import solve_ivp`).

There is no import statement for Jupyter notebooks themselves, but the package still needs to be in the environment. A minimal install will use `ipykernel`. One can alternatively use `jupyter`, which contains the kernel and much more. 

One can install Jupyter Lab only once on a system, and then add different kernels in different environments that become selected within the Jupyter interface.

The environment file should contain all packages needed everywhere in the code base, not just the notebook you might use directly. For example, `scipy` is not needed in the notebook but is used in `hh_model.py`.
