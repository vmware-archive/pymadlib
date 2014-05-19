'''
    4 Jan 2013, vatsan.cs@utexas.edu>
    1) Demonstrate how to use PyMADlib by invoking the linear regression, logistic regression, SVM, KMeans and PLDA algorithms on a sample table.
    2) Demonstrate Matplotlib's visualization of the actual vs predicted results from the model. This requires Matplotlib to be installed.
'''

from pymadlib import DBConnect, LinearRegression, LogisticRegression, SVM, KMeans, PLDA
import os
COLOR_PURPLE = '#CC33FF'
COLOR_VIOLET = '#6600FF'
COLOR_LIGHT_BLUE = '#0099CC'
COLOR_BLUE = '#0000FF'
COLOR_LIGHT_RED = '#FF0099'
COLOR_SIENNA = '#F87431'

def __isTableExists__(tbl_name,conn):
    '''
       Returns true if table tbl_name exists, using the connection conn:  
       Inputs:
       =======
       conn : DBConnect object
       tbl_name : (string) A name of the table whose presence has to be checked
       
       Outputs:
       ========
       True is the input table exists in the database, False otherwise     
    '''
    stmt = ''' select exists(select relname 
                             from pg_class 
                             where relname= '{tbl_name}' and relkind='r'
                            ) as is_exists ;
           '''.format(tbl_name=tbl_name)

    cursor = conn.getCursor()
    cursor.execute(stmt)
    tableExists=False
    for row in cursor:
        tableExists = row['is_exists'] 
    cursor.close()

    return tableExists

def loadDemoTables():
    '''
       Load the tables used in the Demo, if they don't exist. 
    '''
    dbconn = DBConnect()
    conn_dict = dbconn.getConnectionString()
    
    load_tbl_stmt = '''psql -h {hostname} -p {port}  -U {username}  -d {database} -f '''
    load_tbl_stmt = load_tbl_stmt.format( username=conn_dict['username'],
                                          hostname=conn_dict['hostname'],
                                          database=conn_dict['database'],
                                          port=conn_dict['port']
                                        )
    
    this_dir = os.path.dirname(os.path.abspath(__file__))

    for fl in os.listdir(os.path.join(this_dir,'data/')):
        full_path = os.path.join(os.path.join(this_dir,'data'),fl)
        if(fl.endswith('.sql')):
            #If the demo table does not exists in the database already, create it using the provided sql files
            if(not __isTableExists__(fl[:-len('.sql')],dbconn)):   
                print '\n\n cmd:',load_tbl_stmt+' '+full_path
                cmd = load_tbl_stmt+ ' '+full_path
                os.system(cmd)         
                
    print 'Loading demo tables complete'

def linearRegressionDemo(conn):
    '''
       Demonstrate Linear Regression
    '''
    lreg = LinearRegression(conn)
    lreg.train('public.wine_training_set',['1','alcohol','proline','hue','color_intensity','flavanoids'],'quality')
    cursor = lreg.predict('public.wine_test_set','quality')
    rowset = conn.printTable(cursor,['id','quality','prediction'])
    cols = conn.fetchColumns(rowset,['quality','prediction'])

    actual = cols['quality']
    predicted = cols['prediction'] 
    scatterPlot(actual,predicted, 'wine_test_set')        

        
    # 1 b) Linear Regression with categorical variables 
    # We'll use the auto_mpg dataset from UCI : http://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.names
    # make, fuel_type, fuel_system are all categorical variables, rest are real.
    lreg.train('public.auto_mpg_train',['1','height','width','length','highway_mpg','engine_size','make','fuel_type','fuel_system'],'price')
    
    cursor = lreg.predict('public.auto_mpg_test','price')
    rowset = conn.printTable(cursor,['id','price','prediction'])
    cols = conn.fetchColumns(rowset,['price','prediction'])
    
    print '\n\n Linear Regression Predictions (with categorical variables) :'    
    actual = cols['price']
    predicted = cols['prediction'] 
    scatterPlot(actual,predicted, 'auto_mpg_test')    
    
def logisticRegDemo(conn):
    '''
       Demonstrate Logistic Regression
    '''    
    
    # a) Logistic Regression with numeric attributes
    log_reg = LogisticRegression(conn)
    log_reg.train('public.wine_bool_training_set','indep','quality_label')
    cursor = log_reg.predict('public.wine_bool_test_set','',0.5)
    conn.printTable(cursor,['id','quality_label','prediction'])
            
    # b) ROC curve for Logistic Regression using numeric features alone, 
    # Note: Here threshold is set to None, to be able to plot ROC curve    
    cursor = log_reg.predict('wine_bool_test_set','',None)
    cols = conn.fetchColumns(cursor,['quality_label','prediction'])
    actual = cols['quality_label']
    predicted = cols['prediction']
    #show ROC curve
    ROCPlot('ROC curve Logistic Reg. on Continuous Features ',['Logistic Regression'],actual,predicted)
    
    # c) Logistic Regression with mixture of numeric and categorical columns     
    log_reg.train('public.auto_mpg_bool_train',['1','height','width','length','highway_mpg','engine_size','make','fuel_type','fuel_system'],'is_expensive')
    cursor = log_reg.predict('auto_mpg_bool_test','is_expensive',None)
    cols = conn.fetchColumns(cursor,['is_expensive','prediction'])
    actual = cols['is_expensive']
    predicted = cols['prediction']  
    ROCPlot('ROC curve Logistic Reg. including categorical data',['Logistic Regression'],actual,predicted)  
    
def __svmDemoCleanup__(conn):
    '''
       Clean-up any tables that were created
    '''        
    conn.executeQuery('drop table if exists svm_model cascade ;')
    conn.executeQuery('drop table if exists svm_model_param cascade ;')   
    
def svmDemo(conn):
    '''
       Demonstrate SVM Classification and Regression
    '''        
    __svmDemoCleanup__(conn) 
    # a) SVM Regression
    svm_reg = SVM(conn)
    kernal_func = '{madlib_schema}.svm_dot'.format(madlib_schema=conn.madlib_schema)
    svm_reg.train('public.wine_bool_svm_train_set', 
                  'svm_model', 
                  True, 
                  False, 
                  False, 
                  0.1, 
                  0.001, 
                  kernal_func, 
                  0.005, 
                  0.05
                  )
    svm_reg.predict('{1,3,1.63,9.9,0.64,1.39}')
    __svmDemoCleanup__(conn)     
    
    # b) Linear SVM Classification
    svm_reg.train('public.wine_bool_svm_train_set', 'svm_model',False)
    svm_reg.predict('{1,3,1.63,9.9,0.64,1.39}')    
    __svmDemoCleanup__(conn)    
        
    # c) Non-linear SVM Classification
    svm_reg.train('public.wine_bool_svm_train_set', 
                  'svm_model', 
                  False, 
                  False, 
                  False, 
                  0.1, 
                  0.001,
                  kernal_func, 
                  0.005, 
                  0.05
                  )    
    svm_reg.predict('{1,3,1.63,9.9,0.64,1.39}')    
    __svmDemoCleanup__(conn)  
    
    # d) SVM batch prediction (with non linear model)
    conn.executeQuery('drop table if exists gp_pymdlib_svm_prediction cascade;')    
    svm_reg.train('public.wine_bool_svm_train_set', 
                  'svm_model', 
                  False, 
                  False, 
                  False, 
                  0.1, 
                  0.001,
                  kernal_func, 
                  0.005, 
                  0.05
                  )    
    cursor = svm_reg.predict_batch('wine_bool_svm_train_set',
                          'gp_pymdlib_svm_prediction',
                          'id',
                          'ind'
                         )  
    cursor.close()                                       
    cursor = conn.getCursor()
    cursor.execute(''' select t1.id, 
                              t1.label as actual_label, 
                              case when t2.prediction > 0 then 1 else -1 end as predicted_label
                       from wine_bool_svm_train_set t1, gp_pymdlib_svm_prediction t2
                       where t1.id = t2.id;
                   '''
                  )

    print 'SVM Batch prediction results'
    conn.printTable(cursor)
    __svmDemoCleanup__(conn) 
    
def kmeansDemo(conn):
    '''
       Demonstrate K-Means
    '''          
    #a) K-Means with random initialization of centroids
    kmeans = KMeans(conn)
    print '\n\nKMeans with random cluster initialization'
    mdl = kmeans.generateClusters('public.wine_bool_training_set','indep',3)   
    centroids_random_kmeans = str(mdl.get('centroids'))
    centroids_random_kmeans = centroids_random_kmeans.replace('[','{').replace(']','}')
    
    #b) KMeans Plus Plus 
    print '\n\nKMeans Plus Plus '
    mdl = kmeans.generateClusters('public.wine_bool_training_set','indep',3,'kmeanspp') 
    
    #Show a visualization of the clusters.
    #1) Compute the strength of the relationship between all pairs of points and capture this in a graph
    cursor = conn.getCursor()   
    cursor.execute(
                   '''
                      select t1.id as node1, 
                             t2.id as node2, 
                             {madlib_schema}.squared_dist_norm2(t1.indep, t2.indep) as dist 
                      from {table_name} t1, {table_name} t2;  
                   '''.format(table_name='wine_bool_training_set',madlib_schema=conn.madlib_schema)
                  )
    
    result_set = [row for row in cursor]
    cursor.close()
    dist_dict = {}    
    edge_set = set()
    for r in result_set:
        node1 = r.get('node1')
        node2 = r.get('node2')
        ed = [node1,node2]
        ed.sort()
        ed = str(ed)
        dist = r.get('dist')        
        #We are building undirected graph, so don't add back edges.
        if(ed not in edge_set):
            edge_set.add(ed)
            if(dist_dict.has_key(node1)):
                dist_dict[node1][node2]=dist
            else:
                dist_dict[node1] = {node2:dist}
            
        
    #2) Only retain those edges in the 90 percentile, prune the remaining (sparse graph).
    dist_arr = list(set([r.get('dist') for r in result_set]))
    dist_arr.sort()    
    #3) Display the resulting graph where nodes are colored by their cluster number. 
    # Also, nodes in the same cluster should be physically close to each other.
    #Get cluster allocation for deciding colors
    cluster_membership_query = '''
                                    select id as instance_id,
                                           ({madlib_schema}.closest_column(
                                                                  '{centroids}'::double precision[],
                                                                  indep, 
                                                                  '{madlib_schema}.squared_dist_norm2'
                                                                 )
                                           ).column_id as cluster_num
                                    from {table_name};
                               '''.format(
                                           centroids=centroids_random_kmeans,
                                           table_name='wine_bool_training_set',
                                           madlib_schema=conn.madlib_schema
                                         )

    cluster_memberships = {}                           
    cursor = conn.getCursor()
    cursor.execute(cluster_membership_query)
    for r in cursor:
        cluster_memberships[r.get('instance_id')] = r.get('cluster_num')
    cursor.close()    
    #Visualize
    kmeansViz(dist_dict,dist_arr,cluster_memberships)
    
def kmeansViz(clusterGraph,dist_sorted,clusterMemberships,density_factor=0.25):
    '''
       Use networkx to visualize result of k-means
       Inputs:
       =======
       clusterGraph : {a:{b:weight}} - A dict representing the graph, with weight being strength of 
                      relationship between nodes a and b
       dist_sorted :  A sorted list of distances (or strength of the relationships) in descending order 
                      (higher the index, lower the strength)               
       
       clusterMemberships : {id:clusterNumber} - A dict representing the cluster allocation of each 
                            instance in the input
       density_factor: (float) what fraction of the nc2 edges to consider in the final graph 
                       (based on edge strength). Default : 0.25
       Outputs:
       ========
       A visualization of the K-Means clustering using networkx. Edge weights between nodes are the 
       strength of the relationship between the nodes (based on distance metric) and colors indicate
       cluster membership.
    '''
    
    try:
        import networkx as nx, matplotlib.pyplot as plt
    except ImportError:
        print 'NetworkX and/or Matplotlib/Pylab does not exist, skipping networkViz Demo'    
        return

    edges = []
    
    for origNode in clusterGraph.keys():
        for destNode in clusterGraph[origNode].keys():
            dst = clusterGraph[origNode][destNode]
            #Only consider the top-25% edges by strength of the relationship
            if(dst in dist_sorted[:int(density_factor*len(dist_sorted))]):
                strength = 1.0 - (clusterGraph[origNode][destNode]/max(dist_sorted))            
                edges.append((origNode,destNode,{'weight':strength,'color':'red'}))
    
    G=nx.Graph()
    #Add edges
    G.add_edges_from(edges)
    
    nodes_colors = []
    for n in G.nodes():
        cNum = clusterMemberships[n]    
        if(cNum==0):
            nodes_colors.append(COLOR_PURPLE)
        elif(cNum==1):
            nodes_colors.append(COLOR_LIGHT_BLUE)       
        else:
            nodes_colors.append(COLOR_LIGHT_RED)
    
    plt.figure(figsize=(6,6))  
    #Use spring layout for positioning the nodes of the graph
    nodes_pos = nx.spring_layout(G)
    nx.draw_networkx_edges(G,nodes_pos,alpha=0.4,edge_color='k', width=2) 
    nx.draw_networkx_nodes(G,nodes_pos,nodelist=G.nodes(),node_size=80,node_color=nodes_colors) 
    plt.title('K-Means Cluster Visualization for {num_clusters} clusters'.format(num_clusters=3),weight='bold')
    plt.xlim(-0.05,1.05)
    plt.ylim(-0.05,1.05)
    plt.axis('off')
    plt.show()                           
        
def pldaDemo(conn):        
    '''
       Demonstrate LDA
    '''    
    # a) LDA infer
    conn.executeQuery('drop table if exists debate_lda_result_obama cascade ;')
    conn.executeQuery('drop table if exists debate_lda_model_obama cascade ;')      
    lda = PLDA(conn)
    rset = lda.infer('debate_obama_tokens_temp','debate_lda_dict','debate_lda_model_obama','debate_lda_result_obama',30,4,0.5,0.5)
    rowCount=0
    for row in rset:
        if(rowCount==0):
            print '\t| '.join(row.keys())
            print '-------------------------------------------------------------------------------'                  
        rowCount+=1
        print '\t| '.join([str(row[key]) for key in row.keys()])
                
    # b) LDA label test documents
    conn.executeQuery('drop table if exists debate_lda_result_obama_test cascade ;')     
    rset = lda.label_test_documents('debate_obama_tokens_temp','debate_lda_result_obama_test') 
    rowCount=0
    for row in rset:
        if(rowCount==0):
            print '\t| '.join(row.keys())
            print '-------------------------------------------------------------------------------'                  
        rowCount+=1
        print '\t| '.join([str(row[key]) for key in row.keys()])

                      
def scatterPlot(actual,predicted,dataset_name=''):
    '''
        Demonstrate Scatter Plot generation of the actual labels vs predicted labels
        This requires Matplotlib installed on the local system.
        Inputs:
        =======
        actual: (list) a list of actual values for a label column
        predicted: (list) a list of predicted values for a label column
        
        Outputs:
        ========
        Displays the scatter plot in a window
    '''

    try:
        import matplotlib, pylab
        from pylab import poly1d, polyfit, plot
    except ImportError:
        print 'Matplotlib/Pylab does not exist, skipping Scatter Plot Demo'
        return
            
    if(not actual or not predicted) :
        return
    #Line of best fit
    fit = polyfit(actual,predicted,1)
    fit_func = poly1d(fit)
    #
    matplotlib.pyplot.scatter(actual,predicted, facecolors='none', edgecolors=COLOR_LIGHT_RED, s=50, linewidth=2)
    plot(actual,fit_func(actual),'k')
    pylab.title('Scatter plot of Actual Vs Predicted values for dataset : {dataset_name}'.format(dataset_name=dataset_name), weight='bold')
    pylab.xlabel('Actual', weight='bold')
    pylab.ylabel('Predicted', weight='bold')
    pylab.show()

def ROCPlot(title, labels=None,*args):
    '''
       If the PyROC (https://github.com/marcelcaraciolo/PyROC) 
       module is installed, display the ROC curve for SVM/Logistic Regression classifiers.
       Inputs:
       =======
       labels : Labels for the legend
       args: Variable length arguments of the form : actual_1[], predicted_1[], actual_2[], predicted_2[], ....
    '''
    try:
        from pyroc import random_mixture_model, ROCData, plot_multiple_roc
        import pylab
    except ImportError:
        try:
            from pyroc import random_mixture_model, ROCData, plot_multiple_roc
        except ImportError:
            print 'PyROC does not exist, skipping ROC demo. Install PyROC from : https://github.com/marcelcaraciolo/PyROC '
            return    
    if(len(args)==0):
        x = random_mixture_model()
        r1 = ROCData(x)
        y = random_mixture_model()
        r2 = ROCData(y)
        lista = [r1,r2]
        labels = ['Algorithm-1','Algorithm-2']
    else:
        lista = []
        for i in range(0,len(args),2):
            x1 = args[i]
            y1 = args[i+1]
            x1y1 = ((x1[k],y1[k]) for k in range(len(x1)))
            r1 = ROCData(x1y1)
            auc = '%.2f'%r1.auc()
            if(labels):
                labels[i/2] = labels[i/2]+ ', AUC: {0} '.format(auc)
            lista.append(r1)            
    plot_multiple_roc(lista,title,include_baseline=True,labels=labels)    
    pylab.close()
    
def networkVizDemo():
    '''
       Visualize the results of KMeans clustering using NetworkX http://networkx.github.com/
       This example is taken from : http://networkx.github.com/documentation/latest/examples/drawing/random_geometric_graph.html
       and is purely meant to show networkx's visualization.
    '''
    try:
        import networkx as nx, matplotlib.pyplot as plt
    except ImportError:
        print 'NetworkX and/or Matplotlib/Pylab does not exist, skipping networkViz Demo'    
        return

    G=nx.random_geometric_graph(200,0.125)
    # position is stored as node attribute data for random_geometric_graph
    pos=nx.get_node_attributes(G,'pos')

    # find node near center (0.5,0.5)
    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d

    # color by path length from node near center
    p=nx.single_source_shortest_path_length(G,ncenter)

    plt.figure(figsize=(8,8))
    nx.draw_networkx_edges(G,pos,nodelist=[ncenter],alpha=0.4)
    nx.draw_networkx_nodes(G,pos,nodelist=p.keys(),
                           node_size=80,
                           node_color=p.values(),
                           cmap=plt.get_cmap('Reds_r'))
    
    plt.xlim(-0.05,1.05)
    plt.ylim(-0.05,1.05)
    plt.title('Network-X Random Graph Visualization', weight='bold')
    plt.axis('off')
    plt.show()
   
def conn_test():
    ''' 
        Test the connection by displaying rows from a table 
    '''
    conn = DBConnect()
    cursor = conn.getCursor(True)
    cursor.executeQuery('select * from wine_training_set')
    conn.printTable(cursor)        

def pyMADlibDemo():
    ''' 
        Demonstrate building Linear Regression and Logistic Regression Models using MADlib 
    '''
    conn = DBConnect(madlib_schema='madlib_v05')

    #1) Linear Regression
    linearRegressionDemo(conn)    
    
    #2) Logistic Regression 
    logisticRegDemo(conn)        
    
    #3) SVM Regression
    svmDemo(conn)
    
    #4) KMeans
    kmeansDemo(conn)
    
    #5) PLDA
    pldaDemo(conn)

def runDemos():
    '''
       Run the demos
    '''
    loadDemoTables()
    pyMADlibDemo() 
    networkVizDemo()
    
if(__name__=='__main__'):
    runDemos()
