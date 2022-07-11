from html import entities
import pickle

# 受信
infList = [
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
    ]
]

# # 受信
# infList = [ # infomation_list
#     {
#         "course": {
#             "id": "サンプル授業ID1",
#             "name": "サンプル名前1",
#             "link": "サンプルhttps://panda.ecs.kyoto-u.ac.jp/portal/site/授業ID1"
#         },
#         "entries": [
#             {
#                 "id": "サンプル課題ID1",
#                 "title": "サンプル第九回の課題1",
#                 "dueTime": "サンプル期限日1",
#                 "closeTime": "遅延提出期限日1",
#                 "hasFinished": "サンプル終わったかどうか1" #bool　値
#             }
#         ],
#         "isRead": False  # false ← わからない???
#     },
#     {
#         "course": {
#             "id": "サンプル授業ID2",
#             "name": "サンプル名前2",
#             "link": "サンプルhttps://panda.ecs.kyoto-u.ac.jp/portal/site/授業ID2"
#         },
#         "entries": [
#             {
#                 "id": "サンプル課題ID2",
#                 "title": "サンプル第九回の課題2",
#                 "dueTime": "サンプル期限日2",
#                 "closeTime": "遅延提出期限日2",
#                 "hasFinished": "サンプル終わったかどうか2" #bool　値
#             }
#         ],
#         "isRead": False  # false ← わからない???
#     },
#     {
#         "course": {
#             "id": "サンプル授業ID3",
#             "name": "サンプル名前3",
#             "link": "サンプルhttps://panda.ecs.kyoto-u.ac.jp/portal/site/授業ID3"
#         },
#         "entries": [
#             {
#                 "id": "サンプル課題ID3",
#                 "title": "サンプル第九回の課題3",
#                 "dueTime": "サンプル期限日3",
#                 "closeTime": "遅延提出期限日3",
#                 "hasFinished": "サンプル終わったかどうか3" #bool　値
#             }
#         ],
#         "isRead": False  # false ← わからない???
#     },
# ]



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