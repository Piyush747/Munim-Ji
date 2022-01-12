import sqlite3

def create_db():
    con = sqlite3.connect(database="munimji.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(uid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, username TEXT, phonenumber TEXT, password TEXT, bal TEXT DEFAULT '0')")
    cur.execute("CREATE TABLE IF NOT EXISTS records(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, amount TEXT, remark TEXT,type TEXT, username TEXT, FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE)")
    # cur.execute("Drop Table if exists users")
    # cur.execute("DROP TABLE IF EXISTS records")
    con.commit()

create_db()