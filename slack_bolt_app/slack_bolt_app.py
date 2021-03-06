import os
from dotenv import load_dotenv
import json
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from googlesearch import search
import datetime
import re

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

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

dt_now = datetime.datetime.now()

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
    respond(f"<@{command['user_id']}>  ?????????( {weather_place} )????????????????????? {weather_speak} ?????????")

#add by tawara
@app.command("/google")
def repeat_text(ack, respond, command):
    ack()
    userInput =command['text']
    if userInput == "":
        respond("/google ????????????(|??????)????????????????????????????????????")
    else:
        if '|' in userInput:
            userInputArray = userInput.split('|')
            searchCount = int(userInputArray[1])
            searchQuery = userInputArray[0].replace('"', '\"')
            respond("?????????....")
        else:
            searchCount = 1
            searchQuery = userInput
            respond("?????????....")
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
          respond(''.join(str_list)+"?????????????????????????????????OK?????????")
          break

# add by takeda
@app.message("factorization")
def message_fact(message, say):
    msg = re.findall(r'-?[0-9]+', message['text'])
    if len(msg) == 0:
      say('No natural number found')
    elif len(msg) > 1:
      say('Enter only one natural number')
    else:
      num = int(msg[0])
      if num <= 0:
        say("Enter a natural number")
        return
      if num == 1:
        say("1 is not prime")
        return
    rt ,cnt= fact(num)
    ret = ''
    prime = False

    if len(rt) == 1:
        for i in rt.keys():
            if rt[i] == 1:
                prime = True
    for i ,j in rt.items():
            if j == 1:
                ret = ret + str(i)
            elif j > 1:
                ret = ret + str(i) + '^' + str(j)
            cnt -= 1
            if cnt > 0:
                ret += ' * '
            if cnt == 0:
                break
    if prime:
        say(ret + " is prime")
    else:
      say(str(num) + ' = ' + ret)

def fact(num):
    count = 0
    temp = num
    rtlist = {}
    prime = False
    while(not prime):
        for i in range(2,temp+1):
            if i * i > temp:
                prime = True
                if not str(temp) in rtlist:
                    count += 1
                    rtlist.update({str(temp) : 1})
                else:
                  rtlist.update({str(temp) : rtlist[str(temp)] + 1})
                break
            elif temp % i == 0:
                if not str(i) in rtlist:
                    rtlist.update({str(i) : 1})
                    count += 1
                else:
                  rtlist.update({str(i) : rtlist[str(i)] + 1})
                temp = temp // i
                break
    return(rtlist, count)


@app.command("/item")
def command_item(command):
    item=command["text"]


    @app.message("??????????????????????????????")
    def message_yes(say):
        say(f"??????{item}???????????????")

    @app.message("??????")
    def message_yes(say):
      say(f"??????{item}???????????????")

@app.command("/start")
def command_start(say,command):
    start =command['text']
    say(f"{start}????????????????????????????????????????????????????????????????????????????????????????????????")

def fizzbuzz(num):
  if num % 15 == 0:
    return 'FizzBuzz'
  elif num % 5 == 0:
    return 'Buzz'
  elif num % 3 == 0:
    return 'Fizz'
  else:
    return str(num)

@app.message("??????")
def message_weather(message, say):
  request_data = requests.get("https://www.jma.go.jp/bosai/forecast/data/forecast/260000.json").json()
  wfdata = request_data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
  wfdataf = "???????????????????????????"+wfdata+"????????? "
  say(wfdataf)

#add by tawara
def weather_get():
    weather_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/260000.json"
    weather_json = requests.get(weather_url).json()
    weather_place = weather_json[0]["timeSeries"][0]["areas"][0]["area"]["name"]
    weather_full = weather_json[0]["timeSeries"][0]["areas"][0]["weathers"][0]
    return weather_place, weather_full


SocketModeHandler(app,os.environ["SLACK_APP_TOKEN"]).start()
