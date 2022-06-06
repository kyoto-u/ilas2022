import os
from dotenv import load_dotenv
import json
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("hi")
def message_hi(message, say):
    say(f"Hi!!")

@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")

@app.event("app_mention")
def event_mention(event, say):
   print("event_mention: ", json.dumps(event, indent=2)) 

@app.command("/fizzbuzz")
def command_fizzbuzz(ack, respond, command):
  ack()
  try:
    num = int(command['text'])
    ans = fizzbuzz(num)
    respond(f"<@{command['user_id']}> {ans}")
  except ValueError:
    respond(f"<@{command['user_id']}> Invalid Number")



@app.command("/item")
def command_item(command):
    item=command["text"]


    @app.message("うちのオカンによると")
    def message_yes(say):
        say(f"それ{item}やないかい")

    @app.message("でも")
    def message_yes(say):
      say(f"ほな{item}ちゃうかー")

@app.command("/start")
def command_start(say,command):
    start =command['text']
    say(f"{start}と楽単はいくらあっても困りませんからね～。ありがとうございます。")

def fizzbuzz(num):
  if num % 15 == 0:
    return 'FizzBuzz'
  elif num % 5 == 0:
    return 'Buzz'
  elif num % 3 == 0:
    return 'Fizz'
  else:
    return str(num)

@app.message("天気")
def message_weather(message, say):
  request_data = requests.get("https://www.jma.go.jp/bosai/forecast/data/forecast/260000.json").json()
  wfdata = request_data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
  wfdataf = "今日の京都の天気は"+wfdata+"です。 "
  say(wfdataf)


SocketModeHandler(app,os.environ["SLACK_APP_TOKEN"]).start()
