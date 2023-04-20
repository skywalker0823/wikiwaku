
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

WIKI_TOKEN = os.getenv('Wiki_token')
WIKI_MAIL = os.getenv('My_mail')
CHANNEL_ACCESS_TOKEN = os.getenv('Channel_Access_Token')

import datetime
# import requests

today = datetime.datetime.now()
date = today.strftime('%m/%d')

print(f"抓取{date}的資料")

url = f'https://api.wikimedia.org/feed/v1/wikipedia/zh/onthisday/selected/{date}'

headers = {
  'Authorization': f'Bearer {WIKI_TOKEN}',
  'User-Agent': WIKI_MAIL
}
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Error broadcasting message: ", response.status_code, response.text)

data = response.json().get('selected')

with open('origin_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

data_set = {"messages": []}

for i in data:
    message = i['text']
    year = i['pages'][0]['title']
    more_info = i['pages'][1]['content_urls']['mobile']['page']
    image = ""
    # check if image exists
    try:
        image = i['pages'][1]['thumbnail']['source']
    except:
        print("image not exists")
    text = f"{year}{message}\n\n看更多:{more_info}\n{image}"
    data_set["messages"].append({
        "type": "text",
        "text": text
    })

today_date_info = {"messages": [
    {
        "type": "text",
        "text": f"歷史上的今天 for {date}"
    }
]}

print(today_date_info,data_set)

### >>>This is the final data set that will be sent to Line API<<< ###
with open('test.json', 'w', encoding='utf-8') as f:
    json.dump(data_set, f, ensure_ascii=False, indent=4)


