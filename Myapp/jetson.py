from flask import Flask, render_template, request, session, redirect, jsonify
from lib.user_management import Management
from lib.quest_management import questMap
app = Flask(__name__)
app.secret_key = b'random string...'

AREA = ''

# login page access
@app.route('/<point>', methods=['GET'])
def login(point):
    global AREA
    AREA = point
    return render_template('login.html',
            title='Adachi Quest')

@app.route('/jetson', methods=['POST'])
def index_post():
    id = request.form.get('id')
    pswd = request.form.get('pass')
    return render_template('jetson.html',
                title='Adachi Quest',
                message='Hello',
                user=id,
                password=pswd,
                flg=True)


@app.route('/login', methods=['GET'])
def login_get():
    return redirect('/')

@app.route('/takephoto', methods=['POST'])
def takephoto_post():
    id = request.form.get('id')
    pswd = request.form.get('pass')
    return render_template('takephoto.html',
                title='Adachi Quest',
                message='Hello',
                user=id,
                password=pswd)

@app.route('/login', methods=['POST'])
def login_post():
    global AREA
    id = request.form.get('id')
    pswd = request.form.get('pass')
    manager = Management(user_id=id, password=pswd)
    # User & Password が一致するときのみTrue
    flg = manager.checkLogin()
    if flg:
        return render_template('jetson.html',
                title='Adachi Quest',
                point=AREA,
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
    return redirect('/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True, use_debugger=False)
