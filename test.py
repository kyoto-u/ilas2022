from flask import Flask, request
import json
from html import entities
import pickle


#def system_run内でSlack側の処理を記述
def system_run(infList):
    # 整形
    usedInfList = [infList[0]] # 保存するようの情報
    # usedInfListに必要な情報を追加していく
    for inf in infList[1]:

        usedInf = {
            "course" : inf["course"]["name"], # 授業名
            "title" : inf["entries"][0]["title"], # 課題名]
            "dueTime" : inf["entries"][0]["dueTime"], # 締切日時
            "closeTime" : inf["entries"][0]["closeTime"], # 遅延提出期限日
            "hasFinished" : inf["entries"][0]["hasFinished"], # 終わったかどうか(bool値)
            "isRead" : inf["isRead"] # 何に使うかは7/4現在不明(bool値)
        }

        usedInfList.append(usedInf)
    
    # 保存
    with open('datas.pickle', mode='wb') as f:
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
