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
    
#add by tawara
@app.command("/weather")
def return_weather(ack, respond, command):
    ack()
    weather_place = weather_get()[0]
    weather_speak = weather_get()[1]
    respond(f"<@{command['user_id']}>  京都府( {weather_place} )の今日の天気は {weather_speak} です。")

#add by tawara
@app.command("/google")
def repeat_text(ack, respond, command):
    ack()
    userInput =command['text']
    if userInput == "":
        respond("/google 検索語句(|個数)の形式で入力してください")
    else:
        if '|' in userInput:
            userInputArray = userInput.split('|')
            searchCount = int(userInputArray[1])
            searchQuery = userInputArray[0].replace('"', '\"')
        else:
            searchCount = 1
            searchQuery = userInput
            respond("検索中....")
            count=0
        for url in search(searchQuery, lang="jp", num=searchCount):
            respond(url)
            count += 1
            if (count == searchCount):
                break

#add by tawara                
@app.command("/demachi")
def repeat_text(ack, respond, command):
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
