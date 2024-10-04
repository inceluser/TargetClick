from flask import Flask, render_template, request, redirect, session, jsonify
import json
import os
import time
import random

app = Flask(__name__)
app.secret_key = 'R3EdyG8VCe'

# Путь к JSON файлу для хранения результатов
RESULTS_FILE = 'results.json'

# Чтение результатов из JSON файла
def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            results = json.load(f)
            # Преобразуем время в float для всех результатов
            for result in results:
                result['time_spent'] = float(result['time_spent'])
            return results
    return []

# Запись результатов в JSON файл
def save_results(results):
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f)

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
    
    # Загрузка текущих результатов
    results = load_results()
    
    # Добавление нового результата
    results.append({'username': username, 'time_spent': time_spent})
    
    # Сортировка результатов по времени (чем меньше, тем лучше)
    results = sorted(results, key=lambda x: x['time_spent'])  # Преобразуем время в float
    
    # Сохранение обновленных результатов
    save_results(results)
    
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

if __name__ == '__main__':
    app.run(debug=True)
