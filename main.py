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

    response = wiki_response.json().get('selected')
    if wiki_response.status_code != 200:
        print("Error broadcasting message: ", wiki_response.status_code, wiki_response.text)
    # put all i["text"] together and break lines
    for i in response:
        text += i["pages"][0]["title"] + i["text"] + "\n" + "\n"
    data = {
        "messages": [
            {
                "type": "text",
                "text": f"歷史上的今天 for {date}"
            },
            {
                "type": "text",
                "text": text
            }
        ]
    }


    # Line broadcast section
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    r = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        print("Line message broadcast successfully")
        print(r)
    else:
        print("Error broadcasting message: ", r.status_code, r.text)



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
    