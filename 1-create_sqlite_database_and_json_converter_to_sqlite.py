'''
    create Kenna demo data for the generic python KDI connector, and store them into the SQLite database
'''
import sys
import csv
from crayons import *
import json
import sqlite3
import time
from datetime import datetime, timedelta

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
    
def date_plus_x_days2(nb): 
    '''
        calculate current date + nb day in yy-mm-dd format 
    '''
    current_time = datetime.utcnow()
    start_time = current_time + timedelta(days=nb)
    timestampStr = start_time.strftime("%Y-%m-%d")
    return(timestampStr)
    
def date_plus_x_days(nb): 
    '''
        calculate current date + nb day in yy-mm-dd-H:M:S:fZ format 
    '''
    current_time = datetime.utcnow()
    start_time = current_time + timedelta(days=nb)
    timestampStr = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return(timestampStr)

def create_db_and_table():    
    #with sqlite3.connect(':memory:') as conn:
    with sqlite3.connect('database.db') as conn:
        c=conn.cursor()
        try:            
            print("--CUSTOM create assets table")
            sql_create=f"CREATE TABLE IF NOT EXISTS assets ( id text PRIMARY KEY, asset_id text,operating_system  text,priority text,primary_locator text,locator text,vulnerabilities_count text,status text,ip_address text,hostname text,mac_address text,risk_meter_score text);" 
            c.execute(sql_create)
            print("--- OK assets table created")
            
            print("--CUSTOM create vulnerabilities table")
            sql_create=f"CREATE TABLE IF NOT EXISTS vulnerabilities ( id text PRIMARY KEY,vulnerability_id text,status text,priority text,identifiers text,asset_id text,urls text,solution text,cve_id text,cve_description text, severity text ,threat, popular_target text, active_internet_breach text, easily_exploitable text, malware_exploitable text, remote_code_execution text,predicted_exploitable text,top_priority text,risk_meter_score text,created_at text,cve_published_at text,patch_published_at text,first_found_on text,last_seen_time text,due_date text,closed_at text,closed text);" 
            c.execute(sql_create)
            print("--- OK vulnerabilities table created")                        
                
        except:
            sys.exit("couldn't create database.db")
    return()
        
def feed_database():
    conn=create_connection('database.db') # open connection to database
    index=0
    file='./init/assets.json'
    with open(file,'r') as file:
        text_data=file.read()
        json_data=json.loads(text_data)
        assets=json_data['assets']
        print(cyan(json_data,bold=True))
        for item in assets:        
            asset_id=item['id']
            operating_system=item['operating_system']
            priority=item['priority']
            primary_locator=item['primary_locator']
            locator=item['locator']
            vulnerabilities_count=item['vulnerabilities_count']
            status=item['status']
            ip_address=item['ip_address']
            hostname=item['hostname']
            mac_address=item['mac_address']
            risk_meter_score=item['risk_meter_score']
            if conn:
                # connection to database is OK
                c=conn.cursor()
                # let's go to every lines one by one and let's extract url, targeted brand    
                sqlite_data=(index, asset_id , operating_system, priority, primary_locator, locator, vulnerabilities_count,status,ip_address,hostname,mac_address,risk_meter_score)
                sql_add="INSERT OR IGNORE into assets (id, asset_id,operating_system ,priority,primary_locator,locator,vulnerabilities_count,status,ip_address,hostname,mac_address,risk_meter_score ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
                c.execute(sql_add, sqlite_data)
                index+=1
                conn.commit()                
        print()
        print(' ==> assets data OK') 
        print()              
    
    index=0
    file='./init/vulnerabilities.json'
    with open(file,'r') as file:
        text_data=file.read()
        json_data=json.loads(text_data)
        assets=json_data['vulnerabilities']
        print(cyan(json_data,bold=True))
        for item in assets:        
            vulnerability_id=item['id']
            status=item['status']
            cve_id=item['cve_id']
            asset_id=item['asset_id']
            priority=item['priority']
            #urls=item['urls']
            identifiers='identifiers'
            urls='urls'            
            solution=item['solution']
            cve_description=item['cve_description']            
            severity=item['severity']
            threat=item['threat']
            popular_target=item['popular_target']
            active_internet_breach=item['active_internet_breach']
            easily_exploitable=item['easily_exploitable']
            malware_exploitable=item['malware_exploitable']
            remote_code_execution=item['remote_code_execution']
            predicted_exploitable=item['predicted_exploitable']
            top_priority=item['top_priority']
            risk_meter_score=item['risk_meter_score'] 
            closed=item['closed']             
            created_at=item['created_at']
            cve_published_at=item['cve_published_at']
            patch_published_at=item['patch_published_at']
            first_found_on=item['first_found_on']
            last_seen_time=item['last_seen_time']
            due_date=item['due_date']     
            closed_at=item['closed_at'] 
            if conn:
                # connection to database is OK
                c=conn.cursor()
                # let's go to every lines one by one and let's extract url, targeted brand    
                sqlite_data=(index,vulnerability_id,status,priority,identifiers,asset_id,urls,solution,cve_id,cve_description, severity ,threat, popular_target, active_internet_breach, easily_exploitable, malware_exploitable, remote_code_execution,predicted_exploitable,top_priority,risk_meter_score,created_at,cve_published_at,patch_published_at,first_found_on,last_seen_time,due_date,closed_at,closed)
                sql_add="INSERT OR IGNORE into vulnerabilities (id, vulnerability_id,status,priority,identifiers,asset_id,urls,solution,cve_id,cve_description, severity ,threat, popular_target, active_internet_breach, easily_exploitable, malware_exploitable, remote_code_execution,predicted_exploitable,top_priority,risk_meter_score,created_at,cve_published_at,patch_published_at,first_found_on,last_seen_time,due_date,closed_at,closed) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                c.execute(sql_add, sqlite_data)
                index+=1
                conn.commit()                
        print()
        print(' ==> vulnerabilities data OK') 
        print() 
                       
def create_database_if_not_exits():
    try:
        f = open("database.db")
        print(green("- OK the database exists",bold=True))
        f.close()        
    except IOError:
        print(red("- NOK the database DO NOT exists... let's create it",bold=True))
        print('Create database.db')
        create_db_and_table()
        print(green('OK database.db created',bold=True))
        print(yellow('Now update demo data',bold=True))
        feed_database()
        print('-- OK demo data ingested')
        
if __name__ == "__main__":
    create_database_if_not_exits()
    print('ALL DONE')
    print()
    print(yellow('Now run init_modif_scores.py in order to calculate demos risk score',bold=True))