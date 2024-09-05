import mysql.connector
from mysql.connector import Error

class DataAccess:
    def __init__(self):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                port=3306,
                user='root',
                password='',
                database='blog_db'
            )
        except Error as ex:
            print(f'Error: {ex}')

    def connect(self):
        if self.connection is None:
            raise Error("No se pudo establecer la conexión con la base de datos.")
        
        if not self.connection.is_connected():
            self.connection.reconnect(attempts=3, delay=2)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def add_post(self, id_user, post, url_img, title, subtitle):
        self.connect()
        self.cursor.execute(
            "INSERT INTO POST(id_user, post, url_img, title, subtitle, activo) VALUES (%s, %s, %s, %s, %s, 1)", 
            (id_user, post, url_img, title, subtitle)
        )
        self.connection.commit()
        post_id = self.cursor.lastrowid
        
        self.cursor.execute(
            "INSERT INTO user_post (user_id, post_id) VALUES (%s, %s)", 
            (id_user, post_id)
        )
        self.connection.commit()
        self.disconnect()

    def get_posts(self):
        self.connect()
        self.cursor.execute("SELECT * FROM POST ORDER BY id DESC")
        all_posts = self.cursor.fetchall()
        self.disconnect()
        return all_posts
    
    def add_user(self, username, password, email):
        self.connect()
        self.cursor.execute(
            "INSERT INTO USERS (username, password, email, admin) VALUES (%s, %s, %s, %s)", 
            (username, password, email, 0)
        )
        self.connection.commit()
        self.disconnect()

    def get_user(self, username, password):
        self.connect()
        self.cursor.execute(
            "SELECT * FROM USERS WHERE username=%s and password=%s", 
            (username, password)
        )
        user = self.cursor.fetchone()
        self.disconnect()
        return user

    def user_exists(self, username):
        self.connect()
        self.cursor.execute("SELECT 1 FROM USERS WHERE username=%s", (username,))
        user = self.cursor.fetchone()
        self.disconnect()
        return user is not None
    
    def get_post_by_id(self, post_id):
        self.connect()
        self.cursor.execute("SELECT * FROM POST WHERE id=%s", (post_id,))
        post = self.cursor.fetchone()
        self.disconnect()
        return post
    
    def get_user_post(self, user_id):
        self.connect()
        self.cursor.execute("SELECT post_id FROM USER_POST WHERE user_id=%s", (user_id,))
        posts = self.cursor.fetchall()
        self.disconnect()
        return posts
    
    def del_post(self, id):
        self.connect()
        self.cursor.execute("UPDATE post SET activo = 0 WHERE id=%s", (id,))
        self.connection.commit()
        print("UPDATE post SET activo = 0 WHERE id=%s", (id,))
        self.disconnect()
