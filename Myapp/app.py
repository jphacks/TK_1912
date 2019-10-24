from flask import Flask, render_template, request, session, redirect, jsonify

app = Flask(__name__)
app.secret_key = b'random string...'
member_data = {}

@app.route('/', methods=['GET'])
def index():
    if 'login' in session and session['login']:
        msg = 'Login id:'+session['id']
        return render_template('index.html',
                title='Messages',
                message=msg)
    else:
        return redirect('/login')

# login page access
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html',
            title='Adachi Quest',
            err=False,
            message='IDとパスワードを入力：',
            id='')


@app.route('/login', methods=['POST'])
def login_post():
    global member_data
    id = request.form.get('id')
    pswd = request.form.get('pass')
    if id in member_data:
        if pswd == member_data[id]:
            session['login'] = True
        else:
            session['login'] = False
    else:
        member_data[id] = pswd
        session['login'] = True
    session['id'] = id
    if session['login']:
        return redirect('/')
    else:
        return render_template('login.html',
                title='Adachi Quest',
                err=False,
                message='パスワードが違います。',
                id=id)
                
@app.route('/signup', methods=['POST'])
def signup_post():
    global member_data
    id = request.form.get('id')
    pswd = request.form.get('pass')
    if id in member_data:
        if pswd == member_data[id]:
            session['login'] = True
            flg = 'True'
        else:
            session['login'] = False
            flg = 'False'
    else:
        member_data[id] = pswd
        session['login'] = True
        flg = 'True'
    session['id'] = id
    return flg

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True, use_debugger=False)
