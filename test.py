from flask import Flask, request
import json


#def system_run内でSlack側の処理を記述
def system_run(data):
    print(data["some"])


#以下、Flask関連の処理
app = Flask(__name__, static_folder='.', static_url_path='')
@app.route('/', methods=["POST"])
def receiver_run():
    param = json.loads(request.data.decode('utf-8'))
    print(param)
    
    system_run(param)

    return "Success!"

app.run(port=8000, debug=True)
