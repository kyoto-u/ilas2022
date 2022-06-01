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
  dt_now = str(datetime.datetime.now())
  timecell=(534, 554, 614, 629, 639, 651,700,712,724,736,748,802,812,822,836,848,900,915,930,945,1000,1015,1030,1045,1100,1115,1130,1145,1200,1215,1230,1245,1300,1315,1330,1345,1400,1415,1430,1445,1500,1507,1515,1530,1545,1600,1607,1615,1630,1645,1700,1712,1724,1736,1748,1800,1812,1824,1836,1848,1900,1915,1930,1945,2000,2015,2030,2045,2104,2127,2149,2204,2225,2250,2316,2333)
  nowtime = int(dt_now[11:16].replace(":",""))
  for i in timecell:
      if i-nowtime >0:
          str_list = list(str(i))
          str_list.insert(-2,":")
          respond(''.join(str_list)+"までに京都大学を出ればOKです！")
          break

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
      
#add by tawara
def weather_get():
    weather_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/260000.json"
    weather_json = requests.get(weather_url).json()
    weather_place = weather_json[0]["timeSeries"][0]["areas"][0]["area"]["name"]
    weather_full = weather_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
    return weather_place, weather_full

SocketModeHandler(app,os.environ["SLACK_APP_TOKEN"]).start()
