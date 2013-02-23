'''
    4 Jan 2013, vatsan.cs@utexas.edu>
    Utility functions for PyMADlib. Currently this supports dummy coding of categorical columns (Pivoting).
'''
import pickle 

default_schema = 'public'
default_prefix = 'gp_pymdlib_'
default_prefix_arr = 'gp_pymdlib_arr_'
MAX_DISTINCT_VALS = 128

#Easy way of encoding strings without worrying about escaping quotes etc
GP_STRING_IDENTIFIER = '$GP_STR_IDENTIFIER${string_to_encode}$GP_STR_IDENTIFIER$'

PARALLEL_INSERT_FUNC = '''
                          DROP FUNCTION IF EXISTS gp_pivotify({table_name}, bytea, bytea, bytea, text);
                          CREATE FUNCTION gp_pivotify(rec_row {table_name}, cols_bin bytea, col_types_dict_bin bytea, col_distinct_vals_dict_bin bytea, label_col text)
                          RETURNS {output_table} AS
                          $$
                             import pickle
                             cols = pickle.loads(cols_bin)
                             col_types_dict = pickle.loads(col_types_dict_bin)
                             col_distinct_vals_dict = pickle.loads(col_distinct_vals_dict_bin) 
                             
                             insert_rec = []
                             #Insert ID column if it exists
                             if(col_types_dict.has_key('id')):
                                 insert_rec.append(str(rec_row.get('id')))
                                
                             #Insert values for the independent variables    
                             for c in cols:
                                 if(col_distinct_vals_dict.has_key(c)):
                                     #A list of zeros will be used to initialized the binarized categorical column
                                     #binarized_vals[i] will be 1, if 'i' is the value for the categorical column in the current row
                                     num_dummy_variables = len(col_distinct_vals_dict[c].keys())
                                     #In Dummy Coding, if a variable has K possible values, we add K-1 dummy variables (binary) 
                                     #to represent the original variable
                                     if(num_dummy_variables > 1):
                                         num_dummy_variables = num_dummy_variables - 1
                                         
                                     binarized_vals = [0 for k in range(num_dummy_variables)]
                                     #Set the index of the categorical variable's value to 1, rest will be zeros
                                     cat_val = rec_row.get(c)
                                     if(col_distinct_vals_dict[c].has_key(cat_val) and col_distinct_vals_dict[c][cat_val] < num_dummy_variables):
                                         binarized_vals[col_distinct_vals_dict[c][cat_val]]=1
                                     insert_rec.extend(binarized_vals)
                                 else:
                                     insert_rec.append(rec_row.get(c))
                                     
                             #Insert label value if it was passed in the input
                             if(label_col):
                                 insert_rec.append(rec_row.get(label_col))
                             #Return the row
                             return insert_rec
                          $$ LANGUAGE PLPYTHONU;
                       '''
                       
PARALLEL_INSERT_QUERY = '''
                           insert into {output_table_name}
                           (
                                select (binarized_table_type).* from
                                (
                                       select gp_pivotify({table_name}.*,
                                                          {cols}::bytea,
                                                          {col_types_dict}::bytea,
                                                          {col_distinct_vals_dict}::bytea,
                                                          '{label_col}'
                                                         ) as binarized_table_type
                                       from {table_name}
                                ) q1
                           );
                        '''
def isNumeric(num):
    ''' 
        Returns True if the string representation of num is numeric 
        Inputs:
        =======
        num : A string representation of a number.
        Outputs:
        ========
        True if num is numeric, False otherwise
    '''
    try:
        float(num)
    except ValueError, typError:
        print 'valueError :',ValueError
        print 'typeError :',typError
        return False
    else:
        return True  
    
def __binarizeInParallel__(conn, table_name, output_table, cols, col_types_dict, col_distinct_vals_dict, label):
    '''
       Transform the categorical columns into a collection of binary values columns and insert rows
       into this column in parallel using PL/Python function
       Inputs:
       =======
       conn : A DBConnect object
       table_name : (string) Name of input table
       output_table : (string) Name of output table
       cols: (list) list of independent feature column names
       col_types_dict : (dict) a dict of column names and types
       col_distinct_vals_dict : (dict) a dict of column name, and the set of all distinct values in the column
       label : (string) label column name. If empty, it will be ignored.
       
       Outputs:
       =======
       A new table is created with the rows of the original table transformed
    '''
    pinsert_func =  PARALLEL_INSERT_FUNC.format(table_name=table_name, output_table=output_table)
    conn.executeQuery(pinsert_func)
    pinsert_stmt = PARALLEL_INSERT_QUERY.format(output_table_name=output_table,
                                                table_name=table_name,
                                                cols = GP_STRING_IDENTIFIER.format(string_to_encode=pickle.dumps(cols)),
                                                col_types_dict = GP_STRING_IDENTIFIER.format(string_to_encode=pickle.dumps(col_types_dict)),
                                                col_distinct_vals_dict = GP_STRING_IDENTIFIER.format(string_to_encode=pickle.dumps(col_distinct_vals_dict)),
                                                label_col=label
                                       )
    conn.executeQuery(pinsert_stmt)

def __getColTypesDict__(conn,tbl_schema,tbl_nm):
    '''
       Return a dict containing column names and their type, by querying the information schema
       Inputs:
       =======
       conn : A DBConnect object
       tbl_schema : (string) The schema of the table 
       tbl_nm : (string) The name of the table whose columns we need to query
       
       Outputs:
       ========
       col_types_dict : A dict of col_name and types
    '''
    col_types_stmt = ''' 
                        select column_name, data_type
                        from information_schema.columns 
                        where table_schema = '{table_schema}' and table_name = '{table_name}';
                     '''.format(table_schema=tbl_schema, table_name = tbl_nm)
                       
    cursor = conn.getCursor()
    cursor.execute(col_types_stmt)
    col_types_dict = {}
    for row in cursor:
        col_types_dict[row.get('column_name')] = row.get('data_type')
    cursor.close()
    return col_types_dict

def __getColDistinctValsDict__(conn, cols, col_types_dict, table_name):
    '''
       Return a dict of column name, and the set of all distinct values in the column
       Inputs:
       =======
       conn : A DBConnect object
       cols :  (list) list of independent feature column names
       col_types_dict : (dict) a dict of column names and types
       table_name : (string) name of the input table
       
       Outputs:
       ========
       col_distinct_vals_dict : (dict) a dict of column name, and the set of all distinct values in the column
    '''
    distinct_vals_stmt = '''
                            select distinct {col_name}
                            from  {table_name}
                            order by {col_name};
                         '''
    #If any of the columns is of type character or varchar or text, and the number of distinct values in these columns < N (for now let's set it at 32)
    #Then 'binarize' this column's values and create a new table for this column
    col_distinct_vals_dict = {}
    for col in cols:        
        if(col_types_dict[col] in ['char','character varying', 'text']):
            #Find distinct values of the column
            cursor = conn.getCursor()    
            stmt = distinct_vals_stmt.format(col_name=col,table_name=table_name)   
            cursor.execute(stmt)
            distinct_vals = [row.get(col) for row in cursor]
            cursor.close()
            distinct_vals_dict = {}
            for i in range(len(distinct_vals)):
                distinct_vals_dict[distinct_vals[i]]=i
            
            #If the number of distinct values of a categorical column is reasonable, then add it to a mapper    
            if(len(distinct_vals) < MAX_DISTINCT_VALS):
                col_distinct_vals_dict[col] = distinct_vals_dict
                  
    return col_distinct_vals_dict

def __getColNamesAndTypesList__(cols,col_types_dict, col_distinct_vals_dict):
    '''
       Return a list of column names and types, where any categorical column in the original table have
       been 'binarized'. Dummy coding is used to convert categorical columns into dummy variables.
       Refer: http://en.wikipedia.org/wiki/Categorical_variable#Dummy_coding
       
       Inputs:
       =======
       cols :  (list) list of independent feature column names
       col_types_dict : (dict) a dict of column names and types
       col_distinct_vals_dict: (dict) a dict of column name, and the set of all distinct values in the column
       
       Outputs:
       ========
       col_names_and_types_lst : (list) a list of column names and types, where any categorical 
                                 column in the original table have
    '''
    col_names_and_types_lst = []
    for col in cols:
        if(col_distinct_vals_dict.has_key(col)):
            dist_vals = col_distinct_vals_dict[col].keys()
            dist_vals.sort()
            #In Dummy Coding, if a variable has K possible values, we add K-1 dummy variables (binary) to represent the original variable
            if(len(dist_vals) > 1):
                dist_vals = dist_vals[:-1]
            
            for valIndx in range(len(dist_vals)):
                col_names_and_types_lst.append(['{column}_val_{indx}'.format(column=col,indx=valIndx),'integer'])
                
        else:
            col_names_and_types_lst.append([col, col_types_dict[col]])
            
    return col_names_and_types_lst

def __createPivotTable__(conn, output_table, col_types_dict, col_names_and_types_lst, label):
    '''
       Create a Pivot table, where every categorical column in the original table
       has been expanded into n columns, where n is the number of distinct values in the column
       Inputs:
       =======
       conn : DBConnect object
       output_table : (string) name of the pivot table (output)
       col_types_dict : (dict) a dict of column names and types
       col_names_and_types_lst : (list) a list of column names and types, where any categorical 
                                 column in the original table have
       label : (string) name of the label column (if it is an empty string, it will be ignored)
       
       Outputs:
       ========
       A Pivot table is created.
    '''
    cnames_and_types = ', '.join(['  '.join(pair) for pair in col_names_and_types_lst])    
    stmt = ''' '''
    data_dict = {}
    data_dict['output_table'] = output_table
    data_dict['col_names_and_types'] = cnames_and_types
    if(col_types_dict.has_key('id') and label):
        stmt = '''
                 drop table if exists {output_table} cascade;
                 create table {output_table}
                 ({id_col}   {id_col_type},
                  {col_names_and_types},
                  {label_col_name}  {label_col_type}
                 );
               '''
        data_dict['id_col'] = 'id'
        data_dict['id_col_type'] = col_types_dict['id']
        data_dict['label_col_name'] = label
        data_dict['label_col_type'] = col_types_dict[label]
    elif(col_types_dict.has_key('id')):
        #ID column exists, but there is no label column specified
        stmt = '''
                 drop table if exists {output_table} cascade;
                 create table {output_table}
                 ({id_col}   {id_col_type},
                  {col_names_and_types}
                 );
               '''
        data_dict['id_col'] = 'id'
        data_dict['id_col_type'] = col_types_dict['id']
    else:
        #Neither ID column nor label column exists (i.e there only are features in the table)
        stmt = '''
                 drop table if exists {output_table} cascade;
                 create table {output_table}
                 (
                  {col_names_and_types}
                 );
               '''
    stmt = stmt.format(**data_dict)
    conn.executeQuery(stmt)
    
    
def pivotCategoricalColumns(conn,table_name,cols,label='',col_distinct_vals_dict=None):
    '''
       Take a table_name and a set of columns (some of which may be categorical 
       and return a new table, where the categorical columns have been pivoted.
       This method uses the "Dummy Coding" approach: 
       http://en.wikipedia.org/wiki/Categorical_variable#Dummy_coding
       
       Inputs:
       =======
       conn : A psycopg2 connection to a database.
       table_name : (String) the name of the input table
       cols : (List) a list of columns (some of which may be categorical) to be used as independent variable
       label : (String) the dependent column
       col_distinct_vals_dict : (dict) A dict of distinct values for each column. If not specified, this will be 
                                computed from the training data. 

       Outputs:
       ========
       output_table : (String) a new table containing the categorical columns
                      which have been pivoted
       output_indep_cols : The new set of columns where every categorical column has been pivoted.
       output_dep_col : (String) the dependent column (un-transformed) in the output_table 
       col_distinct_vals_dict : (dict) A dict of distinct values for each column                 
    '''
    #Since we allow the user to specify the table name as "schema_name.table_name) and since the
    #information schema requires the table name to be separated out from schema name, so the following
    #ste is required only for the query to look-up column types. It will be used thereafter.
    tbl_schema = 'public' if '.' not in table_name else table_name.split('.')[0]
    tbl_nm = table_name.split('.')[1] if '.' in table_name else table_name
    
    output_table = '{default_schema}.{default_prefix}{table_name}'.format(default_schema=default_schema, 
                                                                          default_prefix=default_prefix, 
                                                                          table_name=tbl_nm
                                                                          )
    col_types_dict = __getColTypesDict__(conn,tbl_schema, tbl_nm)  
                                 
    #It is possible that the input columns could also have a 'bias' variable (intercept in linear regression)
    #The intercept is a number represented as a string. If such a value exists, remove it from the input columns
    #and consider it separately (we don't have to create a column for this variable in the transformed table).
    numeric_cols = []
    for col in cols:
        if (not col_types_dict.has_key(col) and isNumeric(col)):
            numeric_cols.append(col)
    #Remove the intercept variables from cols
    cols = [c for c in cols if c not in numeric_cols]

    #If all the columns in the input are numeric, return the original table along with its columns.
    has_categorical=False
    for col in cols:
        if(col_types_dict[col] in ['char','character varying', 'text']):
            has_categorical = True
    
    #Return original table and original list of columns        
    if(not has_categorical):
        return table_name, numeric_cols+cols, label, col_distinct_vals_dict
    
    if (not col_distinct_vals_dict):
        col_distinct_vals_dict = __getColDistinctValsDict__(conn, cols, col_types_dict, table_name)

    col_names_and_types_lst = __getColNamesAndTypesList__(cols,col_types_dict, col_distinct_vals_dict)

    __createPivotTable__(conn, output_table, col_types_dict, col_names_and_types_lst, label)
    #Now insert values into the new table                                                             
    __binarizeInParallel__(conn, table_name,output_table,cols,col_types_dict, col_distinct_vals_dict, label)                     
    #First include all numeric columns that correspond to any intercept/constant/bias variables
    #Then combine them with the independent variables (transformed or un-transformed)
    output_indep_cols = numeric_cols + [c[0] for c in col_names_and_types_lst]
    output_dep_col = label                                   
    return output_table, output_indep_cols, output_dep_col, col_distinct_vals_dict

def convertsColsToArray(conn, table_name, indep, dep=''):
    '''
       Convert a list of independent columns (all numeric) to an array column and return the transformed table
       
       Inputs:
       =======
       conn : A DBConnect object
       table_name : (string) the input table name
       indep : (list) a list of independent columns (all numeric)
       dep : (string) the dependent column in the input table. If empty, it will be ignored.
       
       Outputs:
       ========
       output_table : (string) the transformed table, where the list of columns in indep have been converted 
                      to an array.
       indep_cols_arr_name : (string) the name of the independent column (of type array) in the transformed table
    ''' 
    tbl_schema = 'public' if '.' not in table_name else table_name.split('.')[0]
    tbl_nm = table_name.split('.')[1] if '.' in table_name else table_name
    col_types_dict = __getColTypesDict__(conn,tbl_schema, tbl_nm)
    out_tbl_nm = tbl_nm.replace(default_prefix,'')
    output_table = '{default_schema}.{default_prefix_arr}{table_name}'.format(default_schema=default_schema, 
                                                                          default_prefix_arr=default_prefix_arr, 
                                                                          table_name=out_tbl_nm
                                                                          )
    indep_cols_arr_name = 'indep'
    #Check all columns are numeric      
    for col in indep:
        if (
               (col_types_dict.has_key(col) and col_types_dict[col] in ['char','character varying', 'text']) or 
               (not col_types_dict.has_key(col) and not isNumeric(col))
           ):
            raise 'Only numeric columns supported. Use pivotCategoricalColumns() to transform categorical columns'
            return 
    
    #Verify if all columns are numeric
    data_dict = {}
    data_dict['table_name'] = table_name
    data_dict['output_table'] = output_table
    data_dict['list_of_indep_cols'] = ','.join(indep)
    data_dict['indep_cols_arr_name'] = indep_cols_arr_name
    if(dep):
        convert_to_arr_stmt = '''
                                 drop table if exists {output_table} cascade;
                                 create table {output_table} as 
                                 (
                                     select array[{list_of_indep_cols}] as {indep_cols_arr_name},
                                            {dep}
                                     from {table_name}
                                 );
                              ''' 
        data_dict['dep'] = dep
    else:
        convert_to_arr_stmt = '''
                                 drop table if exists {output_table} cascade;
                                 create table {output_table} as 
                                 (
                                     select array[{list_of_indep_cols}] as {indep_cols_arr_name}
                                     from {table_name}
                                 );
                              '''               
        
    convert_to_arr_stmt = convert_to_arr_stmt.format(**data_dict)                              
    conn.executeQuery(convert_to_arr_stmt)
    return output_table, indep_cols_arr_name
                          
if(__name__=='__main__'):
    from pymadlib import DBConnect
    conn = DBConnect()
    output_table, indep, dep, cols_distinct_vals = pivotCategoricalColumns(conn,'cuse_dat',['1','age','education','wantsmore','notusing'],'yesusing')
    print 'output table :',  output_table
    print 'output independent columns :', indep
    print 'dependent col :',dep
    #Verify if the input has all numeric columns, the input table is returned unchanged.
    output_table, indep, dep, cols_distinct_vals = pivotCategoricalColumns(conn,'wine_training_set',['1','alcohol','proline','hue','color_intensity','flavanoids'],'quality')
    print 'output table :',  output_table
    print 'output independent columns :', indep
    print 'dependent col :',dep
    