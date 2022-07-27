このリポジトリは、ILASセミナー2022用に作成されたものです。
# Confortable Panda on Slack

[![License](https://img.shields.io/github/license/kyoto-u/ilas2022?color=orange)](https://github.com/kyoto-u/ilas2022/blob/master/LICENSE)
[![Release](https://img.shields.io/github/v/release/kyoto-u/comfortable-sakai?include_prereleases)](https://github.com/kyoto-u/comfortable-sakai/releases)
[![CodeQL](https://github.com/kyoto-u/comfortable-sakai/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kyoto-u/comfortable-sakai/actions/workflows/codeql-analysis.yml)  
[![npm test](https://github.com/kyoto-u/comfortable-sakai/actions/workflows/npm_tests.yml/badge.svg)](https://github.com/kyoto-u/comfortable-sakai/actions/workflows/npm_tests.yml)

## 流れ
---
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
---
1 : 名前 2022-06-27 23:55:00（datetimeオブジェクト）
この形式でいいと思います。

## コマンド提案
---------------------------------------------------------------------------------------
 ```/task 名前```

タスクを追加する

```/task 名前 yyyymmddhhmm```

期限付きのタスクを追加する (hhmmは省略すると00:00になります) 

例(test, 2003/10/18 10:45): ```/task test 200310181045```

```/task 名前 yyyymmddhhmm+[任意の数字]n[y,m,d]```

任意の整数nを用いて定期的なタスクを登録できます。y:年、m:月、d:日を用いて繰り返しを定義できます。この場合、時刻を省略することはできません。
 例(お誕生日 2003/10/18/00:00から毎年繰り返し): ```/task お誕生日 200310180000+1ny```

```/task```

タスクを一覧表示します。 

```/task fin [タスクの番号]```

タスクを消します。 /task で表示したときの番号で指定します。タスクを追加したり消したりするとこの番号は変わるので注意してください。 

```/task del [タスクの番号]```

同じくタスクを消しますが、こちらを用いると繰り返しタスクをすべて消すことができます。 

```/task help```

ヘルプ表示

## Dockerについて（サーバー環境）
---
src/slack_bolt/*はサーバー側で動かします.
また, 実行時にはDockerを使用します.
そのため, pipパッケージを追加したい場合には, ilas2022-docker/Dockerfile に ```RUN python -m pip install ***```を追加してください. 

イメージを作り, コンテナを立ち上げる際は
```
$ cd ilas2022-docker/
$ docker compose up -d --build

$ docker compose exec python3 bash
```
をしてください. 

