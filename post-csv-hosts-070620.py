import csv
import json
import sys
import requests
import os
import getpass
import urllib3

#Prevent SSL certificate warnings
urllib3.disable_warnings()

#Get FMC Server
server_start = "https://"
server_main = input("\nEnter FMC IP or FQDN: https://")
server = server_start + server_main

#Get FMC Credentials
username = input("Username: ")
password = getpass.getpass("Password: ")

#Update to console
print("\nAccessing FMC API...", end ="")

#Define authentication elements
headers = {'Content-Type': 'application/json'}
api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
auth_url = server + api_auth_path
r = None

#CSV operation and file : csv file called in script command
csvfile = open(sys.argv[1])
elementsfile = csv.DictReader(csvfile)

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
    print ("auth token error : "+str(err))
    sys.exit()

#Create authenticated url for API operation 
headers['X-auth-access-token']=auth_token
print('Auth token OK (' + auth_token + (')\n'))
api_path = "/api/fmc_config/v1/domain/" + auth_domain + "/object/hosts"
url = server + api_path
if (url[-1] == '/'):
    url = url[:-1]

#Identify data to use for host creation
for element in elementsfile:
    post_data = {
        "name": element["name"],
        "type": element["type"],
        "value": element["value"],
        "description": element["description"],
    }
#Update to console
    print('\n*****')
    print('Creating host: ' + element["name"])
#POST host to API
    try:
        r = requests.post(url, data=json.dumps(post_data), headers=headers, verify=False)
        status_code = r.status_code
        resp = r.text
        log = open('post_hosts.log', 'a')
        print(" Status code: "+str(status_code))
        json_resp = json.loads(resp)
        log.write('\n=====\n')
        log.write(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
        if status_code == 201 or status_code == 202:
            print (" SUCCESS ")
        elif status_code == 400:
            print ((" Message: ")  + resp + ('\n'))
        else:
            r.raise_for_status()
            print ((" Message: ")  + resp + ('\n'))
    except requests.exceptions.HTTPError as err:
        print ("Error in connection -> "+str(err))
    finally:
        if r: r.close()

#Update to console
print('\nLog file "post_hosts.log" appended\n')
#End script mode
input("Press <Enter> to return to CMD prompt")