from flask import Flask, render_template, request, session, redirect, jsonify
from lib.user_management import Management
from lib.quest_management import questMap
from lib.answer_management import AnswerManage
import urllib.error
import urllib.request
import os
import requests

app = Flask(__name__)
app.secret_key = b'random string...'

AREA = ''
username = ''


def download_img(url, dst, path):
    os.makedirs(dst, exist_ok=True)
    dst_path = os.path.join(dst, path)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(dst_path, 'wb') as f:
            f.write(r.content)


# login page access
@app.route('/<point>', methods=['GET'])
def login(point):
    global AREA
    if point != 'favicon.ico':
        AREA = point
    return render_template('login.html',
            title='Adachi Quest')

@app.route('/', methods=['GET'])
def login_redirect():
    return render_template('login.html',
            title='Adachi Quest')

@app.route('/jetson/<path>/<answer>', methods=['GET'])
def index_post(path, answer):
    global AREA, username
    # Areaのクエストを表示
    am = AnswerManage(area=AREA)
    data = am.acquisitionQuest()
    url = 'http://x.x.x.x:5000/static/data/' + username + '/' + data['name'] + '/' + answer + '/' + path
    dst = './static/data/' + username + '/' + data['name']
    download_img(url, dst, 'result.jpg')
    return render_template('jetson.html',
                title='Adachi Quest',
                message='Hello',
                user=username,
                password='',
                flg=True,
                quest=data,
                file=path,
                answer=answer)


@app.route('/login', methods=['GET'])
def login_get():
    return redirect('/')

@app.route('/takephoto', methods=['POST'])
def takephoto_post():
    global AREA
    id = request.form.get('id')
    pswd = request.form.get('pass')
    answer = request.form.get('answer')
    am = AnswerManage(area=AREA)
    data = am.acquisitionQuest()
    return render_template('takephoto.html',
                title='Adachi Quest',
                message='Hello',
                user=id,
                password=pswd,
                quest=data,
                answer=answer)

@app.route('/login', methods=['POST'])
def login_post():
    global AREA, username
    id = request.form.get('id')
    username = id
    pswd = request.form.get('pass')
    manager = Management(user_id=id, password=pswd)
    # User & Password が一致するときのみTrue
    flg = manager.checkLogin()
    # Areaのクエストを表示
    am = AnswerManage(area=AREA)
    data = am.acquisitionQuest()
    if flg:
        return render_template('jetson.html',
                title='Adachi Quest',
                quest=data,
                user=id,
                password=pswd,
                flg=False)
    else:
        return render_template('login.html',
                title='Adachi Quest',
                message='パスワードが異なるか、登録がありません。') 
                
@app.route('/signup', methods=['POST'])
def signup_post():
    id = request.form.get('name')
    pswd = request.form.get('password')
    manager = Management(user_id=id, password=pswd)
    # 登録済みのUserの場合はFasle
    flg = manager.signup()
    return str(flg)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('id', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=True, use_debugger=False)
