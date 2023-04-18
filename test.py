
import os
import requests
import json
import dotenv

dotenv.load_dotenv()

data = {
    "messages": [
        {
            "type": "text",
            "text": "Cloud Run 功能上線測試 by 軒"
        }
    ]
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.getenv("Channel_Access_Token")
}

response = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(data), headers=headers)

if response.status_code != 200:
    print("Error broadcasting message: ", response.status_code, response.text)
else:
    print("Message broadcasted successfully!")

