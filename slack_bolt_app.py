import os
from dotenv import load_dotenv
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
from googlesearch import search
import datetime

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message("hi")
def message_hi(message, say):
    say(f"Hi!!")

@app.message("hello")
def message_hello(message, respond):
    respond(f"Hey there <@{message['user']}>!")

@app.event("app_mention")
def event_mention(event, respond):
    print("event_mention: ", json.dumps(event, indent=2))

@app.command("/fizzbuzz_tawara")
def command_fizzbuzz(ack, respond, command):
    ack()
    try:
        num = int(command['text'])
        ans = fizzbuzz(num)
        respond(f"<@{command['user_id']}> {ans}")
    except ValueError:
        respond(f"<@{command['user_id']}> Invalid Number")

@app.command("/weather")
def return_weather(ack, respond, command):
    ack()
    weather_place = weather_get()[0]
    weather_speak = weather_get()[1]
    respond(f"<@{command['user_id']}>  京都府( {weather_place} )の今日の天気は {weather_speak} です。")

@app.command("/google")
def repeat_text(ack, respond, command):
    ack()
    userInput =command['text']
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

@app.command("/demachi")
def repeat_text(ack, respond, command):
  ack()
  dt_now = str(datetime.datetime.now())
  timecell=(546, 566, 626, 651, 712, 736, 760, 824, 848, 912, 927, 942, 957, 1012, 1027, 1042, 1057, 1112, 1127, 1142, 1157, 1212, 1227, 1242, 1257, 1312, 1327, 1342, 1357, 1412, 1427, 1442, 1457, 1512, 1527, 1542, 1557, 1612, 1627, 1642, 1657, 1712, 1736, 1760, 1824, 1848, 1912, 1942, 2012, 2042, 2116, 2161, 2237)
  nowtime = int(dt_now[11:16].replace(":",""))
  for i in timecell:
      if i-nowtime >0:
          str_list = list(str(i))
          str_list.insert(-2,":")
          respond(''.join(str_list)+"までに京都大学を出ればOKです！")
          break

def fizzbuzz(num):
    if num % 15 == 0:
        return 'FizzBuzz'
    elif num % 5 == 0:
        return 'Buzz'
    elif num % 3 == 0:
        return 'Fizz'
    else:
        return str(num)

def weather_get():
    weather_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/260000.json"
    weather_json = requests.get(weather_url).json()
    weather_place = weather_json[0]["timeSeries"][0]["areas"][0]["area"]["name"]
    weather_full = weather_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
    return weather_place, weather_full

SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
