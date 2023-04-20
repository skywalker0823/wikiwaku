import base64
import functions_framework
from fastapi import FastAPI, Request
import requests, json, dotenv, os, datetime

dotenv.load_dotenv()

app = FastAPI()

WIKI_TOKEN = os.getenv('Wiki_token')
WIKI_MAIL = os.getenv('My_mail')
CHANNEL_ACCESS_TOKEN = os.getenv('Channel_Access_Token')


# Wiki API section
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    print("!!! Active !!!")
    today = datetime.datetime.now()
    date = today.strftime('%m/%d')
    text = ""
    url = f'https://api.wikimedia.org/feed/v1/wikipedia/zh/onthisday/selected/{date}'
    wiki_headers = {
        'Authorization': f'Bearer {WIKI_TOKEN}',
        'User-Agent': WIKI_MAIL
    }
    wiki_response = requests.get(url, headers=wiki_headers)
    if wiki_response.status_code != 200:
        print("Error broadcasting message: ", wiki_response.status_code, wiki_response.text)
    
    response = wiki_response.json().get('selected')

    data_set = {"messages": []}
    for i in response:
        # text += i["pages"][0]["title"] + i["text"] + "\n" + "\n"
        year = i['pages'][0]['title']
        message = i['text']
        more_info = i['pages'][1]['content_urls']['mobile']['page']
        # image = ""
        # # check if image exists
        # try:
        #     image = i['pages'][1]['thumbnail']['source']
        # except:
        #     print("image not exists")
        text = f"{year}{message}\n\n看更多:{more_info}"
        # put text into data messages
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

    # Line broadcast section
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    today_r = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(today_date_info), headers=headers)
    r = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(data_set), headers=headers)
    if r.status_code == 200 and today_r.status_code == 200:
        print("Line message broadcast successfully")
        print(r)
    else:
        print("Error broadcasting message: ", r.status_code, r.text, today_r.status_code, today_r.text)


# Line message example json
# {
#     "messages": [
#         {
#             "type": "text",
#             "text": "1999年埃里克·哈里斯和迪倫·克萊伯德在美國科羅拉多州高中發動槍擊事件，造成13人死亡。"
#         },
#         {
#             "type": "text",
#             "text": "1978年大韓航空902號班機因為誤入蘇聯領空而遭到蘇聯空軍的攻擊，被迫在州緊急降落。"
#         },
#         {
#             "type": "text",
#             "text": "1862年法國微生物學家（圖）和生理學家克洛德·貝爾納完成首次的殺菌測試。"
#         },
#         {
#             "type": "text",
#             "text": "1792年法國將軍夏爾·弗朗索瓦·迪穆里埃促成國民立法議會向奧地利宣戰，法國大革命戰爭爆發。"
#         },
#         {
#             "type": "text",
#             "text": "1653年英格蘭共和國軍事將領奧立佛·克倫威爾發動政變並解散殘缺議會，其後以小議會取代。"
#         }
#     ]
# }



# Line webhook response ok
@app.post("/")
async def line_webhook(request: Request):
    if request.method == 'POST':
        data = request.get_json()
        events = data['events']
        for event in events:
            event_type = event['type']
            if event_type == 'message':
                message_text = event['message']['text']
                print('User sent message:', message_text)
        return 'OK'
    else:
        print('Webhook error')
        return 'Webhook error'
    