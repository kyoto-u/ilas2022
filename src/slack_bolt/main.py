from cgi import test
import os
from dotenv import load_dotenv
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import datetime # https://note.nkmk.me/python-datetime-now-today/
import requests
from time import sleep
import subprocess
import pickle

load_dotenv()

# reiminderについて
# https://qiita.com/melka-blue/items/03cc2d7c68b7cfdbd110
# https://dlrecord.hatenablog.com/entry/2020/07/13/214241
# https://hashikake.com/subprocess

# subprocessとしてremind.pyを起動
reminder = subprocess.Popen(["python", "remind.py"])

is_file = os.path.isfile('remindDates.pickle')
if is_file:
  with open('remindDates.pickle', 'rb') as f:
    remindDates = pickle.load(f)
else:
  remindDates = [] # remindする時刻のリスト
with open('remindDates.pickle', mode='wb') as f:
  pickle.dump(remindDates, f)

# setReminder,cancelReminderでは、app.pyでremindDatesの再設定を行い、reminder.pyを再起動(remind.pyに変更を反映させるため)

# remindする時刻を追加
def setReminder(date, userid):
  global reminder
  global remindDates
# remind1時刻設定
  remindDates.append(date)
  remindDates = sorted(remindDates)
  with open('remindDates'+str(userid)+'.pickle', mode='wb') as f:
    pickle.dump(remindDates, f)
# reminderが起動しているかどうか(起動していたら再起動、起動していなかったら、データの保存のみ)
  flag = True
  if reminder.poll() is None:
    flag = True
  elif reminder.poll() == 1:
    flag = False  
  if flag:
    reminder.kill()
    sleep(3) # reminderを終了する時間
    reminder = subprocess.Popen(["python", "remind.py"])

# remindする時刻を削除
def cancelReminder(date):
  global reminder

  #remind時刻設定
  remindDates.remove(date)
  with open('remindDates.pickle', mode='wb') as f:
    pickle.dump(remindDates, f)

# reminderが起動しているかどうか(起動していたら再起動、起動していなかったら、データの保存のみ)
  flag = True
  if reminder.poll() is None:
    flag = True
  elif reminder.poll() == 1:
    flag = False
  if flag:
    reminder.kill()
    sleep(3) # reminderを終了する時間
    reminder = subprocess.Popen(["python", "remind.py"])


def timeJugde(s): # 文字列sが時刻かどうか判定
  if ":" not in s:
    return False
  else:
    s = s.replace(":", "")
    if s.isdigit(): # sが数字ならTrue
        if len(s) == 4:
            n = int(s[0:2])
            m = int(s[2:4])
            if n >= 0 and n <= 23 and m >= 0 and m <= 59:
             return True
            else:
                return False
        else:
            return False
    else:
      return False

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# remind関連

# コマンドでremind追加 ex.  /setRemind 07:30
@app.command("/set")
def command_set(ack, respond, command):
  ack()
  reminderTime = command['text']
  if timeJugde(reminderTime):
    if reminderTime in remindDates:
      respond("すでに" + reminderTime + "にはタスクの表示が設定されています")
    else:
      setReminder(reminderTime)
      respond("毎日" + reminderTime + "にタスクを表示するように設定しました")
  else:
    respond("「" + reminderTime + "」は時刻として適切ではありません")

# コマンドでremind削除 ex.  /cancelRemind 07:30
@app.command("/cancel")
def command_cancel(ack, respond, command):
  ack()
  reminderTime = command['text']
  if timeJugde(reminderTime):
    if reminderTime in remindDates:
      cancelReminder(reminderTime)
      respond(reminderTime + "のタスクの表示を取り消しました")
    else:
      respond(reminderTime + "にはタスクの表示は登録されていません")
  else:
    respond("「" + reminderTime + "」は時刻として適切ではありません")

# 現在登録しているremindを確認する
@app.command("/list")
def command_list(ack, respond, command):
  ack()
  l = ",".join(remindDates)
  respond("現在予定しているリマインド時刻は" + l + "です")

# remind.pyを終了
@app.message("stop")
def stop(message, say):
  if reminder.poll() is None:
    reminder.kill()
    say("Reminderを止めました")
  elif reminder.poll() == 1:
    say("Reminderは動いていません")

# remind.pyを起動
@app.message("start")
def start(message, say):
  global reminder
  if reminder.poll() is None:
    say("Reminderは既に動いています")
  elif reminder.poll() == 1:
    reminder = subprocess.Popen(["python", "remind.py"])
    say("Reminderを開始しました")




SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
