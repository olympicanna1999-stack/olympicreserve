import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import base64

# Конфигурация страницы
st.set_page_config(
    page_title="Цифровой реестр спортсменов",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Мок-данные пользователей
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin', 'sport': None},
    'curator_ski': {'password': 'curator123', 'role': 'curator', 'sport': 'лыжные гонки'},
    'curator_biathlon': {'password': 'curator123', 'role': 'curator', 'sport': 'биатлон'},
    'curator_row': {'password': 'curator123', 'role': 'curator', 'sport': 'академическая гребля'}
}

def generate_mock_athletes():
    sports = {
        'лыжные гонки': ['Москва', 'Санкт-Петербург', 'Краснодар', 'Екатеринбург', 'Новосибирск'],
        'биатлон': ['Москва', 'Тюмень', 'Ханты-Мансийск', 'Красноярск', 'Омск'],
        'академическая гребля': ['Москва', 'Санкт-Петербург', 'Ростов-на-Дону', 'Казань', 'Самара']
    }
    
    male_names = ['Александр', 'Дмитрий', 'Михаил', 'Андрей', 'Сергей', 'Алексей', 'Артем', 'Иван', 'Кирилл', 'Максим']
    female_names = ['Анна', 'Мария', 'Екатерина', 'Ольга', 'Ирина', 'Наталья', 'Елена', 'Светлана', 'Юлия', 'Татьяна']
    last_names = ['Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Соколов', 'Михайлов', 'Новиков']
    
    athletes = []
    athlete_id = 1
    
    for sport, regions in sports.items():
        for i in range(15):
            if sport == 'академическая гребля':
                is_male = random.choice([True, False, False])
            else:
                is_male = random.choice([True, True, False])
            
            if is_male:
                first_name = random.choice(male_names)
                gender = 'М'
                last_name = random.choice(last_names)  # Мужская фамилия
            else:
                first_name = random.choice(female_names)
                gender = 'Ж'
                last_name = random.choice(last_names) + 'а'  # Женская фамилия
            
            full_name = f"{last_name} {first_name}"
            
            # Возраст 14-18 лет
            birth_year = 2005 + random.randint(0, 4)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            birth_date = date(birth_year, birth_month, birth_day)
            
            # Генерация физических данных
            if sport == 'лыжные гонки':
                vo2max_range = (55, 75) if is_male else (50, 65)
                strength_range = (45, 65) if is_male else (35, 50)
                lean_mass_range = (55, 70) if is_male else (45, 55)
            elif sport == 'биатлон':
                vo2max_range = (58, 72) if is_male else (52, 63)
                strength_range = (40, 60) if is_male else (30, 45)
                lean_mass_range = (52, 68) if is_male else (43, 53)
            else:  # академическая гребля
                vo2max_range = (60, 78) if is_male else (55, 68)
                strength_range = (55, 80) if is_male else (40, 60)
                lean_mass_range = (60, 75) if is_male else (48, 58)
            
            athlete_data = {
                'id': athlete_id,
                'full_name': full_name,
                'birth_date': birth_date,
                'age': calculate_age(birth_date),
                'sport': sport,
                'gender': gender,
                'region': random.choice(regions),
                'coach': f"Тренер {random.choice(['А', 'Б', 'В'])}",
                'contact_phone': f"+7{random.randint(9000000000, 9999999999)}",
                'physical_data': {
                    'vo2max': round(random.uniform(*vo2max_range), 1),
                    'max_strength': random.randint(*strength_range),
                    'lean_body_mass': round(random.uniform(*lean_mass_range), 1),
                    'anaerobic_threshold': round(random.uniform(3.5, 6.5), 1),
                    'resting_hr': random.randint(45, 65),
                    'max_hr': random.randint(185, 205),
                    'stroke_volume': random.randint(80, 130)
                },
                'medical_data': {
                    'blood_type': random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                    'last_medical_check': (date.today() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
                    'injuries': random.choice(['Нет', 'Легкое растяжение', 'Старая травма колена', 'Нет']),
                    'recommendations': random.choice(['Допущен без ограничений', 'Ограничение нагрузок 20%', 'Допущен']),
                    'doctor_notes': 'Регулярные медицинские осмотры'
                },
                'psychological_data': {
                    'motivation': random.randint(7, 10),
                    'stress_resistance': random.randint(6, 10),
                    'concentration': random.randint(7, 10),
                    'teamwork': random.randint(6, 10),
                    'discipline': random.randint(8, 10),
                    'assessment_date': (date.today() - timedelta(days=random.randint(0, 60))).strftime('%Y-%m-%d')
                }
            }
            
            athletes.append(athlete_data)
            athlete_id += 1
    
    return athletes

def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def authenticate(username, password):
    if username in USERS and USERS[username]['password'] == password:
        return USERS[username]
    return None

def login_page():
    st.title("🏆 Цифровой реестр спортсменов")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("Вход в систему")
            username = st.text_input("Имя пользователя")
            password = st.text_input("Пароль", type="password")
            submit = st.form_submit_button("Войти")
            
            if submit:
                user = authenticate(username, password)
                if user:
                    st.session_state.user = user
                    st.session_state.logged_in = True
                    st.success("Успешный вход!")
                    st.rerun()
                else:
                    st.error("Неверное имя пользователя или пароль")
        
        st.markdown("---")
        st.info("**Тестовые аккаунты:**")
        st.write("- **admin** / admin123 - Руководитель проекта")
        st.write("- **curator_ski** / curator123 - Куратор лыжных гонок")
        st.write("- **curator_biathlon** / curator123 - Куратор биатлона")
        st.write("- **curator_row** / curator123 - Куратор академической гребли")

def generate_pdf_report(athlete):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Заголовок
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 100, "СПОРТИВНЫЙ ПАСПОРТ")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 120, f"Спортсмен: {athlete['full_name']}")
    p.drawString(100, height - 140, f"Вид спорта: {athlete['sport']}")
    p.drawString(100, height - 160, f"Дата рождения: {athlete['birth_date'].strftime('%Y-%m-%d')} (Возраст: {athlete['age']} лет)")
    
    # Персональные данные
    y = height - 200
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "ПЕРСОНАЛЬНЫЕ ДАННЫЕ")
    y -= 30
    
    p.setFont("Helvetica", 10)
    p.drawString(100, y, f"Регион: {athlete['region']}")
    y -= 20
    p.drawString(100, y, f"Тренер: {athlete['coach']}")
    y -= 20
    p.drawString(100, y, f"Контактный телефон: {athlete['contact_phone']}")
    y -= 40
    
    # Физические показатели
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "ФИЗИЧЕСКИЕ ПОКАЗАТЕЛИ")
    y -= 30
    
    p.setFont("Helvetica", 10)
    physical = athlete['physical_data']
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
    medical = athlete['medical_data']
    p.drawString(100, y, f"Группа крови: {medical['blood_type']}")
    y -= 20
    p.drawString(100, y, f"Последний медосмотр: {medical['last_medical_check']}")
    y -= 20
    p.drawString(100, y, f"Травмы: {medical['injuries']}")
    y -= 20
    p.drawString(100, y, f"Рекомендации: {medical['recommendations']}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

def dashboard():
    st.sidebar.title(f"👤 {st.session_state.user['role'].title()}")
    st.sidebar.write(f"Пользователь: {[k for k, v in USERS.items() if v == st.session_state.user][0]}")
    if st.session_state.user['sport']:
        st.sidebar.write(f"Вид спорта: {st.session_state.user['sport']}")
    
    if st.sidebar.button("🚪 Выйти"):
        st.session_state.clear()
        st.rerun()
    
    st.title("🏆 Цифровой реестр спортсменов")
    st.markdown("---")
    
    # Фильтрация спортсменов по правам доступа
    if st.session_state.user['role'] == 'admin':
        athletes = st.session_state.athletes
    else:
        athletes = [a for a in st.session_state.athletes if a['sport'] == st.session_state.user['sport']]
    
    # Статистика
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Всего спортсменов", len(athletes))
    with col2:
        st.metric("Лыжные гонки", len([a for a in athletes if a['sport'] == 'лыжные гонки']))
    with col3:
        st.metric("Биатлон", len([a for a in athletes if a['sport'] == 'биатлон']))
    with col4:
        st.metric("Академическая гребля", len([a for a in athletes if a['sport'] == 'академическая гребля']))
    
    st.markdown("---")
    
    # Поиск и фильтры
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Поиск по ФИО")
    with col2:
        sport_filter = st.selectbox("Вид спорта", ["Все"] + list(set(a['sport'] for a in athletes)))
    
    # Фильтрация
    filtered_athletes = athletes
    if search:
        filtered_athletes = [a for a in filtered_athletes if search.lower() in a['full_name'].lower()]
    if sport_filter != "Все":
        filtered_athletes = [a for a in filtered_athletes if a['sport'] == sport_filter]
    
    # Таблица спортсменов
    if filtered_athletes:
        df_data = []
        for athlete in filtered_athletes:
            df_data.append({
                'ID': athlete['id'],
                'ФИО': athlete['full_name'],
                'Возраст': athlete['age'],
                'Вид спорта': athlete['sport'],
                'Регион': athlete['region'],
                'МПК': athlete['physical_data']['vo2max'],
                'Тренер': athlete['coach']
            })
        
        df = pd.DataFrame(df_data)
        
        # Стилизация таблицы
        def style_vo2max(val):
            color = 'background-color: #d4edda' if val > 65 else 'background-color: #fff3cd'
            return color
        
        styled_df = df.style.applymap(style_vo2max, subset=['МПК'])
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Детальная информация
        st.subheader("📊 Детальная информация о спортсмене")
        selected_id = st.selectbox("Выберите спортсмена", [f"{a['id']} - {a['full_name']}" for a in filtered_athletes])
        
        if selected_id:
            athlete_id = int(selected_id.split(' - ')[0])
            athlete = next(a for a in filtered_athletes if a['id'] == athlete_id)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Персональные данные**")
                st.write(f"ФИО: {athlete['full_name']}")
                st.write(f"Дата рождения: {athlete['birth_date'].strftime('%Y-%m-%d')}")
                st.write(f"Возраст: {athlete['age']} лет")
                st.write(f"Пол: {athlete['gender']}")
                st.write(f"Регион: {athlete['region']}")
                st.write(f"Тренер: {athlete['coach']}")
                st.write(f"Телефон: {athlete['contact_phone']}")
                
                st.markdown("**Медицинские данные**")
                medical = athlete['medical_data']
                st.write(f"Группа крови: {medical['blood_type']}")
                st.write(f"Последний медосмотр: {medical['last_medical_check']}")
                st.write(f"Травмы: {medical['injuries']}")
                st.write(f"Рекомендации: {medical['recommendations']}")
            
            with col2:
                st.markdown("**Физические показатели**")
                physical = athlete['physical_data']
                st.metric("МПК (VO2max)", f"{physical['vo2max']} мл/кг/мин")
                st.metric("Максимальная сила", f"{physical['max_strength']} кг")
                st.metric("Безжировая масса", f"{physical['lean_body_mass']} кг")
                st.metric("ПАНО", f"{physical['anaerobic_threshold']} ммоль/л")
                st.metric("ЧСС в покое", f"{physical['resting_hr']} уд/мин")
                st.metric("Макс. ЧСС", f"{physical['max_hr']} уд/мин")
                st.metric("Ударный объем", f"{physical['stroke_volume']} мл")
                
                st.markdown("**Психологические оценки**")
                psycho = athlete['psychological_data']
                st.write(f"Мотивация: {psycho['motivation']}/10")
                st.write(f"Стрессоустойчивость: {psycho['stress_resistance']}/10")
                st.write(f"Концентрация: {psycho['concentration']}/10")
                st.write(f"Командная работа: {psycho['teamwork']}/10")
                st.write(f"Дисциплина: {psycho['discipline']}/10")
            
            # Генерация PDF
            st.markdown("---")
            st.subheader("📄 Генерация отчета")
            if st.button("Сгенерировать PDF отчет"):
                pdf_buffer = generate_pdf_report(athlete)
                st.success("PDF отчет успешно сгенерирован!")
                
                # Кнопка скачивания
                b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="Паспорт_{athlete["full_name"].replace(" ", "_")}.pdf">📥 Скачать PDF отчет</a>'
                st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Спортсмены не найдены")

def main():
    # Инициализация сессии
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.athletes = generate_mock_athletes()
    
    if not st.session_state.logged_in:
        login_page()
    else:
        dashboard()

if __name__ == "__main__":
    main()
