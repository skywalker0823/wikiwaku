# Greps wikipedia history of today every morning, and broadcast to Line messenger.
<img width="1037" alt="截圖 2023-04-20 上午10 36 52" src="https://user-images.githubusercontent.com/56625237/233243183-7c6d4a07-61bc-4038-9cd8-e2a5c5947e5f.png">



## Tech Stack
* Cloud Scheduler
 - Used to schedule the task, activate pub/sub every day at 09:00
* Cloud Functions
 - Use gen-2, and the underlying is Cloud Run
* Cloud Pub/Sub
 - Used to trigger cloud function
* Cloud Secret Manager
 - Used to store the line and wikipedia token
* Line webhook

這個project的目的是要抓取wikipedia的歷史上的今天，並且每日固定發送到 Line 上
1. Code commit 到 Github
2. 觸發 Cloud Build
3. CloudBuild 部署到 CLoud Function (Gen-2, 底層是 Cloud Run)
4. Cloud Scheduler 每天 09:00 觸發 Cloud Pub/Sub
5. Cloud Pub/Sub 觸發 Cloud Function 並且抓取 wikipedia 的每日歷史
6. Cloud Function 透過 Line webhook 發送到 Line


# 未來功能
* 提升互動性, 星座 或是每日推薦, 山岳資料, 串接公開平台api
* chatGPT 基本功能