# Auto grep wikipedia history of today, and send to line.
## GCP api used
* Cloud Scheduler
Used to schedule the task, activate pub/sub every day at 09:00
* Cloud Functions
Main function
* Cloud Pub/Sub
Used to trigger cloud function
* Cloud Secret Manager
Used to store the line token

* Line webhook


