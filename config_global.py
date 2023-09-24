'''
    this script contains global variables used in several scripts
'''
use_sqlite_db2=1  # 0= Use Kenna API calls and Not DB  1= Use SQLite DB  = for demos with demo data
kenna_host="kenna_host"
kenna_api_token='the_token_must_be_pasted_here' # or in ../keys/kenna.txt - just paste the token in the file
use_ngrok=0 # 0= don't use NGROK 1= Use ngrok
relay_module_fqdn='' # relay module API gateway needed for switching to main view, asset view or cve view. Keep blank if you use NGROK
use_webex_team=0 # use webex team to interact with admin
version='1.0.0'