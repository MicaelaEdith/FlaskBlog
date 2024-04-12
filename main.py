from flask import Flask, render_template, request, redirect
from data_access import DataAccess
from post import Post


app = Flask(__name__)

id=1
data= DataAccess()
login_ok=False

post_list = []
post_list_final = []

@app.route("/")
def index():
	global login_ok
	posts_list_db = data.get_posts()
	post_list.clear()
	for post in posts_list_db:
		id= post[0]
		id_user=post[1]
		post_body=post[2]
		url_img=post[3]
		title=post[4]
		subtitle= post[5]
		aux=Post(id,id_user,post_body,url_img,title,subtitle)
		post_list.append(aux)
	return render_template("index.html", posts = post_list, login=login_ok)	
	
@app.route("/addPost")
def add_post():
	global login_ok
	if login_ok==False:
		return redirect("/login")
	else:
		return render_template("add_post.html",login=login_ok)	
	
@app.route("/login")
def login():
	global login_ok
	if login_ok==True:
		return redirect("/")
	else:
		return render_template("login.html",login=login_ok)

@app.route("/login_", methods=["POST"])
def login_():
	global login_ok
	user=request.form.get("user")
	password=request.form.get("password")
	userlog=data.get_user(user,password)
	if userlog=="":
		return redirect("/login" )
	else:
		login_ok=True
		return redirect("/")
	
@app.route("/add_new_post", methods=["POST"])
def add_new_post():
		id_user=id
		title=request.form.get("title")
		subtitle=request.form.get("subtitle")
		post=request.form.get("textarea")
		url_img="khgg"
		data.add_post(id_user, post,url_img,title,subtitle)
		return redirect("/")

@app.route("/log_out")	
def log_out():
	global login_ok
	login_ok=False
	return redirect("/")

if __name__=="__main__":
	app.run(port=7000,debug=True)
	
	
	