from flask import Flask, render_template, request
from data_access import DataAccess
from post import Post

app = Flask(__name__)

data= DataAccess()
posts_list_db = data.get_posts()
post_list = []

for post in posts_list_db:
	id= post[0]
	id_user=post[1]
	post_body=post[2]
	url_img=post[3]
	title=post[4]
	subtitle= post[5]
	aux=Post(id,id_user,post_body,url_img,title,subtitle)
	post_list.append(aux)

@app.route("/")
def index():
	return render_template("index.html", posts = post_list)	
	
@app.route("/addPost")
def add_post():
	return render_template("add_post.html")	



if __name__=="__main__":
	app.run(port=7000,debug=True)