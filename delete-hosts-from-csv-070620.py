import csv
import json
import sys
import requests
import os
import getpass
import urllib3

#Prevent SSL security warning
urllib3.disable_warnings()

#Get FMC Server
server_start = "https://"
server_main = input("\nEnter the IP or FQDN of your FMC: https://")
server = server_start + server_main

#Get FMC Credentials
username = input("Username: ")
password = getpass.getpass("Password: ")

#Update to console
print("\nAccessing the FMC API, please wait...", end="")

#Define authentication elements
headers = {'Content-Type': 'application/json'}
api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
auth_url = server + api_auth_path
r = None

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
    print("Error generating auth token -> "+str(err))
    sys.exit()

#Create authenticated url for API operation
headers['X-auth-access-token']=auth_token
print('Connected, auth token collected (' + auth_token + (')\n'))
api_path = "/api/fmc_config/v1/domain/" + auth_domain + "/object/hosts/"

#CSV operation and file : csv file called in script command
#csvfile = open(sys.argv[1])
#objects = csv.DictReader(csvfile)

#CSV operation and file specified
f = open("del-host-by-id.csv")
elementsfile = csv.DictReader(f)

#Identify data to use for host deletion
for element in elementsfile:
    del_data = {
        element["objectid"],
    }
#Create authenticated url for API operation
    for element in del_data:
        del_url = server + api_path + element
        try:
#Update to console
            print(del_url)
            r = requests.delete(del_url, headers=headers, verify=False)
            status_code = r.status_code
            resp = r.text
            log = open('delete_objects.log', 'a')
            print(" Status code: "+str(status_code))
            json_resp = json.loads(resp)
            log.write('\n=====\n')
            log.write(json.dumps(json_resp,sort_keys=True,indent=4, separators=(',', ': ')))
#Notify codes to console
            if status_code == 201 or status_code == 202:
                print(" SUCCESS ")
            elif status_code == 400:
                print((" Message: ")+ resp + ('\n'))
            elif status_code == 404:
                print((" Message: ")+ resp + ('\n'))   
            else:
                r.raise_for_status()
                print((" Message: ")+ resp + ('\n'))
        except requests.exceptions.HTTPError as err:
            print("Connection error -> "+str(err))
        finally:
            if r: r.close()

#Update to console
print('\nLog file "delete_objects.log" appended\n')
#End script mode
input("Press <Enter> to return to CMD prompt")
