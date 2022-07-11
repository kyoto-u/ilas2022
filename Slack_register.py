from gc import is_finalized
import os
from dotenv import load_dotenv
import pickle
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import datetime

load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

is_file=os.path.isfile("userid_dict.pickle")
if is_file:
    with open("userid_dict.pickle", "rb") as f:
        userid_dict=pickle.load(f)
else:
    userid_dict={}


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

