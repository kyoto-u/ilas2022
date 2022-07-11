#これはpythonによるデータ送信側のテストコード
import requests

#POST先URL
url = "http://127.0.0.1:8000"

#JSON形式のデータ
payload = [
    "userid",
    [ # infomation_list
        {
            "course": {
                "id": "授業ID",
                "name": "名前",
                "link": "https://panda.ecs.kyoto-u.ac.jp/portal/site/授業ID"
            },
            "entries": [
                {
                    "id": "課題ID",
                    "title": "第九回の課題",
                    "dueTime": "期限日",
                    "closeTime": "遅延提出期限日",
                    "hasFinished": "終わったかどうか" #bool　値
                }
            ],
            "isRead": False  # false ← わからない???
        },
    ]]
r = requests.post(url, json=payload)
print(r)
