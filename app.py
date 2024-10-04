from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os
import time
import random

app = Flask(__name__)
app.secret_key = 'R3EdyG8VCe'

# Путь к файлу базы данных
DATABASE = 'results.db'

# Инициализация базы данных
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                time_spent REAL NOT NULL
            )
        ''')
        conn.commit()

# Загрузка результатов из базы данных
def load_results():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('SELECT username, time_spent FROM results ORDER BY time_spent')
        results = [{'username': row[0], 'time_spent': row[1]} for row in c.fetchall()]
    return results

# Запись результатов в базу данных
def save_result(username, time_spent):
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO results (username, time_spent) VALUES (?, ?)', (username, time_spent))
        conn.commit()

# Главная страница с игрой
@app.route('/')
def index():
    if 'username' not in session:
        return redirect('/login')
    return render_template('index.html', username=session['username'])

# Страница входа/регистрации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        # Ограничение на длину ника
        if len(username) > 15:
            return render_template('login.html', error="Username must be 15 characters or less.")
        session['username'] = username
        return redirect('/')
    return render_template('login.html')

# Обработка завершения игры и сохранение результатов
@app.route('/submit_result', methods=['POST'])
def submit_result():
    if 'username' not in session:
        return redirect('/login')
    
    time_spent = float(request.form['time_spent'])
    username = session['username']
    
    # Сохранение нового результата в базу данных
    save_result(username, time_spent)
    
    return redirect('/results')

# Страница с результатами
@app.route('/results')
def results():
    results = load_results()
    return render_template('results.html', results=results)

# Выход из сессии
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')
        # 

# Инициализация базы данных при запуске приложения
init_db()
    
if __name__ == '__main__':
    app.run(debug=True)
