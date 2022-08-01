import curses
import os
from dotenv import load_dotenv
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import pickle
import pprint
import datetime
load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

#kugiの作成箇所
@app.command("/register")
def register(ack, respond, command, user_id):
    ack()
    is_file=os.path.isfile("userid_dict.pickle")#ファイルの存在確認
    if (is_file==False):
        userid_dict={}
        with open('userid_dict.pickle', mode='wb') as f:    #userid_dictを保存
            pickle.dump(userid_dict, f)
    else:
        panda_id=command["text"]
        with open("userid_dict.pickle", 'rb') as pickle_file:
            userid_dict = pickle.load(pickle_file)
        if (user_id in userid_dict ==False):
            userid_dict[user_id]=panda_id           #slack_idとpanda_idを紐づける
            with open('userid_dict.pickle', mode='wb') as f:    #userid_dictを上書き保存
                pickle.dump(userid_dict, f)
            respond("SlackIDとPandAIDの紐づけに成功しました")
        else:
            dict_add={user_id:panda_id}
            userid_dict.update(dict_add)
            with open('userid_dict.pickle', mode='wb') as f:    #userid_dictを上書き保存
                pickle.dump(userid_dict, f)
            respond("PandAIDを更新しました。")

#作成箇所終わり

#という情報が保存されているという前提で

@app.command("/show")
def show(ack, respond, command, user_id):
    ack()
    #SLACKで課題を一覧表示
    #userid_dictを上書き保存
    is_file=os.path.isfile("userid_dict.pickle")#ファイルの存在確認
    if (is_file==False):
        respond("PandAIDが存在しません。/register コマンドで登録してください。")
    else:
        with open("userid_dict.pickle", 'rb') as pickle_file:
            userid_dict = pickle.load(pickle_file)
        if (userid_dict[user_id]==None):
            respond("PandAIDが存在しません。/register コマンドで登録してください。")
        else:
            panda_id=userid_dict[user_id]
            is_file=os.path.isfile('datas_panda_'+str(panda_id)+'.pickle')#ファイルの存在確認
            if (is_file==False):
                respond("まだ課題データが届いていません。拡張機能をインストールしたブラウザでSakaiを開いてください。")
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
                    respond(kadai_no_itiran)
            #これで[{course:法学入門, title:演習問題１, 2/30まで｝
            #      {course:水理学入門, title:計算問題１, 4/30まで｝...と表示されるはず]
        

  # PandaAssignment = {
  #              "course" : inf["course"]["name"], # 授業名
  #              "title" : inf["entries"][0]["title"], # 課題名]
  #              "dueTime" : inf["entries"][0]["dueTime"], # 締切日時
   #             "closeTime" : inf["entries"][0]["closeTime"], # 遅延提出期限日
   #             "hasFinished" : inf["entries"][0]["hasFinished"], # 終わったかどうか(bool値)
  #              "isRead" : inf["isRead"] # 何に使うかは7/4現在不明(bool値)
  #          }
        
 #データ型を日本語に直す

 #   @app.command("/task")     
 #   def todo(ack, respond, command, respond):
 #       ack()
 #       respond(usedInfList)

SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
