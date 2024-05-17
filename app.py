from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS items
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL);''')

@app.route('/')
def index():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item_name = request.form['name']
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO items (name) VALUES (?)", (item_name,))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add_item.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)