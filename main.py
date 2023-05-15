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
    today = datetime.datetime.now()
    date = today.strftime('%m/%d')
    print("!!! Active !!! date: ", date)
    text = ""
    url = f'https://api.wikimedia.org/feed/v1/wikipedia/zh/onthisday/selected/{date}'
    wiki_headers = {
        'Authorization': f'Bearer {WIKI_TOKEN}',
        'User-Agent': WIKI_MAIL
    }

    wiki_response = requests.get(url, headers=wiki_headers)
    if wiki_response.status_code != 200:
        print("Error! ->", wiki_response.status_code, wiki_response.text)
    response = wiki_response.json().get('selected')
    data_set = {"messages": []}
    nasa_data_set = {"messages": []}
    nasa_image_final_set = {"messages": []}
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
    nasa_image_set = None
    nasa_text_set = None
    if nasa_response.status_code == 200:
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
        # Finding ways to send image that can preview in Line =皿=
        nasa_image_set = {
            "type": "text",
            "text": f"(測試中)圖片請點這裡: {nasa_image}"
        }
        nasa_text_set = {
            "type": "text",
            "text": translated_text
        }
        nasa_data_set["messages"].append(nasa_text_set)
        nasa_image_final_set["messages"].append(nasa_image_set)
    print("all data set...broadcasting to Line...")
    # Line broadcast section
    try:
        today_r = requester("today", today_date_info)
        r = requester("data", data_set)
        nasa_image_r = requester("nasa_image", nasa_image_final_set)
        nasa_r = requester("nasa_text", nasa_data_set)
        print(">>>>> Results:  ",today_r, r, nasa_image_r, nasa_r)
    except Exception as e:
        print("Error broadcasting message: ", e)


def requester(section,data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    response = requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(data), headers=headers)
    print(response)
    return {"status": response.status_code, "section": section}






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
    

# if __name__ == '__main__':
#     hello_pubsub(cloud_event=None)