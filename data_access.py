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
            "INSERT INTO POST(id_user, post, url_img, title, subtitle) VALUES (%s, %s, %s, %s, %s)", 
            (id_user, post, url_img, title, subtitle)
        )
        self.connection.commit()
        print("Post agregado")
        self.disconnect()

    def get_posts(self):
        self.connect()
        self.cursor.execute("SELECT * FROM POST ORDER BY id DESC")
        all_posts = self.cursor.fetchall()
        self.disconnect()
        return all_posts
    
    def add_user(self, username, password):
        self.connect()
        self.cursor.execute(
            "INSERT INTO USERS (username, password, admin) VALUES (%s, %s, %s)", 
            (username, password, 0)
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
