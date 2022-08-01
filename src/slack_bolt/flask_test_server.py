# coding: utf-8
from flask import Flask, render_template
from flask import request

app = Flask(__name__) 

@app.route("/")
def index():
    return "Hello Flask!"

@app.route("/", methods=["POST"])  #追加
def login_manager():
    return "ようこそ、" + request.form["username"] + "さん"

if __name__ == "__main__":
    # webサーバー立ち上げ
    app.run(host='0.0.0.0', port=8080)