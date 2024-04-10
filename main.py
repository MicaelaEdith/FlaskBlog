from flask import Flask, render_template, request, redirect
from data_access import DataAccess
from post import Post

app = Flask(__name__)

loggin_ok=False
id=1
data= DataAccess()

post_list = []
post_list_final = []

@app.route("/")
def index():
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
	return render_template("index.html", posts = post_list)	
	
@app.route("/addPost")
def add_post():
	return render_template("add_post.html")	

@app.route("/login")
def login():
	return render_template("login.html")
	
@app.route("/add_new_post", methods=["POST"])
def add_new_post():
		print("paso1")
		id_user=id
		title=request.form.get("title")
		subtitle=request.form.get("subtitle")
		post=request.form.get("textarea")
		url_img="khgg"
		print("paso")
		data.add_post(id_user, post,url_img,title,subtitle)
		return redirect("/")
		
		
		

if __name__=="__main__":
	app.run(port=7000,debug=True)