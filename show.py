import os
from dotenv import load_dotenv
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import pickle
load_dotenv()

app = App(token=os.environ.get("REPORT1_BOT_TOKEN"))

#kugiの作成箇所
@app.command("/register")
def register(ack, say, command, user_id):
    ack()
    panda_id=command["text"]
    userid_dict=pickle.load("userid_dict.pickle")
    if (user_id in userid_dict ==False):
        userid_dict[user_id]=panda_id           #slack_idとpanda_idを紐づける
        with open('userid_dict.pickle', mode='wb') as f:    #userid_dictを上書き保存
            pickle.dump(userid_dict, f)
        say("SlackIDとPandAIDの紐づけに成功しました")
    else:
        dict_add={user_id:panda_id}
        userid_dict.update(dict_add)
        with open('userid_dict.pickle', mode='wb') as f:    #userid_dictを上書き保存
            pickle.dump(userid_dict, f)
        say("PandAIDを更新しました。")
#作成箇所終わり

#という情報が保存されているという前提で

@app.command("/show")
def show(ack, respond, command, user_id):
    ack()
    #SLACKで課題を一覧表示
     #userid_dictを上書き保存
    userid_dict=pickle.load("userid_dict.pickle")
    panda_id=userid_dict[user_id]
    with open('datas_panda_'+str(panda_id)+'.pickle', mode='r') as f:
     kadai_no_itiran = f
     respond(kadai_no_itiran)

        
 #データ型を日本語に直す

 #   @app.command("/task")     
 #   def todo(ack, respond, command, say):
 #       ack()
 #       respond(usedInfList)

SocketModeHandler(app,os.environ["REPORT1_APP_TOKEN"]).start()

