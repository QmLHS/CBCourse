# Environments: Choose the right room to accomplish a task

More often than not, to accomplish a task you need several tools (i.e. software), and according to the task itself, you
need specific tools.

Solving different tasks will lead you to continuously add new software that increase the probability of software
conflicts.

Creating an environment for each task (or small group of heterogeneous tasks) will help to avoid software conlicts.

`conda` is the tool to easily manage environments.

## Installing conda

First of all you need to install the package manager. I suggest to use miniconda3.

To install it, follow the instructions at the following link [Miniconda — conda documentation](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links)


## Creating an environment

To create a new environment is simple as this:

`conda create -n MyEnvironmentName`

then you need to activate it

`conda activate MyEnvironmentName`

and populate it with the available software of your choice

`conda install python=3.11 pandas matplotlib`

With the line above, you will install python (version 3.11), its two libraries matplotlib and pandas, with all the
necessary programs (dependencies).

From now on, whenever you need to use pyhon together with pandas or matplotlib, it is enough to activate de environment
and use them.

Remember that the programs installed within an environment are available only within that environment.


## Using an environment

To "enter" an environment you need to explicitly activate it:

`conda activate environmentName`

Once finshed, you can "exit" the environment by deactivating it:

`conda deactivate`

Tobtain the list of all the available environments, digit

`conda info --envs`



## Sharing an environment

It is possible to save a snapshot of an environment in order to share it, or to port it on another computer.

```bash
conda activate MyEnvironmentName
conda env export > environment.yml
```

then, you can create an exact copy of it running

```bash
conda env create -f environment.yml
```

## Removing an environment

To completely remove an environment from your computer, digit

`conda env remove --name MyEnvironmentName`



## Conda channels

A conda channel is a compilation of packages. Some of them are thematics `bioconda` or tries to have the most up to date
cross platform version of the packages `conda-forge`

To add a channel to an environment run

```bash
conda config --append channels conda-forge
```


## Example:

Create an environment to perform exploratory data analyses with python.
Let's say we need python (3.11), ipython (to ease the use of python), pandas (to mangle the data), openpyxl (to write *.xlsx) and matplotlib to
visualize the information.

```bash
conda create -n dataAn python=3.11
conda activate dataAn
conda install ipython pandas openpyxl matplotlib
```

or from the file `condaEnvDataAnalysisMinimal.yml`

`conda create -f condaEnvDataAnalysisMinimal.yml`


