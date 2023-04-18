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

# Triggered from a message from line user post request
@app.post("/my-path")
async def hello_http(request: Request):
    print("!!! User-ask !!!")
    data = await request.json()
    print(data)

