from utils import *
from pymadlib import DBConnect
conn = DBConnect()

indep = ['1', 'age','gender','race','bmi','number_of_kids','education_level','income_level','diagnosis_code','treatment_code']
dep = 'infection_cost'
table_name = 'gp_patient_history_1million'
tname, idep, d, cdict = pivotCategoricalColumns(conn,table_name, indep, dep)

