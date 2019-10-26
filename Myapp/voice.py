from flask import Flask, render_template, request, session, redirect, jsonify
import os
import pychromecast
from lib.VoiceToText import VoiceText
import time
from lib.TakePhoto import tfOpenpose

ip_address = "192.168.100.41"  # ChromecastデバイスのIPアドレス
server_host = "192.168.100.36"  # このスクリプトを動かすサーバのホスト名
server_port = 5000  # このスクリプトを動かすサーバのポート番号

app = Flask(__name__)
device = pychromecast.Chromecast(ip_address)
device.wait()
tf = tfOpenpose()
tf.setting()


# login page access
@app.route('/', methods=['GET'])
def index():
    return render_template('practice.html',
            title='Practice',
            message='Hello')

@app.route('/port', methods=['POST'])
def form():
    global tf
    text = 'これから撮影を始めます。'
    vt = VoiceText(device=device)
    vt.main(text = text, server_host=server_host)
    tf.main()
    return redirect('http://192.168.100.36:8000/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=server_port, debug=True, use_reloader=True, use_debugger=False)
