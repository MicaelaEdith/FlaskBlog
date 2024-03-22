import sqlite3
from post import Post

class DataAccess:
    def __init__(self):
        self.db_name = "./sql/blog_db.db"

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()

    def add_user(self, username, password):
        self.connect()
        self.cursor.execute("INSERT INTO USERS (username, password) VALUES (?, ?)", (username, password))
        self.connection.commit()
        print('guardado')
        self.disconnect()

    def get_user(self, username):
        self.connect()
        self.cursor.execute("SELECT * FROM USERS WHERE username=?", (username,))
        user = self.cursor.fetchone()
        self.disconnect()
        return user

    def add_post(self):
	    pass
		
    def get_posts(self):
	    self.connect()
	    self.cursor.execute("SELECT * from POST")
	    all_posts = self.cursor.fetchall()
	    self.disconnect()
	    return all_posts	

	
