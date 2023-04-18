import requests

import os, json, dotenv

dotenv.load_dotenv()

data = {
        "to": os.getenv("User_ID"),
        "messages": [
            {
                "type": "text",
                "text": "功能測試喔x2~~~ by 軒"
            }
        ]
    }
headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("Channel_Access_Token")
    }
r = requests.post("https://api.line.me/v2/bot/message/push", data=json.dumps(data), headers=headers)

print(r)

