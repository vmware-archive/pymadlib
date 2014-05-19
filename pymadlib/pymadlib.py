'''
    Python wrapper for MADlib 
    vatsan.cs@utexas.edu, 3 Jan 2013
    This currently implements the following algorithms of MADlib 0.5: 
        1) Linear regression   (+ can also accept categorical columns as features)
        2) Logistic Regression (+ can also accept categorical columns as features)
        3) SVM (regression & classification) and 
        4) K-Means & 
        5) PLDA 
    Refer : http://doc.madlib.net/v0.5/ for MADlib's user documentation.
'''
from utils import pivotCategoricalColumns, convertsColsToArray
import psycopg2
from psycopg2 import extras
from psycopg2.extensions import cursor as _cursorbase

class DBConnect(object):
        _cursor = None
        @classmethod
        def getConnectionString(cls):
            ''' 
                Read the DB connection parameters from a config file.
                You should create a file in your home directory : ~/.pymadlib.config 
                that should look like so :
                ------------------
                [db_connection]
                user = gpadmin
                password = XXXXX
                hostname = 127.0.0.1 (or the IP of your DB server)
                port = 5432 (the port# of your DB)
                database = vatsandb (the database you wish to connect to)
                ------------------
                Output : Returns the connection string of the form :
                "host='{hostname}' port ='{port}' dbname='{database}' user='{username}' password='{password}'"
            '''
            
            import os
            import ConfigParser
            config_file = os.path.join(os.path.expanduser('~'),'.pymadlib.config')
          
            config = ConfigParser.ConfigParser()
            if( not os.path.exists(config_file)):
                raise Exception('DB connection configuration file not found at {path}'.format(path=config_file))
              
            config.read(config_file)
            username = config.get('db_connection','user')
            password = config.get('db_connection','password')
            hostname = config.get('db_connection','hostname')
            port = config.get('db_connection','port')
            database = config.get('db_connection','database')
            conn_string = "host='{hostname}' port ='{port}' dbname='{database}' user='{username}' password='{password}'"
            conn_string = conn_string.format(hostname=hostname,port=port,database=database,username=username,password=password)
            conn_dict = {}
            conn_dict['username']=username
            conn_dict['password']=password
            conn_dict['hostname']=hostname
            conn_dict['port']=port
            conn_dict['database']=database
            conn_dict['conn_string']=conn_string
        
            return conn_dict    
        
        def __init__(self,conn_str=None,madlib_schema=None):
            ''' Connect to the DB using Psycopg2, if conn_str is not provided, then it is read from .pymadlib.config file '''
            self.conn = psycopg2.connect(conn_str if conn_str else DBConnect.getConnectionString()['conn_string']) 
            self.madlib_schema = madlib_schema if madlib_schema else 'madlib'
            
        def getCursor(self,withhold=True):
            ''' Return a named cursor '''  
            if(self._cursor and not self._cursor.closed):
                self._cursor.close()
            self._cursor = self.conn.cursor('my_unique_cursor',cursor_factory=extras.DictCursor,withhold=withhold)
  
            return self._cursor
        
        def executeQuery(self,query):
            ''' Execute a Query '''
            import sys
            cursor = self.conn.cursor() 
            self._cursor = cursor    
            try:
                cursor.execute(query)
                self.conn.commit()
                cursor.close()
            except:
                _exType, _exVal, exTrace = sys.exc_info()
                print 'Statement failed:', query
                print 'Stacktrace :',dir(exTrace)    
                cursor.close()
                
        def fetchRowsFromCursor(self, cursor):
            '''
               Return a list of all rows fetched from the cursor.
               WARNING :
               ========= 
               Calling this method is discouraged if the query returns a large number of rows.
               It is recommended that you iterate over the cursor in that case.
               
               Inputs:
               =======
               cursor : A cursor object (pointing to the result of a query execution)
               Outputs:
               ========
               A list of all rows fetch from the cursor
            '''
            rows = [r for r in cursor]
            cursor.close()
            return rows
        
        
        def fetchColumns(self, rowset, columns=[]):
            """
               Fetch the specified columns from the cursor. If columns is empty, all columns will be fetched.
               Inputs:
               ======
               cursor : A cursor object (pointing to the result of a query execution)
               columns : The list of columns to be fetched
               
               Outputs:
               ========
               A list of all columns fetched 
            """
            cols = {}
            for row in rowset:
                keys = row.keys() if not columns else columns
                for k in keys:
                    if(cols.has_key(k)):
                        cols[k].append(row.get(k))
                    else:
                        cols[k] = [row.get(k)]
            if(isinstance(rowset,_cursorbase)):
                rowset.close()
            return cols

        def printTable(self, cursor, columns=[]):
            '''
            Print the rows of the table the cursor is pointing to.
            Inputs:
            =======
            cursor : A cursor object pointing to the result of a query executed.
            columns : (Optional) if only a subset of the columns of the table need to be printed, it can be included in this argument
            
            Output:
            =======
            Prints rows of the table
            It also returns the rows as a list
            '''
            rows = self.fetchRowsFromCursor(cursor)
            separator = '\t | '
            formatter = ''
            printedHeader = False
            filler = ['-' for _k in range(80)]
            
            def printHeader(_cols,separator):
                """
                   Print the header row
                """
                widths = [len(k) for k in _cols]
                max_width = max(widths)+5
                formatter = '{:<'+str(max_width)+'}'
                cnames = [formatter.format(c) for c in columns]
                
                print ''.join(filler)
                print separator.join(cnames)
                print ''.join(filler)
                
                return formatter
            
            def printFooter():
                """
                   Print the footer
                """
                print ''.join(filler)
                print ''
                
                
            if(columns):
                formatter = printHeader(columns,separator)
                printedHeader = True

            for r in rows:
                if (not printedHeader):
                    formatter = printHeader(r.keys(),separator)
                    printedHeader = True
                    
                results = []
                if not columns:
                    results = [r.get(k) for k in r.keys()]
                else:
                    results = [r.get(c) for c in columns]      
                print separator.join([formatter.format(str(k)) for k in results]) 
            
            printFooter()    
            print '\n\n'
            
            return rows
        
        def fetchModelParams(self,row_set):
            """
            Given a rowset from table containing the model, return the model params as a dict
            """
            _model = {}
            for r in row_set:
                for k in r.keys():
                    _model[k] = r.get(k)
                    
            return _model
        
        def printModel(self,rowset):
            """
               Print the model co-efficients from the cursor and return a dict representing the model coefficients.
               Inputs:
               =======
               rowset : A rowset from a table containing the model parameters
            
               Outputs:
               ========
               Prints the model coefficients
            """
            
            separator = '\t | '
            filler = ['-' for _k in range(160)]
            
            def printHeader():
                """
                   Print the header row
                """
                print ''.join(filler)
                print '             Model Parameters'
                print ''.join(filler)
                
            def printFooter():
                """
                   Print footer
                """
                print ''.join(filler)
                print ''
                
            printHeader()
            
            for r in rowset:
                key_widths = [len(k) for k in r.keys()]
                max_width = max(key_widths)+5
                formatter = '{:<'+str(max_width)+'}'
                for key in r.keys():
                    print formatter.format(key),separator,str(r.get(key))

            printFooter()
      
class SupervisedLearning(object):
        ''' Base class for all supervised ML algorithms in MADlib '''
        def __init__(self,conn):
            ''' Initialize the connection to a Database '''
            self.dbconn = conn
            
        def train(self, *args):
            ''' Will be implemented by inherting sub-classes '''
            pass
            
        def predict(self, *args):
            ''' Will be implemented by inheriting sub-classes '''
            pass
      

class LinearRegression(SupervisedLearning):
        ''' 
          Python Wrapper to invoke MADlib's Linear Regression Algorithm 
          http://doc.madlib.net/v0.5/group__grp__linreg.html
        '''
        def __init__(self,conn):
            super(LinearRegression,self).__init__(conn)
      
          
        def train(self, table_name, indep, dep):
            ''' 
              Given train a linear regression model on the specified table 
              for the given set of independent and dependent variables 
              Inputs :
              ========
              table_name : (String) input table name
              indep : (list of strings) the independent variables to be used to build the model on
              dep : (string) the class label
              
              Output :
              ========
              The Model coefficients, r2, p_values and t_stats
              The function also returns the model object.
              
            '''
                 
            indep_org = indep
            
            #Transform the columns if any of them are categorical
            table_name, indep, dep, col_distinct_vals_dict = pivotCategoricalColumns(self.dbconn,table_name, indep, dep)
            #
                      
            self.model = {}
            self.model['indep'] = 'array[{0}]'.format(','.join(indep))
            self.model['indep_org'] = indep_org
            self.model['col_distinct_vals_dict'] = col_distinct_vals_dict
            self.model['dep'] = dep
            cursor = self.dbconn.getCursor()
            
            stmt = '''
                      select ({madlib_schema}.linregr({dep},{indep})).* 
                      from {table_name}
                   '''.format(dep=dep,indep=self.model['indep'], table_name=table_name,madlib_schema=self.dbconn.madlib_schema) 
        
            print '\nstatement :',stmt
            print '\n'
            
            cursor.execute(stmt)
            row_set = self.dbconn.fetchRowsFromCursor(cursor)
            mdl_params = self.dbconn.fetchModelParams(row_set)
            self.dbconn.printModel(row_set)
            
            for param in mdl_params:
                self.model[param] = mdl_params[param]
            
            return self.model
        
        def predict(self, predict_table_name, actual_label_col=''):
            ''' 
              Return predicted values using the trained model. Also return precision, recall & f-measure
              Input:
              ======
              predict_table_name : (String) the name of the table to be used for prediction
              actual_label_col : (String) the name of the actual label column (will be ignored if empty)
              
              Output:
              =======
              A cursor to the row set of the results, including the predicted value as column 'prediction'
              
            '''
            #Transform the columns if any of them are categorical
            predict_table_name, _indep, _dep, _discard = pivotCategoricalColumns(self.dbconn,predict_table_name, 
                                                                       self.model['indep_org'], 
                                                                       actual_label_col,
                                                                       self.model['col_distinct_vals_dict'])
            stmt = '''
                      select *, 
                             {madlib_schema}.array_dot(array{coef}::real[],{indep}) as prediction 
                      from {table_name}
                   '''.format(
                              coef=self.model['coef'],
                              indep=self.model['indep'],
                              table_name=predict_table_name,
                              madlib_schema=self.dbconn.madlib_schema
                             )
            cursor = self.dbconn.getCursor()
            cursor.execute(stmt)
            return cursor
      
class LogisticRegression(SupervisedLearning):
        ''' 
        Python Wrapper to invoke MADlib's Logistic Regression Algorithm 
        http://doc.madlib.net/v0.5/group__grp__logreg.html
        '''
        def __init__(self,conn):
            super(LogisticRegression,self).__init__(conn)
                
        def train(self, table_name, indep, dep, numIter=100, optimizer='irls',precision=0.001):
            ''' 
              Given train a logistic regression model on the specified table 
              for the given set of independent and dependent variables 
              Inputs :
              ========
              table_name : (String) input table name
              indep : (String) column containing independent variables as an array, to be used to build the model on
                                                     OR
                      (list) a list of strings, where each element of the list is a column name of table_name or is a constant number                      
              dep : (string) the class label.
              
              Output :
              ========
              The Model coefficients, r2, p_values and t_stats
              The function also returns the model object.            
            '''
            self.model = {}
            #If indep is a list, then the input is specified as a list of columns in a table.
            #1) First, we will transform any categorical columns in this list.
            #2) We will marshal the values from the columns into an array, that can be passed on to MADlib's logistic regression algorithm.
            if(isinstance(indep,[].__class__)):
                self.model['indep_org'] = indep
                table_name, indep, dep, _ = pivotCategoricalColumns(self.dbconn,table_name, indep, dep)
                #Convert transformed independent columns into an array
                table_name, indep = convertsColsToArray(self.dbconn, table_name, indep, dep)
            else:
                self.model['indep_org'] = indep
               
            self.model['indep'] = indep
            self.model['dep'] = dep
            
            stmt = '''
                      select * 
                      from {madlib_schema}.logregr('{table_name}','{dep}','{indep}',{numIter}, '{optimizer}', {precision}) 
                   '''.format(dep=dep,
                               indep=self.model['indep'],
                               table_name=table_name,
                               numIter=numIter,
                               optimizer=optimizer,
                               precision=precision,
                               madlib_schema=self.dbconn.madlib_schema
                              ) 
            
            print '\nstatement :',stmt
            print '\n' 
            cursor = self.dbconn.getCursor()
            cursor.execute(stmt)
            
            row_set = self.dbconn.fetchRowsFromCursor(cursor)
            mdl_params = self.dbconn.fetchModelParams(row_set)
            self.dbconn.printModel(row_set)
            
            for param in mdl_params:
                self.model[param] = mdl_params[param]
                
            return self.model
        
        def predict(self, predict_table_name,actual_label_col='',threshold=0.5):
            ''' 
              Return predicted values using the trained model. Also return precision, recall & f-measure
              Input:
              ======
              predict_table_name : (String) the name of the table to be used for prediction
              actual_label_col : (String) the name of the actual label column (will be ignored if empty).
              threshold : (float), the probability beyond which the predicted values will be considered +ve (default: 0.5)
                                 
              Output:
              =======
              A cursor to the row set of the results, including the predicted value as column 'prediction'
            '''
            #If the independent columns specified in the training method were a list (instead of a column name of type array)
            #We should transform the independent columns in the predict table as well
            if(isinstance(self.model['indep_org'],[].__class__)):
                predict_table_name, indep, dep, _ = pivotCategoricalColumns(self.dbconn,predict_table_name, self.model['indep_org'], actual_label_col)
                #Convert transformed independent columns into an array
                predict_table_name, indep = convertsColsToArray(self.dbconn, predict_table_name, indep, dep)
                
            stmt = ''' '''
            if(threshold):
                stmt = '''
                          select *,
                                case when (1.0/(1.0 + exp(-1.0*{madlib_schema}.array_dot({indep}, array{coef}::real[])))) > {threshold} 
                                          THEN 1 ELSE 0 
                                end as prediction 
                          from {table_name}
                       '''.format(coef=self.model['coef'],
                                  indep=self.model['indep'],
                                  table_name=predict_table_name,
                                  threshold=threshold,
                                  madlib_schema=self.dbconn.madlib_schema
                                 )
            else:
                #If threshold is not specified, we will return actual predictions
                stmt = '''
                          select *,
                                (1.0/(1.0 + exp(-1.0*{madlib_schema}.array_dot({indep}, array{coef}::real[]))))  as prediction 
                         from {table_name}
                       '''.format(coef=self.model['coef'],
                                  indep=self.model['indep'],
                                  table_name=predict_table_name,
                                  madlib_schema=self.dbconn.madlib_schema
                                 )

            print '\nstatement:',stmt
            print '\n'
            
            cursor = self.dbconn.getCursor()
            cursor.execute(stmt)
            return cursor
      
class SVM(SupervisedLearning):      
        ''' 
          Python Wrapper to invoke MADlib's SVM Algorithm 
          http://doc.madlib.net/v0.5/group__grp__kernmach.html
        '''
        def __init__(self,conn):
            super(SVM,self).__init__(conn)
          
        def train(self, table_name, model_table, isRegression=False, parallel=False, verbose=False, eta=0.1, reg=0.001, kernel_func=None, nu=0.005, slambda=0.05):
            ''' 
              Train an SVM classification model  on the specified table 
              Inputs :
              ========
              table_name : (String) input table name
              model_table : (String) name of the table in which the model will be saved.
              isRegression : (Boolean) is SVM Regression ? (default : False)
              parallel : (Boolean) should the training set be split into different parts and multiple models be trained (one on each part), in parallel ? (default : False)
              verbose : (Boolean) default: False
              eta : (Double) default 0.1
              reg : (Double) default 0.001, required for Linear SVM Classification
              kernel_func : (String) the kernel function to be used for non-linear SVM (ex: Madlib.svm_dot, Madlib.svm_gaussian etc).
              nu : (Double) Required for non-linear SVM classification and SVM regression.
              slambda : (Double) Required for SVM Regression (default: 0.05).
              Output :
              ========
              Model Params
            '''
            cursor = self.dbconn.getCursor()
            if(isRegression==True and kernel_func==None):
                raise Exception ('Parameter kernel_func required for SVM Regression')
            
            #Save Model Params, we will need this during prediction    
            self.model = {}
            self.model['isRegression'] = isRegression
            self.model['model_table'] = model_table
            self.model['parallel'] = parallel
            self.model['verbose'] = verbose
            self.model['eta'] = eta 
            self.model['reg'] = reg
            self.model['kernel_func'] = kernel_func
            self.model['nu'] = nu
            self.model['slambda'] = slambda                    
            
            stmt = ''' '''
            if(isRegression==True):
                stmt =  '''select {madlib_schema}.svm_regression('{table_name}',
                                                        '{model_table}',
                                                        {parallel},
                                                        '{kernel_func}',
                                                        {verbose},
                                                        {eta},
                                                        {nu},
                                                        {slambda}
                                                        );
                        '''.format(
                                   table_name=table_name,
                                   model_table=model_table,
                                   verbose=verbose,
                                   parallel=parallel,
                                   eta=eta,                                 
                                   kernel_func=kernel_func,
                                   nu=nu,
                                   slambda=slambda,
                                   madlib_schema=self.dbconn.madlib_schema
                                  )
                
            #Linear SVM Classification
            elif(kernel_func==None):
                stmt =  '''select {madlib_schema}.lsvm_classification('{table_name}',
                                                             '{model_table}',
                                                             {parallel},
                                                             {verbose},
                                                             {eta},
                                                             {reg}
                                                            );
                        '''.format(
                                   table_name=table_name,
                                   model_table=model_table,
                                   verbose=verbose,
                                   parallel=parallel,
                                   eta=eta,
                                   reg=reg,
                                   madlib_schema=self.dbconn.madlib_schema
                                  )
                
            #SVM Classification
            else:
                stmt =  '''select {madlib_schema}.svm_classification ('{table_name}',
                                                             '{model_table}',
                                                             {parallel},
                                                             '{kernel_func}',
                                                             {verbose},
                                                             {eta},
                                                             {nu}
                                                            );
                        '''.format(
                                   table_name=table_name,
                                   model_table=model_table,
                                   verbose=verbose,
                                   parallel=parallel,
                                   eta=eta,                                 
                                   kernel_func=kernel_func,
                                   nu=nu,
                                   madlib_schema=self.dbconn.madlib_schema
                                  )                                             
               
            
            print '\nstatement :',stmt
            print '\n' 
            
            cursor.execute(stmt)
            
            row_set = self.dbconn.fetchRowsFromCursor(cursor)
            mdl_params = self.dbconn.fetchModelParams(row_set)
            #self.dbconn.printModel(row_set)
            
            for param in mdl_params:
                self.model[param] = mdl_params[param]
                
            return self.model
            
        def predict(self, new_instance):
            ''' 
              Return predicted values using the trained model. 
              Input:
              ======
              new_instance : (String) String representation of the new instance (this would be the independent variable column in a table).
              
              Output:
              =======
              A cursor to the row set of the results, including the predicted value as column 'prediction'
            '''
            
            stmt = ''' '''
            #SVM Regression or non-linear SVM.
            if(self.model['isRegression']==True or self.model['kernel_func'] !=None ):
                algo_name =  'svm_predict_combo' if self.model['parallel'] else 'svm_predict'
                stmt = '''
                          select {madlib_schema}.{algo_name}('{model_table}','{new_instance}'); 
                       '''.format(algo_name=algo_name,
                                  model_table = self.model['model_table'],
                                  new_instance=new_instance,
                                  madlib_schema=self.dbconn.madlib_schema                    
                                 )
            #Linear SVM    
            elif(self.model['kernel_func']==None):
                algo_name =  'lsvm_predict_combo' if self.model['parallel'] else 'lsvm_predict'
                stmt = ''' 
                          select {madlib_schema}.{algo_name}('{model_table}','{new_instance}');
                       '''.format(algo_name=algo_name,
                                  model_table = self.model['model_table'],
                                  new_instance=new_instance,
                                  madlib_schema=self.dbconn.madlib_schema                     
                                 )
                              
            print '\nstatement:',stmt
            print '\n'
            
            cursor = self.dbconn.getCursor()
            cursor.execute(stmt)
            return cursor
        
        def predict_batch(self, predict_table, output_table, id_col, data_col):
            '''
               SVM batch prediction 
               Inputs:
               =======
               predict_table : (string) the table containing the test set to be predicted on.
               output_table : (string) the output table which will contain the results of the prediction
               id_col : (string) the id column in the predict_table
               data_col : (string) the name of the column containing the independent variables
               parallel : 
               
               Outputs:
               ========
               A cursor to the row set containing the results of prediction.               
            '''
            #SVM Regression or non-linear SVM.
            if(self.model['isRegression']==True or self.model['kernel_func'] !=None ):
                algo_name =  'svm_predict_batch'
            #Linear SVM    
            elif(self.model['kernel_func']==None):
                algo_name =  'lsvm_predict_batch'        
                        
            stmt = '''
                      select {madlib_schema}.{algo_name}('{input_table}','{data_col}','{id_col}','{model_table}','{output_table}',{parallel}); 
                   '''.format(algo_name=algo_name,
                              input_table=predict_table,
                              id_col=id_col,
                              data_col=data_col,
                              output_table=output_table,
                              model_table = self.model['model_table'],
                              parallel=self.model['parallel'],
                              madlib_schema=self.dbconn.madlib_schema                    
                             )   
                                                              
            print '\nstatement:',stmt
            print '\n'
            self.dbconn.executeQuery(stmt)
            #Return a cursor to the output table
            stmt = '''select * from {output_table};'''.format(output_table=output_table)
            cursor = self.dbconn.getCursor()
            cursor.execute(stmt)
            return cursor            
                  
class KMeans(object):
        ''' 
        Python Wrapper to invoke MADlib's KMeans Algorithm 
        http://doc.madlib.net/v0.5/group__grp__kmeans.html
        '''    
        def __init__(self,conn):
            self.dbconn = conn 
        
        def generateClusters(
                               self, 
                               table_name, 
                               instances, 
                               numClusters, 
                               initial_centroids=None, 
                               seeding_method='random',
                               fn_dist='{madlib_schema}.squared_dist_norm2',
                               agg_centroid='{madlib_schema}.avg', 
                               max_num_iterations=20, 
                               min_frac_reassigned=0.001
                            ):
            '''
               Invoke MADlib's K-Means algorithm
               Inputs:
               =======
               table_name = (String) name of the table containing the instances to be clusters
               instances = (String) the name of the column containing the instances (of type float8[])
               numClusters = (int) number of clusters
               initial_centroids = (String or float8[][]) the initial list of centroids to be used (either a column name or a float8[][])
               seeding_method = (String) the seeding method to be used 'random' or 'kmeanspp' or 'custom' (default: random)
               fn_dist = (String) name of the SQL function to be used as the distance metric (default: squared_dist_norm2)
               agg_centroid = (String) the SQL function that will used for computing the centroid (default : madlib.avg)
               max_num_iterations = (int) the number of iterations to run the K-Means algorithm for (default : 20)
               min_frac_reassigned = (float) fraction of the points to be re-assigned (default: 0.001)
               
               Outputs:
               ========
               Returns the model, which includes the centroids etc
               
            '''          
            if(seeding_method=='kmeanspp'):          
                #Initialization using K-Means Plus Plus           
                stmt = '''
                             select * from {madlib_schema}.kmeanspp(
                                                         '{table_name}',
                                                         '{instances}',
                                                         {numClusters},
                                                         '{fn_dist}',
                                                         '{agg_centroid}',
                                                         {max_num_iterations},
                                                         {min_frac_reassigned}
                                                         );                                                       
                          '''.format(
                                      table_name=table_name,
                                      instances=instances,                                    
                                      numClusters=numClusters,
                                      fn_dist=fn_dist.format(madlib_schema=self.dbconn.madlib_schema),
                                      agg_centroid=agg_centroid.format(madlib_schema=self.dbconn.madlib_schema),
                                      max_num_iterations=max_num_iterations,
                                      min_frac_reassigned=min_frac_reassigned,
                                      madlib_schema=self.dbconn.madlib_schema
                                     )
            elif(seeding_method=='custom'):
                #Initialization using a set of provided centroids           
                stmt = '''
                             select * from {madlib_schema}.kmeans(
                                                         '{table_name}',
                                                         '{instances}',
                                                         {numClusters},
                                                         '{initial_centroids}',
                                                         '{fn_dist}',
                                                         '{agg_centroid}',
                                                         {max_num_iterations},
                                                         {min_frac_reassigned}
                                                         );                                                       
                          '''.format(
                                      table_name=table_name,
                                      instances=instances,                                    
                                      numClusters=numClusters,
                                      initial_centroids=initial_centroids,
                                      fn_dist=fn_dist.format(madlib_schema=self.dbconn.madlib_schema),
                                      agg_centroid=agg_centroid.format(madlib_schema=self.dbconn.madlib_schema),
                                      max_num_iterations=max_num_iterations,
                                      min_frac_reassigned=min_frac_reassigned,
                                      madlib_schema=self.dbconn.madlib_schema
                                     )          
            else:
                #Random initialization              
                stmt = '''
                          select * from {madlib_schema}.kmeans_random(
                                                             '{table_name}',
                                                             '{instances}',
                                                             {numClusters},
                                                             '{fn_dist}',
                                                             '{agg_centroid}',
                                                             {max_num_iterations},
                                                             {min_frac_reassigned}
                                                             );                                                       
                       '''.format(
                                  table_name=table_name,
                                  instances=instances,
                                  numClusters=numClusters,
                                  fn_dist=fn_dist.format(madlib_schema=self.dbconn.madlib_schema),
                                  agg_centroid=agg_centroid.format(madlib_schema=self.dbconn.madlib_schema),
                                  max_num_iterations=max_num_iterations,
                                  min_frac_reassigned=min_frac_reassigned,
                                  madlib_schema=self.dbconn.madlib_schema
                                 )
                                 
            cursor = self.dbconn.getCursor()
            self.model = {}
            
            print '\nstatement :',stmt
            print '\n' 
            
            cursor.execute(stmt)
            
            row_set = self.dbconn.fetchRowsFromCursor(cursor)
            mdl_params = self.dbconn.fetchModelParams(row_set)
            self.dbconn.printModel(row_set)
            
            for param in mdl_params:
                self.model[param] = mdl_params[param]
                              
            return self.model  
      
class PLDA(object):
        ''' 
        Python Wrapper to invoke MADlib's PLDA Algorithm 
        http://doc.madlib.net/v0.5/group__grp__plda.html
        '''    
        def __init__(self,conn):
            self.dbconn = conn 
        
        def infer(self, dataTable, dictTable, modelTable, outputTable, numTopics, numIter=30, alpha=0.5, eta=0.5):
            '''
               Invoke MADlib's PLDA algorithm
               Inputs:
               =======
               dataTable = (String) the table containing the documents on which the LDA model has to be built
               dictTable = (String) table containing a dictionary of all tokens in the documents
               modelTable = (String) table to store the LDA model params in.
               outputTable = (String) table to store the results of the LDA model
               numTopics = (int) number of topics in the document.
               numIter = (int) number of iterations of the Gibbs sampler to run (default : 30)             
               alpha = (float) the dirichlet prior Alpha (default: 0.5)
               eta = (float) eta (default:0.5)
               
               Outputs:
               ========
               Returns a row set of the form || id | topics | topics_d || from the outputTable 
            ''' 
            self.model = {}
            self.model['dictTable']=dictTable
            self.model['modelTable']=modelTable
            self.model['alpha']=alpha
            self.model['eta']=eta
            self.model['numTopics']=numTopics
                       
            stmt = '''
                      select {madlib_schema}.plda_run('{dataTable}', '{dictTable}', '{modelTable}', '{outputTable}', 
                             {numIter}, {numTopics}, {alpha}, {eta});  
                   '''.format(
                              dataTable=dataTable,
                              dictTable=dictTable,
                              modelTable=modelTable,
                              outputTable=outputTable,
                              numIter=numIter,
                              numTopics=numTopics,
                              alpha=alpha,
                              eta=eta,
                              madlib_schema=self.dbconn.madlib_schema
                             ) 
               
            self.dbconn.executeQuery(stmt)
            stmt = ''' select id, (topics).topics, (topics).topic_d
                       from {outputTable};
                   '''.format (
                                outputTable=outputTable
                              )     
            cursor = self.dbconn.getCursor()
            cursor.execute(stmt)
            result_set = [row for row in cursor]   
            cursor.close()
            return result_set
        
        def label_test_documents(self, testTable, outputTable, dictTable=None, modelTable=None, numTopics=None, alpha=None, eta=None):
            '''
               Invoke MADlib's PLDA algorithm
               Inputs:
               =======
               testTable = (String) the table containing the documents on which the LDA model has to predict topics
               dictTable = (String) table containing a dictionary of all tokens in the documents
               modelTable = (String) table to store the LDA model params in.
               outputTable = (String) table to store the results of the LDA model
               numTopics = (int) number of topics in the document (default : the value used in building the LDA model)       
               alpha = (float) the dirichlet prior Alpha (default: value used in building the LDA model - in the infer() method)
               eta = (float) eta (default: value used in building the LDA model - in the infer() method)
               
               Outputs:
               ========
               Returns a row set of the form || id | contents | topics || from the outputTable 
            ''' 
                      
            dictTable = self.model['dictTable'] if not dictTable else dictTable
            modelTable = self.model['modelTable'] if not modelTable else modelTable
            numTopics = self.model['numTopics'] if not numTopics else numTopics
            alpha = self.model['alpha'] if not alpha else alpha
            eta = self.model['eta'] if not eta else eta          
            
            stmt = '''
                      select {madlib_schema}.plda_label_test_documents('{testTable}', '{outputTable}', '{modelTable}', '{dictTable}',
                               {numTopics}, {alpha}, {eta});
                   '''.format(
                              testTable=testTable,
                              outputTable=outputTable,
                              modelTable=modelTable,
                              dictTable=dictTable,
                              numTopics=numTopics,
                              alpha=alpha,
                              eta=eta,
                              madlib_schema=self.dbconn.madlib_schema
                             )
            
            self.dbconn.executeQuery(stmt)
            
            stmt = '''
                      select id, contents, topics from {outputTable};
                   '''.format(outputTable=outputTable)
                         
            cursor = self.dbconn.getCursor()   
            cursor.execute(stmt)
            result_set = [row for row in cursor]
            cursor.close()
            return result_set
