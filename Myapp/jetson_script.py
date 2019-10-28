from flask import Flask, render_template, request, session, redirect, jsonify
import os
import pychromecast
from lib.VoiceToText import VoiceText
import time
from lib.TakePhoto import tfOpenpose

ip_address = "192.168.100.44"  # ChromecastデバイスのIPアドレス
server_host = "192.168.100.46"  # このスクリプトを動かすサーバのホスト名
server_port = 5000  # このスクリプトを動かすサーバのポート番号

device = pychromecast.Chromecast(ip_address)
vt = VoiceText()
tf = tfOpenpose()
tf.setting()

app = Flask(__name__)

image_path = ''
answer = ''

# login page access
@app.route('/get', methods=['GET'])
def index():
    global image_path, answer
    if (image_path == '') and (answer == ''):
        return jsonify({'path': image_path, 'answer':answer})
    else:
        return jsonify({'path': 'None', 'answer':'None'})

@app.route('/post/<user>/<area>', methods=['POST'])
def form(user, area):
    global tf, vt,device,image_path, answer
    tf.captureSetting(filename='output',user=user, area=area)
    text = 'これから撮影を始めます'
    url = vt.main(text = text, server_host=server_host)
    device.wait()
    mc = device.media_controller
    mc.play_media(url, "audio/mp3")
    mc.block_until_active()
    tf.takeMovie()

    text = '少々お待ちください'
    url = vt.main(text = text, server_host=server_host)
    device.wait()
    mc = device.media_controller
    mc.play_media(url, "audio/mp3")
    mc.block_until_active()
    answer, image_path = tf.MovieToImage()

    if answer != 'NG':
        text = 'あなたは' + answer + 'を選びましたね。オープンイメージを押してください。'
    else:
        text = '何のポーズかわかりませんでした。再撮影を押してください'
    url = vt.main(text = text, server_host=server_host)
    url = vt.main(text = text, server_host=server_host)
    device.wait()
    mc = device.media_controller
    mc.play_media(url, "audio/mp3")
    mc.block_until_active()
    return redirect('http://192.168.100.28:8000/jetson/'+image_path.split('/')[-1]+'/'+answer)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=server_port)