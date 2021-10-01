# Requirements:

To install the necessary requirements, we provide a environment.yml file that can be used with [anaconda](https://anaconda.org/). Of course you can use any other means of installing the requirements listed in this file. 

The required packages are:  
```matplotlib=3.4.2```  
```numpy=1.20.3```  
The code could run using older versions as well.

## Conda Environment 

To create an environment ```autumn2021``` with the required packages, run the following command:  

```conda env create -f environment.yml```  

To activate the environment and start coding, run:

```conda activate autumn2021```

## Jupyter Notebook

If you like to run a jupyter notebook server, just as we did, you may need to install it in your current (conda) environment.
Of course, you can code in any other environment of your choice, that's why we did not include this dependency in the ```environment.yaml``` directly.

The classic Jupyter Notebook can be installed with conda:  
```conda install -c conda-forge notebook```

If you use pip, you can install it with:  
```pip install notebook```

To run the notebook, run the following command at the Terminal:  
```jupyter notebook```
