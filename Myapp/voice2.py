from flask import Flask, render_template, request, session, redirect, jsonify
import os
import pychromecast
from lib.VoiceToText import VoiceText
import time

ip_address = "x.x.x.x"  # ChromecastデバイスのIPアドレス
server_host = "x.x.x.x"  # このスクリプトを動かすサーバのホスト名
server_port = 8000  # このスクリプトを動かすサーバのポート番号
app = Flask(__name__)
device = pychromecast.Chromecast(ip_address)
device.wait()

# login page access
@app.route('/', methods=['GET'])
def index():
    return render_template('practice.html',
            title='Practice',
            message='Hello')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=server_port, debug=True, use_reloader=True, use_debugger=False)
