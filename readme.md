このリポジトリは、ILASセミナー2022用に作成されたものです。

# 流れ
typescript 送信
python 受信

受信データ
```
[
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
                "dueTime": 期限日,
                "closeTime": 遅延提出期限日,
                "hasFinished": 終わったかどうか bool
            }
        ],
        "isRead": false ← わからない???
    },
]
```

このデータから課題一覧と期限日、終わったか（提出済みか）どうかを取り出します。

処理後のデータを別で格納、またプログラムが終了しても消えないようにこの段階で外部に出力しておきます。

このデータを用いてTodoリストを作ります(後述)

## Todoリストの形式の提案
1 : 名前 2022-06-27 23:55:00
この形式でいいと思います。

## コマンド提案
---------------------------------------------------------------------------------------
タスクを追加する /task 名前

期限付きのタスクを追加する (hhmmは省略すると00:00になります) /task 名前 yyyymmddhhmm
例(test, 2003/10/18 10:45): /task test 200310181045

任意の整数nを用いて定期的なタスクを登録できます。y:年、m:月、d:日を用いて繰り返しを定義できます。この場合、時刻を省略することはできません。+のところスペースは入れないでね～ /task 名前 yyyymmddhhmm+[任意の数字]n[y,m,d]
 例(お誕生日 2003/10/18/00:00から毎年繰り返し): /task walnutsお誕生日 200310180000+1ny

タスクを一覧表示します。 /task

タスクを消します。 /task で表示したときの番号で指定します。タスクを追加したり消したりするとこの番号は変わるので注意してください。 /task fin [タスクの番号]

同じくタスクを消しますが、こちらを用いると繰り返しタスクをすべて消すことができます。 /task del [タスクの番号]

ヘルプ表示 /task help

---------------------------------------------------------------------------------------






slack_incomming.py: Slack bot using Incomming Webhook
slack_bolt.py:      Slack bot using Bolt
dot.env:            Template of environment variables for slack_bolt.py
                    Please copy dot.env to .env and change each value
