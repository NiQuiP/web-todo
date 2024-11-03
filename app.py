from flask import Flask, render_template, request, url_for, redirect, flash
import mysql.connector
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

db_config = {
    'user': 'root',  # Ganti jika username MySQL berbeda
    'password': '',  # Ganti jika ada password
    'host': 'localhost',
    'database': 'web-todo'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form['title']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO todos (title) VALUES (%s)", (title,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Berhasil menambahkan list", "success")
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        new_title = request.form['title']
        cursor.execute("UPDATE todos SET title = %s WHERE id = %s", (new_title, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Berhasil update list", "success")
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM todos WHERE id = %s", (id,))
    todo = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', todo=todo)

@app.route('/delete/<int:id>')
def delete_todo(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Berhasil menghapus list", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)