from cgi import test
import os
from dotenv import load_dotenv
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

#new install
# pip install schedule

#new import
import requests
import schedule
from time import sleep
import pickle

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
    
# 定期実行 
# https://di-acc2.com/programming/python/4574/
# https://qiita.com/hiratarich/items/3e932b84b599762ed913
#メッセージ送信関連　https://note.com/npaka/n/n4bcb38a1ea74

# TOKEN = '<トークン>'
CHANNEL = 'murakami' # 　ここに送るチャンネル名を書く
TOKEN = str(os.environ.get("SLACK_BOT_TOKEN"))
url = "https://slack.com/api/chat.postMessage"
headers = {"Authorization": "Bearer "+TOKEN}
data  = {
   'channel': CHANNEL,
   'text': 'テストです。'
}
# r = requests.post(url, headers=headers, data=data)
# print("return ", r.json())
def send(message):
  data["text"] = message
  r = requests.post(url, headers=headers, data=data)
  # print("return ", r.json())


def test():
  text = "task message test"
  send(text)


# スケジュール登録
with open('remindDates.pickle', mode='rb') as f:
    remindDates = pickle.load(f)
for date in remindDates:
  schedule.every().day.at(date).do(test).tag(date)


# イベント実行
while True:
    schedule.run_pending()
    sleep(50)

SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()