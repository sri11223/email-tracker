import requests
import json

url = 'https://email-tracker-ity3.onrender.com/'

# Get all data
print("Fetching all tracking records...")
response = requests.get(url + 'data')
data = json.loads(response.content.decode("utf-8"))

print(f"\nFound {len(data)} tracking records:")
print("-" * 60)

for item in data:
    print(f"📧 {item['title']} - Opens: {item['counter']} - Created: {item['dateTime']}")

print("-" * 60)

# Ask for confirmation
confirm = input("\n⚠️  Do you want to DELETE ALL tracking data? (yes/no): ")

if confirm.lower() == 'yes':
    print("\n🗑️  Deleting all tracking data...")
    response = requests.delete(url + 'data/clear')
    result = json.loads(response.content.decode("utf-8"))
    
    if result.get('success'):
        print("✅ All tracking data cleared successfully!")
    else:
        print(f"❌ Error: {result.get('message')}")
else:
    print("❌ Operation cancelled")
