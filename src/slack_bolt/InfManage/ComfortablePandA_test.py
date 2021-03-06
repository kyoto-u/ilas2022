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
                "id": "2022-888-R106-054",
                "name": "[2022前期金２]英語リーディング",
                "link": "https://panda.ecs.kyoto-u.ac.jp/portal/site/2022-888-R106-054"
            },
            "entries": [
                {
                    "id": "00001",
                    "title": "最後のリサーチ報告",
                    "dueTime": "1657980000",
                    "closeTime": "遅延提出期限日",
                    "hasFinished": "終わったかどうか" #bool　値
                }
            ],
            "isRead": False  # false ← わからない???
        },
    ]]
r = requests.post(url, json=payload)
print(r)
