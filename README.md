# Auto grep wikipedia history of today, and send to line.



## GCP api used
* Cloud Scheduler
 - Used to schedule the task, activate pub/sub every day at 09:00
* Cloud Functions
 - Use gen-2, and the underlying is Cloud Run
* Cloud Pub/Sub
 - Used to trigger cloud function
* Cloud Secret Manager
 - Used to store the line token

* Line webhook

這個project的目的是要抓取wikipedia的每日歷史，並且發送到line上
1. Code commit 到 Github
2. 觸發 Cloud Build
3. CloudBuild 部署到 CLoud Function (Gen-2, 底層是 Cloud Run)
4. Cloud Scheduler 每天 09:00 觸發 Cloud Pub/Sub
5. Cloud Pub/Sub 觸發 Cloud Function 並且抓取 wikipedia 的每日歷史
6. Cloud Function 透過 Line webhook 發送到 Line

