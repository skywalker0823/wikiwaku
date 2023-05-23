# Greps wikipedia history of today and NSAS APOD every morning, and broadcast to Line messenger.
## Hosted on Google Cloud Platform with fully automated CI/CD pipeline

<img width="1117" alt="截圖 2023-05-23 上午11 34 26" src="https://github.com/skywalker0823/wikiwaku/assets/56625237/17abd8f3-e30e-4474-850d-16f34ad34735">


<img src="https://github.com/skywalker0823/wikiwaku/assets/56625237/dbe01c01-c0c6-49fd-8312-8e871a960bfb" alt="IMG_3558" width="300">
<img src="https://github.com/skywalker0823/wikiwaku/assets/56625237/99a3fbfb-4ac8-4ee9-acd2-29b9a64f256d" alt="IMG_3557" width="300">



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
- 3. 把Nasa原文資料藉由OpenAI API翻譯成中文
- 4. 把以上資料整理成Line的格式 then GO~ 

# 未來功能
* 提升互動性(webhook), 星座 或是每日推薦, 山岳資料, 串接公開平台api
* chatGPT 基本功能
