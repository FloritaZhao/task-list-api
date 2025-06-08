import os
import requests

def notify_task_complete(task):
    slack_token = os.environ.get("SLACK_TOKEN")
    channel = os.environ.get("SLACK_CHANNEL", "#test-slack-api")
    text = f"Flora just completed the task *{task.title}*"

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": f"Bearer {slack_token}"},
        json={"channel": channel, "text": text}
    )

    if not response.ok or response.json().get("ok") is not True:
        print("Slack notification failed:", response.text)