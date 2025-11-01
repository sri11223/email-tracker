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
    recipient = input('enter recipient email/name (will be embedded in URL): ')
    myobj = {'title': title, 'recipient': recipient}
    responseData = requests.post(url, data = myobj)
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        response_json = json.loads(responseData.content.decode("utf-8"))
        if 'uuid' in response_json:
            tracking_url = url + str(response_json['uuid'])
            # Add recipient parameter to URL if provided
            if recipient:
                tracking_url += f'&r={requests.utils.quote(recipient)}'
            print('✅ Tracking URL Created!\n')
            print(f'👤 For: {recipient if recipient else "Not specified"}\n')
            print(tracking_url)
            print('\n📋 HTML tag:')
            print(f'<img src="{tracking_url}" width="1" height="1">')
            print('\n💡 Tip: The recipient "{}" will be automatically recorded when they open the email!'.format(recipient))
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
        recipient = responseData[i].get('recipient', 'Not specified')
        print('Title: ' + str(responseData[i]['title']) + ', ' + 'Recipient: ' + str(recipient) + ', ' + 'Created: ' + str(responseData[i]['dateTime']), '\nNumber of times opened: ' + str(responseData[i]['counter']) + ', ' + 'Tracking ID: ' + str(responseData[i]['uuid']))
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
                    
                    print('=' * 60)
                    print(f'📧 Email Tracking Report for: {var}')
                    print(f'👤 Recipient: {responseData[i].get("recipient", "Not specified")}')
                    print(f'Total Activity: {len(statsArr)} events')
                    print('=' * 60)
                    
                    if len(statsArr) > 0:
                        # Show all opens with smart analysis
                        print(f'\n📊 TRACKING EVENTS:')
                        print('-' * 60)
                        
                        # Smart detection: First 2-3 opens are usually Gmail scans
                        # Opens after 5+ minutes are likely real user opens
                        from datetime import datetime
                        
                        for idx, event in enumerate(statsArr):
                            print(f'\n📌 Event #{idx+1}')
                            print(f'⏰ Time: {event["time"]}')
                            
                            # Show who opened if available
                            if 'recipient' in event and event['recipient'] != 'Unknown':
                                print(f'👤 Opened by: {event["recipient"]}')
                            
                            # Analyze if likely real or scan
                            if idx < 2:
                                likelihood = "⚠️  Likely Gmail Scan (within first 2 events)"
                            else:
                                likelihood = "✅ Likely Real Open (after initial scans)"
                            
                            print(f'📈 Analysis: {likelihood}')
                            
                            if event['country'] != 'Unknown':
                                location_parts = []
                                if event['city'] != 'Unknown':
                                    location_parts.append(event['city'])
                                if event['regionName'] != 'Unknown':
                                    location_parts.append(event['regionName'])
                                if event['country'] != 'Unknown':
                                    location_parts.append(event['country'])
                                
                                if location_parts:
                                    print(f'📍 Location: {", ".join(location_parts)}')
                                print(f'🌐 IP: {event["ip"]}')
                            
                            print('-' * 60)
                        
                        # Summary
                        print(f'\n💡 SUMMARY:')
                        print(f'   • First 1-2 opens: Usually Gmail security scans')
                        print(f'   • Opens after that: Likely real recipient opens')
                        print(f'   • Multiple opens = Email was definitely delivered ✅')
                    else:
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
                    
                    print('=' * 60)
                    print(f'📧 Email Tracking Report for ID: {var}')
                    print(f'👤 Recipient: {responseData[i].get("recipient", "Not specified")}')
                    print(f'Total Activity: {len(statsArr)} events')
                    print('=' * 60)
                    
                    if len(statsArr) > 0:
                        # Show all opens with smart analysis
                        print(f'\n📊 TRACKING EVENTS:')
                        print('-' * 60)
                        
                        # Smart detection: First 2-3 opens are usually Gmail scans
                        # Opens after 5+ minutes are likely real user opens
                        from datetime import datetime
                        
                        for idx, event in enumerate(statsArr):
                            print(f'\n📌 Event #{idx+1}')
                            print(f'⏰ Time: {event["time"]}')
                            
                            # Show who opened if available
                            if 'recipient' in event and event['recipient'] != 'Unknown':
                                print(f'👤 Opened by: {event["recipient"]}')
                            
                            # Analyze if likely real or scan
                            if idx < 2:
                                likelihood = "⚠️  Likely Gmail Scan (within first 2 events)"
                            else:
                                likelihood = "✅ Likely Real Open (after initial scans)"
                            
                            print(f'📈 Analysis: {likelihood}')
                            
                            if event['country'] != 'Unknown':
                                location_parts = []
                                if event['city'] != 'Unknown':
                                    location_parts.append(event['city'])
                                if event['regionName'] != 'Unknown':
                                    location_parts.append(event['regionName'])
                                if event['country'] != 'Unknown':
                                    location_parts.append(event['country'])
                                
                                if location_parts:
                                    print(f'📍 Location: {", ".join(location_parts)}')
                                print(f'🌐 IP: {event["ip"]}')
                            
                            print('-' * 60)
                        
                        # Summary
                        print(f'\n💡 SUMMARY:')
                        print(f'   • First 1-2 opens: Usually Gmail security scans')
                        print(f'   • Opens after that: Likely real recipient opens')
                        print(f'   • Multiple opens = Email was definitely delivered ✅')
                    else:
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
