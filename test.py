
import os
import requests
import json
import dotenv
import openai
import datetime

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
NASA_API_KEY = os.getenv('NASA_API_KEY')
openai.api_key = os.getenv('OPEN_AI_API_KEY')

# import datetime
# # import requests

# today = datetime.datetime.now()
# date = today.strftime('%m/%d')

# print(f"抓取{date}的資料")

# url = f'https://api.wikimedia.org/feed/v1/wikipedia/zh/onthisday/selected/{date}'

# headers = {
#   'Authorization': f'Bearer {WIKI_TOKEN}',
#   'User-Agent': WIKI_MAIL
# }
# response = requests.get(url, headers=headers)
# if response.status_code != 200:
#     print("Error broadcasting message: ", response.status_code, response.text)

# data = response.json().get('selected')

# with open('origin_data.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

# data_set = {"messages": []}

# for i in data:
#     message = i['text']
#     year = i['pages'][0]['title']
#     more_info = i['pages'][1]['content_urls']['mobile']['page']
#     image = ""
#     # check if image exists
#     # try:
#     #     image = i['pages'][1]['thumbnail']['source']
#     # except:
#     #     print("image not exists")
#     text = f"{year}{message}\n\n看更多:{more_info}"
#     data_set["messages"].append({
#         "type": "text",
#         "text": text
#     })

# today_date_info = {"messages": [
#     {
#         "type": "text",
#         "text": f"歷史上的今天 for {date}"
#     }
# ]}

# print(today_date_info,data_set)

# ### >>>This is the final data set that will be sent to Line API<<< ###
# with open('test.json', 'w', encoding='utf-8') as f:
#     json.dump(data_set, f, ensure_ascii=False, indent=4)



# # NASA API
# url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}'
# response = requests.get(url)
# if response.status_code == 200:
#     print("success")
#     data = response.json()
#     print(data)
#     comments = data['explanation']
#     image = data['url']
#     translate_result = openai.Completion.create(
#         model = "text-davinci-003",
#         prompt = f"Translate this to Triditional Chinese: \n\n{comments}\n\n",
#         temperature = 0.7,
#         max_tokens = 3000
#         )
#     translated_comments = translate_result['choices'][0]['text'].encode('utf-8').decode('utf-8')
#     print(translated_comments)


# else:
#     print("fail")


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
    print("Error broadcasting message: ", wiki_response.status_code, wiki_response.text)
else:
    print("Message broadcasted successfully!")