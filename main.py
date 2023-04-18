import base64
import functions_framework
from fastapi import FastAPI, Request
import requests, json, dotenv, os

dotenv.load_dotenv()

app = FastAPI()

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    # Print out the data from Pub/Sub, to prove that it worked
    print("!!! Active !!!")
    print("Sending Line update message")
    data = {
        "messages": [
            {
                "type": "text",
                "text": "GCP+Broadcast 功能測試 by 軒"
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("Channel_Access_Token")
    }
    r = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(data), headers=headers)
    if r.status_code == 200:
        print("Line message broadcast successfully")
        print(r)
    else:
        print("Error broadcasting message: ", r.status_code, r.text)

# Line webhook response ok
@app.post("/callback")
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
    