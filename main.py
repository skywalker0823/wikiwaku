import base64, functions_framework, openai, requests, json, dotenv, os, datetime
from fastapi import FastAPI, Request

dotenv.load_dotenv()

app = FastAPI()

WIKI_TOKEN = os.getenv('Wiki_token')
WIKI_MAIL = os.getenv('My_mail')
CHANNEL_ACCESS_TOKEN = os.getenv('Channel_Access_Token')
NASA_API_KEY = os.getenv('NASA_API_KEY')
openai.api_key = os.getenv('OPEN_AI_API_KEY')


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
        year = i['pages'][0]['title']
        message = i['text']
        more_info = i['pages'][1]['content_urls']['mobile']['page']
        text = f"{year}{message}\n\n看更多:{more_info}"
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


    # NASA API section
    nasa_url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}'
    nasa_response = requests.get(nasa_url)
    if nasa_response.status_code == 200:
        print("NASA API request successfully...continue")
        nasa_data = nasa_response.json()
        nasa_image = nasa_data['url']
        nasa_explanation = nasa_data['explanation']
        translate_response = openai.Completion.create(
            model = "text-davinci-003",
            prompt = f"Translate this to Triditional Chinese: \n\n{nasa_explanation}\n\n",
            temperature = 0.7,
            max_tokens = 3000
        )
        translated_text = translate_response['choices'][0]['text'].encode('utf-8').decode('utf-8')
        nasa_image_set = {
            "type": "image",
            "originalContentUrl": nasa_image,
            "previewImageUrl": nasa_image
        }
        nasa_text_set = {
            "type": "text",
            "text": translated_text
        }

    # Line broadcast section
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }

    today_r = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(today_date_info), headers=headers)
    r = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(data_set), headers=headers)
    nasa_image_r = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(nasa_image_set), headers=headers)
    nasa_r = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(nasa_text_set), headers=headers)
    if r.status_code == 200 and today_r.status_code == 200:
        print("Line message broadcast successfully")
        print(r)
    if nasa_image_r.status_code == 200 and nasa_r.status_code == 200:
        print("NASA message broadcast successfully")
        print(nasa_image_r, nasa_r)
    else:
        print("Error broadcasting message: ", r.status_code, r.text, today_r.status_code, today_r.text)










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
    