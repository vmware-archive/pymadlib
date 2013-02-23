================================================================================
Python wrapper for MADlib 
Srivatsan Ramanujam <vatsan.cs@utexas.edu>, 3 Jan 2013
This currently implements Linear regression, Logistic Regression, 
SVM (regression & classification), K-Means and LDA algorithms of MADlib.
Refer : http://doc.madlib.net/v0.5/ for MADlib's user documentation.
================================================================================

Dependencies : 
===============
You'll need the python extension : psycopg2 to use PyMADlib.
  (i)  If you have matplotlib installed, you'll see Matplotlib visualizations for Linear Regression demo.
 (ii)  If you have installed networkx (http://networkx.github.com/download.html), you'll see a visualization of the k-means demo
(iii)  PyROC (https://github.com/marcelcaraciolo/PyROC) is included in the source of this distribution with permission from its developer. You'll see a visualization of the ROC curves for Logistic Regression.

Configurations:
===============
To configure your DB Connection parameters
You should create a file in your home directory : ~/.pymadlib.config 
that should look like so :

------------------------------------------------------------
[db_connection]
user = gpadmin
password = XXXXX
hostname = 127.0.0.1 (or the IP of your DB server)
port = 5432 (the port# of your DB)
database = vatsandb (the database you wish to connect to)
------------------------------------------------------------

INSTALLATION INSTRUCTIONS:
===========================
1) You may install pymadlib by downloading the source (from PyPI) and then run the following :

     sudo python setup.py build
     sudo python setup.py install
         (OR)
2) If you use easy_install or pip, simply run :
     sudo easy_install pymadlib
    

Running the Demos :
===================
You may run the demo from the extracted directory of pymadlib like so :

python example.py

        (OR)
        
If you installed PyMADlib using instructions in the previous section, then simply run

python -c 'from pymadlib.example import runDemos; runDemos()'


Datasets packaged with this installation :
=========================================
PyMADlib packages publicly available datasets from the UCI machine learning repository and other sources.

1) Wine quality dataset from UCI Machine Learning repository : http://archive.ics.uci.edu/ml/datasets/Wine+Quality
2) Auto MPG dataset from UCI ML repository : http://archive.ics.uci.edu/ml/datasets/Auto+MPG
3) Obama-Romney second presidential debate (2012) transcripts for the LDA models. 


Installation Issues:
=====================

Installing pymadlib using distutils should automatically install the dependent library psycopg2, which is required to
connect to a PostGres database (where MADlib is installed on). If you are using Mac OSX 10.6.X you may run into issues
with installing psycopg2.

Here are some blogs which discuss the issue and offer solutions:

http://hardlifeofapo.com/psycopg2-and-postgresql-9-1-on-snow-leopard/
http://www.initd.org/psycopg/articles/2010/11/11/links-about-building-psycopg-mac-os-x/


