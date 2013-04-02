A Python wrapper for MADlib - an open source library for scalable in-database machine learning algorithms

## Algorithms

PyMADlib currently has wrappers for the following algorithms in MADlib

1. Linear regression
1. Logistic Regression
1. SVM (regression & classification)
1. K-Means 
1. LDA 

Refer [MADlib User Docs](http://doc.madlib.net/v0.5/ ) for MADlib's user documentation.

***


## Dependencies

1. You'll need the python extension _**psycopg2**_ to use PyMADlib.
1. If you have matplotlib installed, you'll see Matplotlib visualizations for Linear Regression demo.
1. If you have installed [networkx](http://networkx.github.com/download.html), you'll see a visualization of the k-means demo
1. [PyROC](https://github.com/marcelcaraciolo/PyROC) is included in the source of this distribution with permission from its developer. You'll see a visualization of the ROC curves for Logistic Regression.



***  

## Configurations

To configure your DB Connection parameters
You should create a file in your home directory

>     ~/.pymadlib.config 

that should look like so :


>     [db_connection]  
>     user = gpadmin  
>     password = XXXXX  
>     hostname = 127.0.0.1 (or the IP of your DB server)  
>     port = 5432 (the port# of your DB)  
>     database = vatsandb (the database you wish to connect to)  



***


## Installation Instructions

1. You may install pymadlib by downloading the source (from PyPI) and then run the following

>     sudo python setup.py build
>     sudo python setup.py install

2. If you use easy_install or pip, simply run :

>     sudo easy_install pymadlib
    

***

## Usage Tutorial

Visit [PyMADlib Tutorial](http://nbviewer.ipython.org/5275846) for a tutorial on using PyMADlib
Also visit [PyMADlib IPython NB](https://gist.github.com/vatsan/5275846) to download the IPython NB tutorial


## Running the Demos

You may run the demo from the extracted directory of pymadlib like so :

>     python example.py

        
If you installed PyMADlib using instructions in the previous section, then simply run

>     python -c 'from pymadlib.example import runDemos; runDemos()'

Remember to close the Matplotlib windows that pop-up to continue with the rest of the demo.


***

## Gallery

![K-Means Cluster Visualization](https://lh3.googleusercontent.com/-bXz3gCrnQFo/UTu3lXFKbeI/AAAAAAAAKgI/Hpjsqzb_GTQ/w776-h714-p-o-k/kmeans_networkx_viz.png)

![Scatter Plot - Linear Regression (numeric attributes only)](https://lh3.googleusercontent.com/-esbS5NTl58E/UTu3lfBqUXI/AAAAAAAAKgE/tawiqnTgYLQ/w470-h353-o-k/linear_reg_scatter_1.png)

![Scatter Plot - Linear Regression (with categorical attributes)](https://lh6.googleusercontent.com/-vNTw5Q6d0pg/UTu3lVjBIzI/AAAAAAAAKgA/pbiLfGiYisw/w470-h353-o-k/linear_reg_scatter_2.png)

![ROC Curve - Logistic Regression](https://lh3.googleusercontent.com/-ymBoJ7qQo-o/UTu3l9RUBvI/AAAAAAAAKgU/_Mc0jiM_Yq0/w470-h353-o-k/logistic_reg_pyroc.png)

![Random graph visualization - Networkx](https://lh6.googleusercontent.com/-H-3h0bV8EDQ/UTu3lyED9YI/AAAAAAAAKgY/CcoJ2oSme2M/s353-c-o-k/random_networkx_viz.png)

***  


## Datasets packaged with this installation

PyMADlib packages publicly available datasets from the UCI machine learning repository and other sources.

1. [Wine quality dataset from UCI Machine Learning repository](http://archive.ics.uci.edu/ml/datasets/Wine+Quality)
1. [Auto MPG dataset from UCI ML repository from UCI Machine Learning repository](http://archive.ics.uci.edu/ml/datasets/Auto+MPG)
1. [Wine quality dataset from UCI Machine Learning repository](http://archive.ics.uci.edu/ml/datasets/Wine+Quality)
1. Obama-Romney second presidential debate (2012) transcripts


***

## Installation Issues


Installing pymadlib using distutils should automatically install the dependent library psycopg2, which is required to connect to a PostGres database (where MADlib is installed on). If you are using Mac OSX 10.6.X you may run into issues with installing psycopg2.

[psycopg2-and-postgresql-9-1-on-snow-leopard](http://hardlifeofapo.com/psycopg2-and-postgresql-9-1-on-snow-leopard/) and [links-about-building-psycopg-mac-os-x](http://www.initd.org/psycopg/articles/2010/11/11/links-about-building-psycopg-mac-os-x/) discuss the issue and offer some solutions.


***

##### Srivatsan Ramanujam <vatsan.cs@utexas.edu>, 3 Jan 2013
