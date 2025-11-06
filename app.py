from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from database import users_db, athletes_db, users_credentials
from models import User, Athlete
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # В продакшене заменить на надежный ключ

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в систему'

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id), users_db)

def check_password_stub(password_hash, password):
    """Заглушка для проверки пароля - в продакшене использовать нормальную аутентификацию"""
    return password == "password123"

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = None
        for uid, user_obj in users_db.items():
            if user_obj.username == username:
                user = user_obj
                break
        
        if user and check_password_stub(users_credentials.get(username, ''), password):
            login_user(user)
            flash('Успешный вход в систему!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        athletes = athletes_db
    else:
        athletes = [a for a in athletes_db if a.sport == current_user.sport]
    
    # Статистика
    total_athletes = len(athletes)
    sports_stats = {}
    for athlete in athletes:
        if athlete.sport not in sports_stats:
            sports_stats[athlete.sport] = 0
        sports_stats[athlete.sport] += 1
    
    return render_template('dashboard.html', 
                         athletes=athletes, 
                         total_athletes=total_athletes,
                         sports_stats=sports_stats)

@app.route('/athlete/<int:athlete_id>')
@login_required
def athlete_detail(athlete_id):
    athlete = next((a for a in athletes_db if a.id == athlete_id), None)
    
    if not athlete:
        flash('Спортсмен не найден', 'error')
        return redirect(url_for('dashboard'))
    
    # Проверка прав доступа
    if current_user.role == 'curator' and athlete.sport != current_user.sport:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('athlete_detail.html', athlete=athlete)

@app.route('/generate_report/<int:athlete_id>')
@login_required
def generate_report(athlete_id):
    athlete = next((a for a in athletes_db if a.id == athlete_id), None)
    
    if not athlete:
        flash('Спортсмен не найден', 'error')
        return redirect(url_for('dashboard'))
    
    # Проверка прав доступа
    if current_user.role == 'curator' and athlete.sport != current_user.sport:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('dashboard'))
    
    # Создание PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Заголовок
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 100, f"СПОРТИВНЫЙ ПАСПОРТ")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 120, f"Спортсмен: {athlete.full_name}")
    p.drawString(100, height - 140, f"Вид спорта: {athlete.sport}")
    p.drawString(100, height - 160, f"Дата рождения: {athlete.birth_date} (Возраст: {athlete.age} лет)")
    
    # Персональные данные
    y = height - 200
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "ПЕРСОНАЛЬНЫЕ ДАННЫЕ")
    y -= 30
    
    p.setFont("Helvetica", 10)
    p.drawString(100, y, f"Регион: {athlete.region}")
    y -= 20
    p.drawString(100, y, f"Тренер: {athlete.coach}")
    y -= 20
    p.drawString(100, y, f"Контактный телефон: {athlete.contact_phone}")
    y -= 40
    
    # Физические показатели
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "ФИЗИЧЕСКИЕ ПОКАЗАТЕЛИ")
    y -= 30
    
    p.setFont("Helvetica", 10)
    physical = athlete.physical_data
    p.drawString(100, y, f"МПК (VO2max): {physical['vo2max']} мл/кг/мин")
    y -= 20
    p.drawString(100, y, f"Максимальная сила: {physical['max_strength']} кг")
    y -= 20
    p.drawString(100, y, f"Безжировая масса тела: {physical['lean_body_mass']} кг")
    y -= 20
    p.drawString(100, y, f"ПАНО: {physical['anaerobic_threshold']} ммоль/л")
    y -= 20
    p.drawString(100, y, f"ЧСС в покое: {physical['resting_hr']} уд/мин")
    y -= 20
    p.drawString(100, y, f"Максимальная ЧСС: {physical['max_hr']} уд/мин")
    y -= 20
    p.drawString(100, y, f"Ударный объем сердца: {physical['stroke_volume']} мл")
    y -= 40
    
    # Медицинские данные
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "МЕДИЦИНСКИЕ ДАННЫЕ")
    y -= 30
    
    p.setFont("Helvetica", 10)
    medical = athlete.medical_data
    p.drawString(100, y, f"Группа крови: {medical['blood_type']}")
    y -= 20
    p.drawString(100, y, f"Последний медосмотр: {medical['last_medical_check']}")
    y -= 20
    p.drawString(100, y, f"Травмы: {medical['injuries']}")
    y -= 20
    p.drawString(100, y, f"Рекомендации: {medical['recommendations']}")
    y -= 40
    
    # Сохранение PDF
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return send_file(buffer, 
                    as_attachment=True, 
                    download_name=f"Паспорт_{athlete.full_name.replace(' ', '_')}.pdf",
                    mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
