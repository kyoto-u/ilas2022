from cgi import test
import os
from dotenv import load_dotenv
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import datetime # https://note.nkmk.me/python-datetime-now-today/

#new install
# pip install schedule

# #new import
import requests
import schedule
from time import sleep

    



# # 定期実行 https://di-acc2.com/programming/python/4574/

load_dotenv()


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
  print("return ", r.json())

n = 1

def test():
  global n
  text = str(n) + "回目の実行（テスト）"
  send(text)
  n += 1


#02 スケジュール登録
schedule.every().day.at("6:00").do(test)


#03 イベント実行
while True:
    schedule.run_pending()
    sleep(60)




def what_time(t):
  hour = t.hour
  if hour >= 3 and hour < 11:
    return "morning"
  elif hour >= 11 and hour < 18:
    return "noon"
  else:
    return "night"

def greet_word(time):
    if time == "morning":
      return "Good morning"
    elif time == "noon":
      return "Good afternoon"
    elif time == "night":
      return "Good evening"



app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
dt_now = datetime.datetime.now()



@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")

@app.message("good morning")
def good_morning(message, say):
    now_time = what_time(dt_now)
    greetword = greet_word(now_time)
    say(greetword + f" <@{message['user']}>!")
    if now_time != "morning":
      say("It is not morning. It is " + now_time + ".")

@app.message("good afternoon")
def good_morning(message, say):
    now_time = what_time(dt_now)
    greetword = greet_word(now_time)
    say(greetword + f" <@{message['user']}>!")
    if now_time != "noon":
      say("It is not noon. It is " + now_time + ".")

@app.message("good evening")
def good_morning(message, say):
    now_time = what_time(dt_now)
    greetword = greet_word(now_time)
    say(greetword + f" <@{message['user']}>!")
    if now_time != "night":
      say("It is not night. It is " + now_time + ".")


@app.event("app_mention")
def event_mention(event, say):
   print("event_mention: ", json.dumps(event, indent=2))

@app.command("/fizzbuzzmurakami")
def command_fizzbuzz(ack, respond, command):
  ack()
  try:
    num = int(command['text'])
    ans = fizzbuzz(num)
    respond(f"<@{command['user_id']}> {ans}")
  except ValueError:
    respond(f"<@{command['user_id']}> Invalid Number")

def fizzbuzz(num):
  if num % 15 == 0:
    return 'FizzBuzz'
  elif num % 5 == 0:
    return 'Buzz'
  elif num % 3 == 0:
    return 'Fizz'
  else:
    return str(num)

SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
