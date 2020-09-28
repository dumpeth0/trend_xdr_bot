import requests
import json
from datetime import datetime

#XDR Base URL
url_base = 'https://api.xdr.trendmicro.com'

#Your XDR user token
token = 'YOUR_XDR_API_TOKEN_HERE'
headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json;charset=utf-8'}

def getRoles():
    #Function to get all XDR User Roles.
    url_path = '/v1.0/xdr/portal/accounts/roles'
    
    query_params = {}
    r = requests.get(url_base + url_path, params=query_params, headers=headers)

    return(r.json()['data']['roles'])

def getModels():
    #Function to get all XDR Machine Learning Models.
    url_path = '/v1.0/xdr/dmm/models'
    query_params = {}

    r = requests.get(url_base + url_path, params=query_params, headers=headers)
    
    resp_dict = json.loads(r.text)
    result = []
    
    for k in resp_dict["data"]:
        result.append(k['name'] + ' || ')
                 
    return(result)

def getWorkbench():
    #Get the Workenchs opened since 09/01/2020 with High or Medium Severity.
    url_path = '/v2.0/siem/events'
       
    #Get the exactly hour during the script execution
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S"+ ".000Z")
    
    #If you want to change the timeframe edit the startDateTime and endDateTime. 
    query_params = {'startDateTime':'2020-09-01T10:00:00.000Z','endDateTime': date}
    r = requests.get(url_base + url_path, params=query_params, headers=headers)
     
    resp_dict = json.loads(r.text)
    result = []

    for k in resp_dict['data']['workbenchRecords']:
        if k['severity'] == 'high' or k['severity'] == 'medium':
            result.append(k['workbenchName'] + ' - ' + k['workbenchId'] + ' - ' + k['severity'] + ' - '+ k['workbenchLink'] + ' || ')
                             
    return(result)

def countWorkbench():
    #Get the Workenchs opened since 09/01/2020 with all Severity.
    url_path = '/v2.0/siem/events'
       
    #Get the exactly hour during the script execution
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S"+ ".000Z")
    
    #If you want to change the timeframe edit the startDateTime and endDateTime. 
    query_params = {'startDateTime':'2020-09-01T10:00:00.000Z','endDateTime': date}
    r = requests.get(url_base + url_path, params=query_params, headers=headers)
     
    resp_dict = json.loads(r.text)
    countH = 0
    countM = 0
    countL = 0

    for k in resp_dict['data']['workbenchRecords']:
        if k['severity'] == 'high':
            countH += 1
        elif k['severity'] == 'medium':
            countM += 1
        else:
            countL += 1
            
    return("Low:" + str(countL) + "\nMedium:" + str(countM) + "\nHigh:" + str(countH))

def blockDomain():
    #Block the domain 0secops.com. If you want to change the domain, set your own in the targetValue.
    url_path = '/v1.0/xdr/response/block'
    query_params = {}
    body = '''
    {
        "valueType": "domain",
        "targetValue": "0secops.com",
        "productId": "sao",
        "description": "Telegram Bot"
    }
    '''
    
    r = requests.post(url_base + url_path, params=query_params, headers=headers, data=body)

    action_id = (r.json()['actionId'])
    return(action_id)

def removeDomain():
    #Remove the domain 0secops.com. If you want to change the domain, set your own in the targetValue.
    url_path = '/v1.0/xdr/response/restoreBlock'
    query_params = {}
    body = '''
    {
        "valueType": "domain",
        "targetValue": "0secops.com",
        "productId": "sao",
        "description": "Telegram Bot"
    }
    '''
    
    r = requests.post(url_base + url_path, params=query_params, headers=headers, data=body)

    action_id = r.json()['actionId']
    
    while True:
        status = r.json()['taskStatus']
        if status == "skipped":
            return("ID: " + action_id + "\nStatus: Skipped")
        if status == "success":
            return("ID: " + action_id + "\nStatus: Success")
        elif status == "failed":
            return("ID: " + action_id + "\nStatus: Failed")
        else:
            return("ID: " + action_id + "\nStatus: STATUS NOT WORKING YET...")

def getResponse(action_id):
    #Function to monitoring the status of a response sent to the console.
    url_path = '/v1.0/xdr/response/getTask'
    query_params = {'actionId': action_id}
    
    r = requests.get(url_base + url_path, params=query_params, headers=headers)
        
    while True:
        status = r.json()['data']['taskStatus']
        if status == "skipped":
            return("Skipped")
        if status == "success":
            return("Success")
        elif status == "failed":
            return("Failed")
        else:
            return("STATUS NOT WORKING YET...")


    
