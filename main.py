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
                    
                    # Separate clicks from opens
                    clicks = [s for s in statsArr if s.get('type') == 'click']
                    opens = [s for s in statsArr if s.get('type') != 'click']
                    
                    print('=' * 60)
                    print(f'📧 Email Tracking Report for: {var}')
                    print('=' * 60)
                    
                    # Show clicks first (most reliable)
                    if len(clicks) > 0:
                        print(f'\n🖱️  CONFIRMED CLICKS (100% Real User): {len(clicks)}')
                        print('-' * 60)
                        for idx, click in enumerate(clicks):
                            print(f'\n✅ Click #{idx+1}')
                            print(f'⏰ Time: {click["time"]}')
                            
                            if click['country'] != 'Unknown':
                                location_parts = []
                                if click['city'] != 'Unknown':
                                    location_parts.append(click['city'])
                                if click['regionName'] != 'Unknown':
                                    location_parts.append(click['regionName'])
                                if click['country'] != 'Unknown':
                                    location_parts.append(click['country'])
                                
                                if location_parts:
                                    print(f'📍 Location: {", ".join(location_parts)}')
                                print(f'🌐 IP Address: {click["ip"]}')
                            else:
                                print(f'📍 Location: Not available')
                                print(f'🌐 IP Address: {click["ip"]}')
                            print('-' * 60)
                    
                    # Show opens (may include Gmail proxy)
                    if len(opens) > 0:
                        print(f'\n📬 Image Opens (may include Gmail scans): {len(opens)}')
                        print('   (Use click tracking for accurate results)')
                    else:
                        print('\n📭 No opens yet')
                    
                    if len(clicks) == 0 and len(opens) == 0:
                        print('📭 Email not opened yet')
                    
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
                    
                    # Separate clicks from opens
                    clicks = [s for s in statsArr if s.get('type') == 'click']
                    opens = [s for s in statsArr if s.get('type') != 'click']
                    
                    print('=' * 60)
                    print(f'📧 Email Tracking Report for ID: {var}')
                    print('=' * 60)
                    
                    # Show clicks first (most reliable)
                    if len(clicks) > 0:
                        print(f'\n🖱️  CONFIRMED CLICKS (100% Real User): {len(clicks)}')
                        print('-' * 60)
                        for idx, click in enumerate(clicks):
                            print(f'\n✅ Click #{idx+1}')
                            print(f'⏰ Time: {click["time"]}')
                            
                            if click['country'] != 'Unknown':
                                location_parts = []
                                if click['city'] != 'Unknown':
                                    location_parts.append(click['city'])
                                if click['regionName'] != 'Unknown':
                                    location_parts.append(click['regionName'])
                                if click['country'] != 'Unknown':
                                    location_parts.append(click['country'])
                                
                                if location_parts:
                                    print(f'📍 Location: {", ".join(location_parts)}')
                                print(f'🌐 IP Address: {click["ip"]}')
                            else:
                                print(f'📍 Location: Not available')
                                print(f'🌐 IP Address: {click["ip"]}')
                            print('-' * 60)
                    
                    # Show opens (may include Gmail proxy)
                    if len(opens) > 0:
                        print(f'\n📬 Image Opens (may include Gmail scans): {len(opens)}')
                        print('   (Use click tracking for accurate results)')
                    else:
                        print('\n📭 No opens yet')
                    
                    if len(clicks) == 0 and len(opens) == 0:
                        print('📭 Email not opened yet')
                    
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
