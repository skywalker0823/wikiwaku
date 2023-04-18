
import os
import requests
import json
import dotenv

dotenv.load_dotenv()

# data = {
#     "messages": [
#         {
#             "type": "text",
#             "text": "Cloud Run 功能上線測試 by 軒"
#         }
#     ]
# }

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Bearer " + os.getenv("Channel_Access_Token")
# }

# response = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(data), headers=headers)

# if response.status_code != 200:
#     print("Error broadcasting message: ", response.status_code, response.text)
# else:
#     print("Message broadcasted successfully!")


import datetime
# import requests

today = datetime.datetime.now()
date = today.strftime('%m/%d')

print(f"抓取{date}的資料")

url = 'https://api.wikimedia.org/feed/v1/wikipedia/zh/onthisday/selected/' + date

headers = {
  'Authorization': 'Bearer '+ os.getenv('Wiki_token'),
  'User-Agent': os.getenv('My_mail')
}

response = requests.get(url, headers=headers)
data = response.json().get('selected')
text = ""
if response.status_code != 200:
    print("Error broadcasting message: ", response.status_code, response.text)

for i in data:
    text += i["pages"][0]["title"] + i["text"] + "\n" + "\n"

print(text)

data = {
    "messages": [
        {
            "type": "text",
            "text": "歷史上的今天: " + date
        },
        {
            "type": "text",
            "text": text
        }
    ]
}


# print(data)
    


