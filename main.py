from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from data_access import DataAccess
from post import Post

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

data = DataAccess()
login_ok = False
en_es = 'es'
current_user_id = None
post_list = []
post_list_final = []

@app.route("/")
def index():
    global login_ok
    posts_list_db = data.get_posts()
    post_list.clear()
    for post in posts_list_db:
        id = post[0]
        id_user = post[1]
        post_body = post[2]
        url_img = post[3]
        title = post[4]
        subtitle = post[5]
        aux = Post(id, id_user, post_body, url_img, title, subtitle)
        post_list.append(aux)
    return render_template("index.html", posts=post_list, login=login_ok)    

@app.route("/post/<int:post_id>")
def view_post(post_id):
    post_data = data.get_post_by_id(post_id)

    if post_data is None:
        return redirect("/")

    post = Post(post_data[0], post_data[1], post_data[2], post_data[3], post_data[4], post_data[5])
    return render_template("post.html", post=post)

@app.route("/add_Post")
def add_post():
    global login_ok
    if not login_ok:
        return redirect("/login")
    else:
        return render_template("add_post.html", login=login_ok)
    
@app.route("/profile")
def profile():
    global login_ok
    if not login_ok:
        return redirect("/login")
    else:
        posts = data.get_user_post(current_user_id)
        posts_list = []

        for post in posts:
            print(post)
            post_data = data.get_post_by_id(post[0])
            p = Post(post_data[0], post_data[1], post_data[2], post_data[3], post_data[4], post_data[5])
            posts_list.append(p)
            posts_list.reverse()
        return render_template("profile.html", login=login_ok, posts_list = posts_list)
    

@app.route("/add_new_post", methods=["POST"])
def add_new_post():
    global current_user_id
    if current_user_id is None:
        return redirect("/login")

    id_user = current_user_id
    title = request.form.get("title")
    post = request.form.get("textarea")
    file = request.files.get("formFile")
    subtitle = request.form.get("subtitle", None) 

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    url_img = os.path.join('img', filename)
    url_img = url_img.replace('\\', '/')
    if (title and post and file) and(file and allowed_file(file.filename)):
        data.add_post(id_user, post, url_img, title, subtitle)
        return redirect("/")
    else:
        return render_template("add_Post.html")

@app.route("/login")
def login():
    global login_ok
    if login_ok:
        return redirect("/")
    else:
        return render_template("login.html", login=login_ok)

@app.route("/login_", methods=["POST"])
def login_():
    global login_ok, current_user_id
    user = request.form.get("user")
    password = request.form.get("password")
    userlog = data.get_user(user, password)
    if userlog is None:
        return redirect("/login")
    else:
        login_ok = True
        current_user_id = userlog[0]
        return redirect("/")

    
@app.route("/new_user", methods=["GET"])
def new_user():
    global login_ok
    if login_ok:
        return redirect("/")
    else:
        return render_template("new_user.html", login=login_ok)
    
@app.route("/new_user_", methods=["POST"])
def new_user_():
    global login_ok, current_user_id
    
    if login_ok:
        return redirect("/")
    
    username = request.form.get("user")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    email = request.form.get("email")

    if password1 != password2:
        return render_template("new_user.html", login=login_ok, username=username, email=email, error="Las contraseñas no coinciden.")

    if data.user_exists(username):
            return render_template("new_user.html", login=login_ok, username=username, email=email, error="El nombre de usuario ya existe. Por favor, elija uno diferente.")

    data.add_user(username, password1, email)
    return redirect("/login")

@app.route("/log_out")
def log_out():
    global login_ok, current_user_id
    login_ok = False
    current_user_id = None
    return redirect("/")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(port=7000, debug=True)
