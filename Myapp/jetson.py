from flask import Flask, render_template, request, session, redirect, jsonify
from lib.user_management import Management
from lib.quest_management import questMap
app = Flask(__name__)
app.secret_key = b'random string...'

# login page access
@app.route('/', methods=['GET'])
def login():
    return render_template('login.html',
            title='Adachi Quest',
            message='')

@app.route('/jetson', methods=['POST'])
def index_post():
    id = request.form.get('id')
    pswd = request.form.get('pass')
    # User & Password が一致するときのみTrue
    myPlace = {'name':'研究室','lat':35.747701, 'lng':139.806098}
    qm = questMap(lat=myPlace['lat'], lng=myPlace['lng'])
    pins, question = qm.main()
    return render_template('jetson.html',
                title='Adachi Quest',
                message='Hello',
                user=id,
                password=pswd,
                pins = pins,
                question = question,
                myPlace =myPlace)

@app.route('/jetson', methods=['GET'])
def index_get():
    return redirect('/')

@app.route('/login', methods=['GET'])
def login_get():
    return redirect('/')


@app.route('/login', methods=['POST'])
def login_post():
    id = request.form.get('id')
    pswd = request.form.get('pass')
    manager = Management(user_id=id, password=pswd)
    # User & Password が一致するときのみTrue
    flg = manager.checkLogin()
    myPlace = {'name':'研究室','lat':35.747701, 'lng':139.806098}
    qm = questMap(lat=myPlace['lat'], lng=myPlace['lng'])
    pins, question = qm.main()
    if flg:
        return render_template('jetson.html',
                title='Adachi Quest',
                message='Hello',
                user=id,
                password=pswd,
                pins = pins,
                question = question,
                myPlace =myPlace)
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True, use_debugger=False)
