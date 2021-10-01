# Requirements:

To install the necessary requirements, we provide a environment.yml file that can be used with anaconda. Of course you can use any other means of installing the requirements listed in this file.

The required packages are:  
matplotlib=3.4.2  
numpy=1.20.3  
The code could run using older versions as well.

## Jupyter Notebook

The classic Jupyter Notebook can be installed with conda:
```conda install -c conda-forge notebook```

If you use pip, you can install it with:
```pip install notebook```

To run the notebook, run the following command at the Terminal:
```jupyter notebook```

## Conda Environment 

To create an environment with a specific version of Python and the required packages:

```conda create -n myenv python```
```conda install -n myenv matplotlib=3.4.2 numpy=1.20.3```
