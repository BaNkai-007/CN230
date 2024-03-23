from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def landingPage():
    return render_template('index.html','style.css')

@app.route('/<name>')
def new(name):
    return f"hello, {name}!"

# @app.route('/hep')
# def stat(name=None):
#     return render_template('index.html',name=name)

# @app.route('/upload',methods=['GET','POST'])
# def upload():
#     if request.method() == 'POST':
#         file = request.files['file']
#         file.save(f"/var/www/uploads/{secure_filename(file.filename)}")

# @app.route("/me")
# def get_current_user():
#     username = input()
#     theme = input()
#     image = input()
# def me_api():
#     user = get_current_user()
#     return {
#         "username": user.username,
#         "theme": user.theme,
#         "image": url_for("user_image", filename=user.image),
#     }

# @app.route("/users")
# def get_all_users():
#     return user
# def users_api():
#     users = get_all_users()
#     return [user.to_json() for user in users]

users = {
    'amit':'amitpass',
    'sasmit':'sasmitpass'
}

@app.route('/login')
def load_page():
    return render_template('login.html')

@app.route('/handle_post',methods=['GET','POST'])

def handle_post():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        print(user,password)
        if user in users and users[user] == password:
            return "<h1>Welcome!</h1>"
        else:
            return '<h1>invalid</h1>'
    else:
        return render_template('login.html')

    