import base64
import functions_framework
from fastapi import FastAPI, Request

app = FastAPI()

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    # Print out the data from Pub/Sub, to prove that it worked
    print("!!! Active !!!")
    print("test 123")
    print(base64.b64decode(cloud_event.data["message"]["data"]))

# Triggered from a message from line user post request
@app.post("/my-path")
async def hello_http(request: Request):
    print("!!! User-ask !!!")
    data = await request.json()
    print(data)
