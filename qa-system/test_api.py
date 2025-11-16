# test_api.py
# quick script to test the API and see what we're working with

import requests
import json

BASE_URL = "https://november7-730026606190.europe-west1.run.app"

def test_messages_endpoint():
    """test the messages endpoint and see the data structure"""
    
    print("🔍 Testing /messages/ endpoint...\n")
    
    # test with small limit first
    response = requests.get(
        f"{BASE_URL}/messages/",
        params={"skip": 0, "limit": 5}
    )
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"✅ API is working!")
        print(f"📊 Total messages available: {data.get('total', 0)}")
        print(f"📝 Items in this page: {len(data.get('items', []))}\n")
        
        # show first message as example
        if data.get('items'):
            print("Example message:")
            print(json.dumps(data['items'][0], indent=2))
            print("\n" + "="*50 + "\n")
            
            # show all messages in this batch
            print("First 5 messages:\n")
            for i, msg in enumerate(data['items'], 1):
                print(f"{i}. {msg.get('user_name', 'Unknown')}: {msg.get('message', '')[:100]}...")
        
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def test_full_fetch():
    """test fetching all messages with pagination"""
    
    print("\n" + "="*50)
    print("🔄 Testing full pagination...\n")
    
    all_messages = []
    skip = 0
    limit = 100
    
    while True:
        response = requests.get(
            f"{BASE_URL}/messages/",
            params={"skip": skip, "limit": limit}
        )
        
        if response.status_code != 200:
            print(f"❌ Error at skip={skip}")
            break
        
        data = response.json()
        items = data.get('items', [])
        
        if not items:
            break
        
        all_messages.extend(items)
        print(f"📦 Fetched page: skip={skip}, got {len(items)} items, total: {len(all_messages)}")
        
        if len(all_messages) >= data.get('total', 0):
            break
        
        skip += limit
    
    print(f"\n✅ Total messages fetched: {len(all_messages)}")
    
    # analyze the data
    if all_messages:
        unique_users = set(msg.get('user_name') for msg in all_messages)
        print(f"👥 Unique users: {len(unique_users)}")
        print(f"📋 Users: {', '.join(sorted(unique_users)[:10])}{'...' if len(unique_users) > 10 else ''}")
        
        # check for any weird data
        missing_names = sum(1 for msg in all_messages if not msg.get('user_name'))
        missing_messages = sum(1 for msg in all_messages if not msg.get('message'))
        
        if missing_names:
            print(f"⚠️  {missing_names} messages missing user_name")
        if missing_messages:
            print(f"⚠️  {missing_messages} messages missing message text")
    
    return all_messages

if __name__ == "__main__":
    # run the tests
    test_messages_endpoint()
    messages = test_full_fetch()
    
    print("\n" + "="*50)
    print("✨ Test complete! Ready to build the QA system.")