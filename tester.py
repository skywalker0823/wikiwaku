
import os
import requests
import json
import dotenv
import openai
import datetime

dotenv.load_dotenv()

# WIKI_TOKEN = os.getenv('Wiki_token')
# WIKI_MAIL = os.getenv('My_mail')
# NASA_API_KEY = os.getenv('NASA_API_KEY')
# openai.api_key = os.getenv('OPEN_AI_API_KEY')

# 發送到測試群組
CHANNEL_ACCESS_TOKEN = os.getenv('Test_Access_Token')

data = {
    "messages": [
        {
            "type": "text",
            "text": "測試"
        }
    ]
}


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
}

response = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(data), headers=headers)

if response.status_code != 200:
    print("Error broadcasting message: ", response.status_code, response.text)
else:
    print("Message broadcasted successfully!")
    
