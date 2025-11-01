import requests
import json
import os
from requests.models import Response

# DO NOT PUT YOUR LOCALHOST URL HERE, INSTEAD TRY DEPLOYING IT ON HEROKU, AWS, ETC. 
# OR USE NGROK TO GET AN TEMPORARY URL
# 
# EXAMPLE WITH NGROK:- 
# url = 'https://9a90-43-242-115-265.ngrok.io/'

# Deployed on Render.com
url = 'https://email-tracker-ity3.onrender.com/'     

def create():
    title = input('enter title: ')
    myobj = {'title': title}
    responseData = requests.post(url, data = myobj)
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        response_json = json.loads(responseData.content.decode("utf-8"))
        if 'uuid' in response_json:
            print(url + str(response_json['uuid']))
        else:
            print('Error from server:')
            print(response_json)
    except Exception as e:
        print(f'Error: {e}')
        print(f'Server response: {responseData.content.decode("utf-8")}')
    print('\n\n\n')
    
def getData():
    response = requests.get(url + 'data')
    responseData = json.loads(response.content.decode("utf-8"))    # responseData = json.loads(yasd)
    os.system('cls' if os.name == 'nt' else 'clear')
    # print(responseData)
    i = 0
    while i != len(responseData):
        print('Title: ' + str(responseData[i]['title']) + ', ' + 'Created: ' + str(responseData[i]['dateTime']), '\nNumber of times opened: ' + str(responseData[i]['counter']) + ', ' + 'Tracking ID: ' + str(responseData[i]['uuid']))
        print('\n')
        i += 1 

def info():
    response = requests.get(url + 'data')
    responseData = json.loads(response.content.decode("utf-8"))    # responseData = json.loads(yasd)
    
    main = input('Return Info by \n(1) Title (2) Tracking ID \n=>')
    
    if main == '1':    
        i = 0
        var = input('Enter Title\n=>')
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\n')
        while i != len(responseData):
            if str(responseData[i]['title']) == var:
                # statsArr = json.loads(responseData[i]['stats'])
                statsArr = responseData[i]['stats']
                if statsArr != 'Null':
                    statsArr = json.loads(statsArr)
                    x = 0
                    print('=' * 60)
                    print(f'📧 Email Tracking Report for: {var}')
                    print(f'Total Opens: {len(statsArr)}')
                    print('=' * 60)
                    while len(statsArr) != x:
                        print(f'\n🔍 Open #{x+1}')
                        print(f'⏰ Time: {statsArr[x]["time"]}')
                        
                        # Only show if not "Unknown"
                        if statsArr[x]['country'] != 'Unknown':
                            location_parts = []
                            if statsArr[x]['city'] != 'Unknown':
                                location_parts.append(statsArr[x]['city'])
                            if statsArr[x]['regionName'] != 'Unknown':
                                location_parts.append(statsArr[x]['regionName'])
                            if statsArr[x]['country'] != 'Unknown':
                                location_parts.append(statsArr[x]['country'])
                            
                            if location_parts:
                                print(f'📍 Location: {", ".join(location_parts)}')
                            print(f'🌐 IP Address: {statsArr[x]["ip"]}')
                        else:
                            print(f'📍 Location: Not available (Email opened via proxy/Gmail servers)')
                            print(f'🌐 IP Address: {statsArr[x]["ip"]}')
                        
                        print('-' * 60)
                        x += 1
                    break
                else:
                    print('📭 Email not opened yet')
        
            i += 1 
    
    if main == '2':    
        i = 0
        var = input('Enter Tracking ID(Example:- 5359ebc0-c4f2-49b5-9074-0ce0adb03a6e)\n=>')
        os.system('cls' if os.name == 'nt' else 'clear')
        print('\n\n')
        while i != len(responseData):
            if str(responseData[i]['uuid']) == var:
                # statsArr = json.loads(responseData[i]['stats'])
                statsArr = responseData[i]['stats']
                if statsArr != 'Null':
                    statsArr = json.loads(statsArr)
                    x = 0
                    print('=' * 60)
                    print(f'📧 Email Tracking Report for ID: {var}')
                    print(f'Total Opens: {len(statsArr)}')
                    print('=' * 60)
                    while len(statsArr) != x:
                        print(f'\n🔍 Open #{x+1}')
                        print(f'⏰ Time: {statsArr[x]["time"]}')
                        
                        # Only show if not "Unknown"
                        if statsArr[x]['country'] != 'Unknown':
                            location_parts = []
                            if statsArr[x]['city'] != 'Unknown':
                                location_parts.append(statsArr[x]['city'])
                            if statsArr[x]['regionName'] != 'Unknown':
                                location_parts.append(statsArr[x]['regionName'])
                            if statsArr[x]['country'] != 'Unknown':
                                location_parts.append(statsArr[x]['country'])
                            
                            if location_parts:
                                print(f'📍 Location: {", ".join(location_parts)}')
                            print(f'🌐 IP Address: {statsArr[x]["ip"]}')
                        else:
                            print(f'📍 Location: Not available (Email opened via proxy/Gmail servers)')
                            print(f'🌐 IP Address: {statsArr[x]["ip"]}')
                        
                        print('-' * 60)
                        x += 1
                    break
                else:
                    print('📭 Email not opened yet')

            i += 1

while True:
    print("<============================>")
    main = input('1) create a tracking url \n2) get all the active urls \n3) get active url info \n=>')
    if main == '1':
        create()
    if main == '2':
        getData()
    if main == '3':
        info()
