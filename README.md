# Greps wikipedia history of today and NSAS APOD every morning, and broadcast to Line messenger.
<img width="1037" alt="截圖 2023-04-20 上午10 36 52" src="https://user-images.githubusercontent.com/56625237/233243183-7c6d4a07-61bc-4038-9cd8-e2a5c5947e5f.png">


![IMG_3558](https://github.com/skywalker0823/wikiwaku/assets/56625237/dbe01c01-c0c6-49fd-8312-8e871a960bfb)
![IMG_3557](https://github.com/skywalker0823/wikiwaku/assets/56625237/99a3fbfb-4ac8-4ee9-acd2-29b9a64f256d)


## Tech Stack
* Python
* Cloud Build
 - CICD
* Cloud Scheduler
 - Used to schedule the task, activate pub/sub every day at 09:00
* Cloud Functions
 - Use gen-2, and the underlying is Cloud Run
* Cloud Pub/Sub
 - Used to trigger cloud function
* Cloud Secret Manager
 - Used to store the line and wikipedia token
* Line webhook and Other APIs

## APIs
* Wikipedia API
 - https://api.wikimedia.org/wiki/API_reference/Feed/On_this_day
* Line Messaging API
 - https://developers.line.biz/en/docs/messaging-api/overview/
* OpenAI text-devinci-003 for translation
 - https://platform.openai.com/docs/api-reference

這個project的目的是要抓取wikipedia的歷史上的今天與Nasa每日一圖，並且每日固定發送到 Line 上
1. Code commit 到 Github
2. 觸發 Cloud Build
3. CloudBuild 部署到 CLoud Function (Gen-2, 底層是 Cloud Run)
4. Cloud Scheduler 每天 09:00 觸發 Cloud Pub/Sub
5. Cloud Pub/Sub 觸發 Cloud Function
- 1. 抓取歷史上的今天(可以指定zh, en, ja 等語言)
- 2. 抓Nasa每日一圖
- 3. 把Nasa資料藉由OpenAI API翻譯成中文
- 4. 把以上資料整理成Line的格式 then GO~ 

# 未來功能
* 提升互動性(webhook), 星座 或是每日推薦, 山岳資料, 串接公開平台api
* chatGPT 基本功能
