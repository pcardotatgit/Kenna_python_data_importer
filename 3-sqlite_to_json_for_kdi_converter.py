'''
    read the Asset Vulnerability Results from DB and create the JSON data for KDI.
    
    Create entries into the JSON resulting file ONLY for assets which has vulnerabilities
    
    version 20230924
'''
from crayons import *
import sys
from read_database_kenna import read_db
import time
from datetime import datetime, timedelta

version='1.0.0'
vuln_defs=''

def current_date():
    current_time = datetime.utcnow()
    current_date = current_time.strftime("%Y-%m-%dT")
    return(current_date)

def get_vulnerabilities_for(asset_id,scanner_type):
    date=current_date()
    where_clause=" where asset_id='"+asset_id+"'"
    #print('where ',where_clause)
    result=read_db('database.db','vulnerabilities',where_clause)
    #print(cyan(result,bold=True))
    resultat=''
    vuln_defs=''
    vuln_def=[]
    if result:        
        for item in result:
            if item[20]=='0':
                status='open'
            else:
                status='closed'
            resultat0='''\t\t\t\t{        
                    "scanner_identifier": '''+item[3]+''',
                    "vuln_def_name": "'''+item[8]+'''",
                    "scanner_type": "'''+scanner_type+'''",
                    "created_at": "'''+date+'''T00:00:00+00:00",
                    "last_seen_at": "'''+date+'''T00:00:00+00:00",
                    "last_fixed_on": "2023-06-03T00:00:00+00:00",
                    "scanner_score": '''+item[10]+''',
                    "override_score": '''+item[10]+''',
                    "status": "'''+status+'''"\n\t\t\t\t},\n'''               
            resultat=resultat+resultat0            
            vuln_def.append([item[8],scanner_type,'WASC-17'] )
            print('get_vulnerabilities_for > name :',item[8])
            #a=input('get_vulnerabilities_for > found name :')
        resultat=resultat[:-2]
        #print(yellow(vuln_def))
        #print()
        #print()
    return(resultat,vuln_def)

if __name__ == "__main__":
    vuln_defs=[]
    vuln_def=[]
    print()  
    print(yellow(f'------ Kenna JSON DATA GENERATOR FOR KDI CONNECTOR {version} ------',bold=True))
    print() 
    scanner_type = input('what is the scanner name ? ( ex : Qualsys - default = My_Scanner ) : ')
    if scanner_type=="":
        scanner_type="My_Scanner"
    with open('./data_for_kdi/data_for_kdi.json','w') as file:
        line_out='''{
    "skip_autoclose": false,
    "version": 2,
    "assets": ['''
        file.write(line_out)
        file.write("\n")
        print(yellow(f'- Let\' get asset from DB',bold=True))
        where_clause=""
        result=read_db('database.db','assets',where_clause)
        if result:
            line_out=''
            print(cyan(result,bold=True))
            line_out=''
            line_out3=''
            for item in result:
                print(yellow('======================================================>',bold=True))
                print(yellow('new asset',bold=True))
                print()
                line_out2='\t\t{\n\t\t\t'            
                print(' New item is : ',green(item,bold=True))
                line_out2=line_out2+'"'+item[4]+'":"'+item[5]+'",\n\t\t\t'
                if item[2]:
                    line_out2=line_out2+'"os":"'+item[2]+'",\n\t\t\t'    
                if item[8] and item[4]!='ip_address':
                    line_out2=line_out2+'"ip_address":"'+item[8]+'",\n\t\t\t'                     
                if item[4]=="file":
                    if 'php' in item[5]:
                        line_out2=line_out2+'"application":"Appache Web Server",\n\t\t\t'# for the demo ! change that
                    else:
                        line_out2=line_out2+'"application":"BookStore",\n\t\t\t'# for the demo ! change that
                line_out2=line_out2+'"priority":'+item[3]+',\n'
                vulns,vuln_def_list=get_vulnerabilities_for(item[1],scanner_type) # get vulnerabilities for this asset
                print('vulns :',cyan(vulns))
                print('vuln_def_list',cyan(vuln_def_list))
                #a = input('stop :')
                for item3 in vuln_def_list:
                    print('--',yellow(item3,bold=True))
                    if item3 and item3 not in vuln_defs:                    
                        vuln_defs.append(item3)
                        print('----',yellow(' add it into vuln_defs',bold=True))
                    else:
                        print('----',red('Already into vuln_defs',bold=True))
                if vulns:                    
                    line_out2=line_out2+'\t\t\t"vulns": [\n'          
                    line_out2=line_out2+vulns
                    line_out2+='\n\t\t\t],'
                    line_out2+='\n\t\t\t"findings": [\n' 
                    line_out2=line_out2+vulns              
                    line_out2+='\n\t\t\t]\n\t\t},\n'   
                    line_out3+=line_out2
                else:
                    line_out2=''
                    #a=input('No Vulns ! continue ?')
                    print(red(" no vuln for this asset. We dont keep it",bold=True))
                print (' line to save : \n',blue(line_out2,bold=True))
            line_out=line_out3[:-2]       
            line_out+='\n\t],\n'             
            file.write(line_out)   
            # vuln_defs
            line_out='\t"vuln_defs": [\n' 
            for item in vuln_defs:
                line_out+='\t\t{\n'
                line_out=line_out+'\t\t\t"name": "'+item[0]+'",\n'
                line_out=line_out+'\t\t\t"scanner_type": "'+scanner_type+'",\n'
                line_out=line_out+'\t\t\t"wasc_identifiers": "WASC-17"\n\t\t},\n'
            # file trailer            
            line_out=line_out[:-2]
            line_out+='\n\t]\n}'
            file.write(line_out)                  
    print("===============================================================")
    print()
    print(green("OK Done the resuluting file is : ./data_for_kdi/data_for_kdi.json",bold=True))