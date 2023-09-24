'''
    this files contains resource that manages interaction with the sqllite database.
    
    SqlLite DB contains kenna demo data
'''

import sys
import sqlite3
from crayons import *
from datetime import datetime, timedelta
import time

def date_time():
	'''
		get current date time in yy-mm-dd-H:M:S:fZ format 
	'''
	current_time = datetime.utcnow()
	current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
	return(current_time)

def read_db(database,table,where_clause):
    '''
        read table with where clause in database 
    '''
    liste=[]
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()
        sql_request = f"SELECT * from {table} {where_clause}"
        #print()
        #print(sql_request)
        #print()
        try:
            cursor.execute(sql_request)
            for resultat in cursor:
                #print(resultat)        
                liste.append(resultat)
        except:
            sys.exit("couldn't read database")
    return(liste)

def new_alert_into_db(client):
    '''
        for demo : ingest demo alerts into amp_alerts and critical_alerts
    '''
    liste=[]    
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()
        sql_request = f"SELECT * from amp_alerts"
        print(sql_request)
        cursor.execute(sql_request)
        amp_index=0
        for resultat in cursor:
            #print(int(resultat[0]))  
            if int(resultat[0])>amp_index:
                amp_index=int(resultat[0])
            #liste.append(resultat)  
        amp_index+=1
        print(green(amp_index,bold=True))
        sql_request = f"SELECT * from critical_alerts"
        print(sql_request)
        cursor.execute(sql_request)
        critical_alerts_index=0
        for resultat in cursor:
            #print(int(resultat[0]))  
            if int(resultat[0])>critical_alerts_index:
                critical_alerts_index=int(resultat[0])
            #liste.append(resultat)      
        critical_alerts_index+=1
        print(green(critical_alerts_index,bold=True))     
        row=[]
        row.append(client)
        row.append('High')
        row.append('MALWARE ALERT')
        row.append('NEW')
        row.append('Secure EndPoint')
        current_time=date_time()
        row.append(current_time)
        sqlite_data=(critical_alerts_index, row[0] , row[1], row[2], row[3], row[4], row[5])
        #sql_request="INSERT OR IGNORE into critical_alerts (id, Customer,Severity,Description,Status,Source,DateTime ) VALUES (?,?,?,?,?,?,?)" 
        sql_request=f"INSERT OR IGNORE into critical_alerts (id, Customer,Severity,Description,Status,Source,DateTime ) VALUES ({critical_alerts_index}, '{row[0]}' , '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}')" 
        print(sql_request)
        #cursor.execute(sql_request, sqlite_data)
        cursor.execute(sql_request)
        conn.commit()   
        row=[]
        row.append(client)
        row.append('Demo Endpoint')
        row.append('192.168.8.14')
        current_time=date_time()
        row.append(current_time)
        row.append(current_time)
        row.append("Unresolved")
        row.append("High")
        sqlite_data=(amp_index, row[0] , row[1], row[2], row[3], row[4], row[5], row[6])
        sql_request=f"INSERT OR IGNORE into amp_alerts (id, customer,hostname,internal_ips,earliest_activity,latest_activity,status,severity  ) VALUES ({amp_index}, '{row[0]}' , '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}', '{row[5]}', '{row[6]}')" 
        print(sql_request)        
        cursor.execute(sql_request)
        conn.commit()         
        sql_request = f"UPDATE clients SET risk_status = '! ALERT !' where name = '{client}'"
        print(sql_request)        
        cursor.execute(sql_request)
        conn.commit()
    return(1)     
   
def update_client_db(database,table,client):
    liste=[]
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()
        try:
            sql_data=('')
            sql_request = f"UPDATE {table} SET selected = ''"
            print()
            print(sql_request)
            print()        
            cursor.execute(sql_request)
            sql_request = f"UPDATE {table} SET selected = 'YES' where name = '{client}'"
            print()
            print(sql_request)
            print()        
            cursor.execute(sql_request)            
        except:
            sys.exit("couldn't connect to database 2")
    return(liste)    
    
def update_db_generic(database,table,where_clause):
    liste=[]
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()
        sql_data=('')
        sql_request = f"UPDATE tasks SET selected = ? begin_date = ? end_date = ? WHERE id = ?"
        sql_request = f"UPDATE {table} SET selected = ?"
        print()
        print(sql_request)
        print()
        try:
            cursor.execute(sql_request,sql_data)
            for resultat in cursor:
                #print(resultat)        
                liste.append(resultat)
        except:
            sys.exit("couldn't read database")
    return(liste)     

def main(database,table):    
    #table="observables"
    file=open('out.txt','w')
    where=' where selected = "YES"'
    where=''
    resultats = read_db(database,table,where)    
    if resultats :
        for resultat in resultats:
            print(resultat)
            ligne_out=resultat[0]+';'+resultat[1]+';'+resultat[2]+';'+resultat[3]+';'+resultat[4]
            file.write(ligne_out)
            file.write('\n')
    else:
        print('NO RESULTS')
    file.close()
    
if __name__=='__main__':
    database="database.db"
    table="clients"
    #main(database,table)   
    client_name='ACME COMPANY'
    #update_client_db(database,table,client_name)
    new_alert_into_db(client_name)