from cgi import test
import os
from dotenv import load_dotenv
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
import schedule
from time import sleep
import pickle
import datetime

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
    
# 定期実行 
# https://di-acc2.com/programming/python/4574/
# https://qiita.com/hiratarich/items/3e932b84b599762ed913
#メッセージ送信関連　https://note.com/npaka/n/n4bcb38a1ea74

# TOKEN = '<トークン>'
CHANNEL = 'general' # 　ここに送るチャンネル名を書く
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


def test(user_id):
  is_file=os.path.isfile("userid_dict.pickle")#ファイルの存在確認
  if (is_file==False):
      send("PandAIDが存在しません。/register コマンドで登録してください。")
  else:
      with open("userid_dict.pickle", 'rb') as pickle_file:
          userid_dict = pickle.load(pickle_file)
      if (userid_dict[user_id]==None):
          send("PandAIDが存在しません。/register コマンドで登録してください。")
      else:
          panda_id=userid_dict[user_id]
          is_file=os.path.isfile('datas_panda_'+str(panda_id)+'.pickle')#ファイルの存在確認
          if (is_file==False):
              send("まだ課題データが届いていません。拡張機能をインストールしたブラウザでSakaiを開いてください。")
          else:
              with open('datas_panda_'+str(panda_id)+'.pickle', mode='rb') as f:
                  f=pickle.load(f)
                  kadai_no_itiran=""
                  n=1
                  f[1] = sorted(f[1], key=lambda x:x["dueTime"])
                  for i in f[1]:
                      kadai_no_itiran=kadai_no_itiran + str(n)+".　授業:"+i["course"]+"　　課題名:"+i["title"]+"　　期限日:"+str(datetime.datetime.fromtimestamp(i["dueTime"]))+"\n"
                      n+=1
                  if kadai_no_itiran =="":
                      kadai_no_itiran = "課題はありません"
                  send(kadai_no_itiran)
  


# スケジュール登録
with open('remindDates.pickle', mode='rb') as f:
    remindDates = pickle.load(f)
for mykey, myvalue in remindDates.items():
  for date in myvalue:
    schedule.every().day.at(date).do(test, mykey).tag(date)

# イベント実行
while True:
    schedule.run_pending()
    sleep(50)

SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()