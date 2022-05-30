import os
from dotenv import load_dotenv
import json
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

