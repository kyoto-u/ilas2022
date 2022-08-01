from flask import Flask, request
import json
from html import entities
import pickle
import time


#def system_run内でSlack側の処理を記述
def system_run(infList):
    # 整形
    PandaAssignments = []
    PandaAssignment={}
    # usedInfListに必要な情報を追加していく
    for inf in infList[1]:
        for entries in inf["entries"]:
            if (time.time()<int(entries["dueTime"])and entries["hasFinished"]==False): #課題があり、かつ締め切りを過ぎていないとき
                PandaAssignment = {
                    "course" : inf["course"]["name"], # 授業名
                    "title" : entries["title"], # 課題名]
                    "dueTime" : entries["dueTime"], # 締切日時
                    "closeTime" : entries["closeTime"], # 遅延提出期限日
                    "hasFinished" : entries["hasFinished"], # 終わったかどうか(bool値)
                }
                PandaAssignments.append(PandaAssignment)
    
    usedInfList = [infList[0], PandaAssignments] # 保存するようの情報
    # 保存
    panda_id=infList[0]
    with open('datas_panda_'+str(panda_id)+'.pickle', mode='wb') as f:
        pickle.dump(usedInfList, f)
    print(usedInfList)


#以下、Flask関連の処理
app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/', methods=["POST"])
def receiver_run():
    param = json.loads(request.data.decode('utf-8'))
    system_run(param)

    return "Success!"

app.run(port=8000, debug=True)
