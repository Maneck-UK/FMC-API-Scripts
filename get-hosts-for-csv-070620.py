import json
import sys
import requests
import getpass
import urllib3

#Prevent SSL certificate warnings
urllib3.disable_warnings()

#Option menu
menu = {}
menu["1"]="-- List all FMC host objects with IP and Object ID" 
menu["2"]="-- List all FMC host objects full JSON output"

while True: 
    options=menu.keys()
    print("\n" * 100)
    print("\n\n")
    print("GET Hosts from FMC")
    print("\n\n")
    for entry in options: 
        print(entry, menu[entry])
    selection=input("\nSelect an option: ")
    if selection in menu:
        break

#Get FMC Server        
server_start = "https://"
server_main = input("\nEnter the IP or FQDN of your FMC: https://")
server = server_start + server_main

#Get FMC Credentials
username = input("Username: ")
password = getpass.getpass("Password: ")

#Update to console
print("\nAccessing FMC API...", end ="")

#Enable output to be logged and specify outputfile
orig_stdout = sys.stdout
sys.stdout = open('GEToutput.txt', 'w')

#Define authentication elements
r = None
headers = {'Content-Type': 'application/json'}
api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
auth_url = server + api_auth_path

#Generate insecure auth token for API operation
try:
    r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify=False)
    auth_headers = r.headers
    auth_token = auth_headers.get('X-auth-access-token', default=None)
    auth_domain = auth_headers.get('DOMAIN_UUID', default=None)
    if auth_token == None:
        print("auth_token not found. Exiting...")
        sys.exit()
except Exception as err:
    print ("Error getting auth token : "+str(err))
    sys.exit()
 
#Create authenticated url for API operation
headers['X-auth-access-token']=auth_token 
api_path = "/api/fmc_config/v1/domain/" + auth_domain + "/object/hosts?expanded=true&limit=1000"
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]

#Generate insecure auth token for API operation 
try:
    r = requests.get(url, headers=headers, verify=False)
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        json_resp = json.loads(resp)
    else:
        r.raise_for_status()
        print("GET error : "+resp)
except requests.exceptions.HTTPError as err:
    print ("Connection error : "+str(err)) 

finally:
    if r : r.close()

#GET host objects in text format    
if selection == "1":
    print("hostname,ipaddress,objectid")
    for HOST in json_resp['items']:
        print(HOST['name'] + "," + HOST['value'] + "," + HOST['id'])
#GET host objects in JSON format 
elif selection == "2":
    print(json.dumps(json_resp['items'],indent=3, separators=(',', ': ')))
else:
    sys.exit()
#Disable output to be logging
sys.stdout = orig_stdout

#Update to console
print("Completed\n\nLocate GEToutput.txt int the script execution directory\n")
#End script mode
input("Press <Enter> to close this window.")