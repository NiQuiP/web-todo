from flask import Flask, render_template, request, url_for, redirect, flash
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'usfrctvw6bdtqd9z',
    'password': '2TfxpuVTt3pmqwdjFcuC',  
    'host': 'brywriu7r3g2fby2inam-mysql.services.clever-cloud.com',
    'database': 'brywriu7r3g2fby2inam'
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
    app.run()