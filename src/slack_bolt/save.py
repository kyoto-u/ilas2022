#!/usr/bin/python3
import os
from dotenv import load_dotenv
import pickle
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import datetime

#    usedInf = {
#        "course" : inf["course"]["name"], # 授業名
#        "title" : inf["entries"][0]["title"], # 課題名]
#        "dueTime" : inf["entries"][0]["dueTime"], # 締切日時
#        "closeTime" : inf["entries"][0]["closeTime"], # 遅延提出期限日
#        "hasFinished" : inf["entries"][0]["hasFinished"], # 終わったかどうか(bool値)
#        "isRead" : inf["isRead"] # 何に使うかは7/4現在不明(bool値)
#    }
userid_dict={}

load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.command("/task")
def todo(ack, respond, command):
    ack()
    userInput = command['text'].split()
    userid = str(command['user_id'])

    if userInput == []:
        # registerの辞書からuseridに対応するpandaのidを取得してきます
        # pandaのidを用いてusedInf のタスクの中身を持ってきます
        # for分でタスクと日付を一つずつ取り出して文字列に
        respond(文字列)


SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()