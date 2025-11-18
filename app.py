# Olympic Reserve - Веб-приложение для мониторинга олимпийского резерва
# Optimized Version - Работает с SQLite базой данных
# Версия: 2.0 (совместимо с olympic_reserve.db)
# Автор: Senior Web Developer (15 лет опыта в спорте)
# Дата: 18 ноября 2025 г.

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import io
import base64
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ===== КОНФИГУРАЦИЯ =====
st.set_page_config(
    page_title="🏆 Программа мониторинга олимпийского резерва",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_NAME = 'olympic_reserve.db'
CACHE_DURATION = 3600  # 1 час

# ===== МОКИРОВАННЫЕ УЧЕТНЫЕ ДАННЫЕ =====
USERS = {
    'admin': {'password': 'admin123', 'role': 'admin', 'sport': None},
    'curator_rowing': {'password': 'curator123', 'role': 'curator', 'sport': 'Гребля'},
    'curator_skiing': {'password': 'curator123', 'role': 'curator', 'sport': 'Лыжные гонки'},
    'curator_biathlon': {'password': 'curator123', 'role': 'curator', 'sport': 'Биатлон'},
}

# ===== ФУНКЦИИ РАБОТЫ С БД =====

@st.cache_resource
def get_db_connection():
    """Получить подключение к БД"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        st.error(f"❌ Ошибка подключения к БД: {e}")
        return None

@st.cache_data(ttl=CACHE_DURATION)
def load_athletes():
    """Загрузить всех спортсменов из БД"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql('SELECT * FROM athletes', conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Ошибка загрузки спортсменов: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=CACHE_DURATION)
def load_medical_records():
    """Загрузить медицинские записи"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql('SELECT * FROM medical_records', conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=CACHE_DURATION)
def load_psychological_records():
    """Загрузить психологические записи"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql('SELECT * FROM psychological_records', conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=CACHE_DURATION)
def load_financial_records():
    """Загрузить финансовые записи"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql('SELECT * FROM financial_records', conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=CACHE_DURATION)
def load_mentorship():
    """Загрузить данные наставничества"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql('SELECT * FROM mentorship', conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=CACHE_DURATION)
def load_training_camps():
    """Загрузить данные тренировочных сборов"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql('SELECT * FROM training_camps', conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=CACHE_DURATION)
def load_functional_tests():
    """Загрузить функциональные тесты"""
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql('SELECT * FROM functional_tests', conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

# ===== ФУНКЦИИ АУТЕНТИФИКАЦИИ =====

def authenticate(username, password):
    """Проверить учетные данные"""
    if username in USERS and USERS[username]['password'] == password:
        return USERS[username]
    return None

def login_page():
    """Страница входа"""
    st.title("🏆 Цифровой реестр спортсменов")
    st.markdown("## Программа мониторинга олимпийского резерва РФ")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.subheader("🔐 Вход в систему")
            username = st.text_input("Имя пользователя")
            password = st.text_input("Пароль", type="password")
            submit = st.form_submit_button("Войти", use_container_width=True)
            
            if submit:
                user = authenticate(username, password)
                if user:
                    st.session_state.user = user
                    st.session_state.logged_in = True
                    st.success("✅ Успешный вход!")
                    st.rerun()
                else:
                    st.error("❌ Неверное имя пользователя или пароль")
    
    st.markdown("---")
    st.info("**📝 Тестовые аккаунты:**\n"
            "- **admin** / admin123 - Администратор (полный доступ)\n"
            "- **curator_rowing** / curator123 - Куратор гребли\n"
            "- **curator_skiing** / curator123 - Куратор лыжных гонок\n"
            "- **curator_biathlon** / curator123 - Куратор биатлона")

# ===== ФУНКЦИИ ГЕНЕРАЦИИ ОТЧЕТОВ =====

def generate_athlete_report_pdf(athlete_id, athlete_name):
    """Генерирование PDF отчета о спортсмене"""
    df_athletes = load_athletes()
    df_medical = load_medical_records()
    df_psych = load_psychological_records()
    
    athlete = df_athletes[df_athletes['athlete_id'] == athlete_id]
    if athlete.empty:
        return None
    
    athlete = athlete.iloc[0]
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Заголовок
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "СПОРТИВНЫЙ ПАСПОРТ")
    
    p.setFont("Helvetica", 11)
    p.drawString(50, height - 80, f"Спортсмен: {athlete['full_name']}")
    p.drawString(50, height - 100, f"Вид спорта: {athlete['sport']}")
    p.drawString(50, height - 120, f"Возраст: {athlete['age']} лет")
    p.drawString(50, height - 140, f"Пол: {athlete['gender']}")
    p.drawString(50, height - 160, f"Федерация: {athlete['federation']}")
    
    # Физические показатели
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 200, "ФИЗИЧЕСКИЕ ПОКАЗАТЕЛИ")
    
    p.setFont("Helvetica", 10)
    y = height - 230
    p.drawString(50, y, f"VO₂max: {athlete['vo2_max_ml_kg_min']} мл·кг⁻¹·мин⁻¹")
    y -= 20
    p.drawString(50, y, f"Рост: {athlete['height_cm']} см")
    y -= 20
    p.drawString(50, y, f"Вес: {athlete['weight_kg']} кг")
    y -= 20
    p.drawString(50, y, f"Жировая ткань: {athlete['body_fat_percent']}%")
    y -= 20
    p.drawString(50, y, f"Мышечная масса: {athlete['muscle_mass_percent']}%")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

# ===== ГЛАВНАЯ ПАНЕЛЬ УПРАВЛЕНИЯ =====

def dashboard():
    """Главная панель управления"""
    
    # Боковая панель
    with st.sidebar:
        st.title(f"👤 {st.session_state.user['role'].title()}")
        
        username = [k for k, v in USERS.items() if v == st.session_state.user][0]
        st.write(f"Пользователь: **{username}**")
        
        if st.session_state.user['sport']:
            st.write(f"Спорт: **{st.session_state.user['sport']}**")
        
        st.markdown("---")
        
        page = st.radio("📊 Навигация",
                       ["Общая статистика",
                        "Профиль спортсмена",
                        "Анализ данных",
                        "Финансирование",
                        "Наставничество"])
        
        st.markdown("---")
        if st.button("🚪 Выход", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # Основной контент
    st.title("🏆 Цифровой реестр спортсменов")
    
    if page == "Общая статистика":
        show_general_statistics()
    elif page == "Профиль спортсмена":
        show_athlete_profile()
    elif page == "Анализ данных":
        show_data_analysis()
    elif page == "Финансирование":
        show_financing()
    elif page == "Наставничество":
        show_mentorship_page()

# ===== СТРАНИЦА 1: ОБЩАЯ СТАТИСТИКА =====

def show_general_statistics():
    """Страница общей статистики"""
    st.header("📊 Общая статистика программы")
    
    df_athletes = load_athletes()
    
    if df_athletes.empty:
        st.error("❌ Данные не загружены. Проверьте базу данных.")
        return
    
    # Фильтрация по правам доступа
    if st.session_state.user['role'] == 'curator':
        df_athletes = df_athletes[df_athletes['sport'] == st.session_state.user['sport']]
    
    # Метрики
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Всего спортсменов", len(df_athletes))
    
    with col2:
        main_pool = len(df_athletes[df_athletes['reserve_level'] == 'Основной пул'])
        st.metric("🎯 Основной пул", main_pool)
    
    with col3:
        avg_vo2 = df_athletes['vo2_max_ml_kg_min'].mean()
        st.metric("📈 Средний VO₂max", f"{avg_vo2:.1f}")
    
    with col4:
        avg_age = df_athletes['age'].mean()
        st.metric("📅 Средний возраст", f"{avg_age:.1f}")
    
    st.markdown("---")
    
    # Распределение по видам спорта
    col1, col2 = st.columns(2)
    
    with col1:
        sport_counts = df_athletes['sport'].value_counts()
        fig = px.pie(values=sport_counts.values, names=sport_counts.index,
                    title="Распределение по видам спорта")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        reserve_counts = df_athletes['reserve_level'].value_counts()
        fig = px.bar(x=reserve_counts.index, y=reserve_counts.values,
                    title="Распределение по пулам",
                    labels={'x': 'Уровень резерва', 'y': 'Количество'})
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Таблица спортсменов
    st.subheader("📋 Список спортсменов")
    
    df_display = df_athletes[['athlete_id', 'full_name', 'gender', 'age', 'sport',
                               'reserve_level', 'vo2_max_ml_kg_min', 'status']].copy()
    df_display.columns = ['ID', 'ФИО', 'Пол', 'Возраст', 'Вид спорта',
                          'Резерв', 'VO₂max', 'Статус']
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

# ===== СТРАНИЦА 2: ПРОФИЛЬ СПОРТСМЕНА =====

def show_athlete_profile():
    """Страница профиля спортсмена"""
    st.header("👤 Профиль спортсмена")
    
    df_athletes = load_athletes()
    
    if df_athletes.empty:
        st.error("❌ Данные не загружены.")
        return
    
    # Фильтрация по правам доступа
    if st.session_state.user['role'] == 'curator':
        df_athletes = df_athletes[df_athletes['sport'] == st.session_state.user['sport']]
    
    athlete_options = [f"{row['athlete_id']} - {row['full_name']}" 
                       for _, row in df_athletes.iterrows()]
    
    if not athlete_options:
        st.warning("⚠️ Спортсмены не найдены для вашего вида спорта")
        return
    
    selected = st.selectbox("Выберите спортсмена", athlete_options)
    athlete_id = selected.split(' - ')[0]
    
    athlete = df_athletes[df_athletes['athlete_id'] == athlete_id].iloc[0]
    
    # Основная информация
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📋 Основная информация")
        st.write(f"**ФИО:** {athlete['full_name']}")
        st.write(f"**Возраст:** {athlete['age']} лет")
        st.write(f"**Пол:** {'Мужской' if athlete['gender'] == 'М' else 'Женский'}")
        st.write(f"**Вид спорта:** {athlete['sport']}")
    
    with col2:
        st.subheader("💪 Антропометрия")
        st.write(f"**Рост:** {athlete['height_cm']} см")
        st.write(f"**Вес:** {athlete['weight_kg']} кг")
        st.write(f"**Жировая ткань:** {athlete['body_fat_percent']}%")
        st.write(f"**Мышечная масса:** {athlete['muscle_mass_percent']}%")
    
    with col3:
        st.subheader("🏃 Физические показатели")
        st.write(f"**VO₂max:** {athlete['vo2_max_ml_kg_min']} мл·кг⁻¹·мин⁻¹")
        st.write(f"**ЧСС покоя:** {athlete['resting_heart_rate_bpm']} уд/мин")
        st.write(f"**Макс. ЧСС:** {athlete['heart_rate_peak_bpm']} уд/мин")
        st.write(f"**Резерв:** {athlete['reserve_level']}")
    
    st.markdown("---")
    
    # Медицинские данные
    st.subheader("🏥 Медицинские данные")
    df_medical = load_medical_records()
    
    medical_athlete = df_medical[df_medical['athlete_id'] == athlete_id]
    
    if not medical_athlete.empty:
        latest = medical_athlete.sort_values('exam_date').iloc[-1]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Последний вес", f"{latest['weight_kg']} кг")
            st.metric("VO₂peak", f"{latest['vo2_peak_ml_kg_min']}")
        
        with col2:
            st.metric("АД (сист./диаст.)", f"{latest['systolic_blood_pressure']}/{latest['diastolic_blood_pressure']}")
            st.metric("Гемоглобин", f"{latest['hemoglobin_g_dl']} г/дл")
        
        with col3:
            st.write(f"**Статус:** {latest['health_status']}")
            st.write(f"**Допуск:** {latest['medical_clearance']}")
    
    # Психологический профиль
    st.markdown("---")
    st.subheader("🧠 Психологический профиль")
    
    df_psych = load_psychological_records()
    psych_athlete = df_psych[df_psych['athlete_id'] == athlete_id]
    
    if not psych_athlete.empty:
        psych = psych_athlete.iloc[-1]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Мотивация:** {psych['motivation_level_1_10']}/10")
            st.write(f"**Стрессоустойчивость:** {psych['stress_resilience_1_10']}/10")
            st.write(f"**Уверенность в себе:** {psych['self_confidence_1_10']}/10")
        
        with col2:
            st.write(f"**Концентрация:** {psych['concentration_ability_1_10']}/10")
            st.write(f"**Командное взаимодействие:** {psych['team_cooperation_1_10']}/10")
            st.write(f"**Общий балл:** {psych['overall_psychological_score_1_100']}/100")

# ===== СТРАНИЦА 3: АНАЛИЗ ДАННЫХ =====

def show_data_analysis():
    """Страница анализа данных"""
    st.header("📈 Анализ данных")
    
    df_athletes = load_athletes()
    
    if df_athletes.empty:
        st.error("❌ Данные не загружены.")
        return
    
    # Фильтрация по правам доступа
    if st.session_state.user['role'] == 'curator':
        df_athletes = df_athletes[df_athletes['sport'] == st.session_state.user['sport']]
    
    # Корреляция VO₂max и рейтинга
    fig = px.scatter(df_athletes, x='vo2_max_ml_kg_min', y='rating_position',
                    color='gender', size='training_experience_years',
                    hover_name='full_name',
                    title='Корреляция VO₂max и рейтинга',
                    labels={'vo2_max_ml_kg_min': 'VO₂max (мл·кг⁻¹·мин⁻¹)',
                           'rating_position': 'Позиция в рейтинге'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Распределение по возрасту
    fig = px.histogram(df_athletes, x='age', nbins=10,
                      color='gender',
                      title='Распределение спортсменов по возрасту',
                      labels={'age': 'Возраст', 'count': 'Количество'})
    st.plotly_chart(fig, use_container_width=True)

# ===== СТРАНИЦА 4: ФИНАНСИРОВАНИЕ =====

def show_financing():
    """Страница финансирования"""
    st.header("💰 Финансирование программы")
    
    df_athletes = load_athletes()
    df_financial = load_financial_records()
    
    if df_financial.empty:
        st.warning("⚠️ Финансовые данные не загружены")
        return
    
    # Фильтрация по правам доступа
    if st.session_state.user['role'] == 'curator':
        df_athletes = df_athletes[df_athletes['sport'] == st.session_state.user['sport']]
        df_financial = df_financial[df_financial['athlete_id'].isin(df_athletes['athlete_id'])]
    
    # Общий бюджет
    total_budget = df_financial['total_monthly_budget_rub'].sum()
    st.metric("Общий ежемесячный бюджет", f"₽{total_budget:,.0f}")
    
    st.markdown("---")
    
    # Распределение по источникам
    budget_by_source = df_financial.groupby('funding_source')['total_monthly_budget_rub'].sum()
    
    fig = px.pie(values=budget_by_source.values, names=budget_by_source.index,
                title='Распределение по источникам финансирования')
    st.plotly_chart(fig, use_container_width=True)

# ===== СТРАНИЦА 5: НАСТАВНИЧЕСТВО =====

def show_mentorship_page():
    """Страница наставничества"""
    st.header("👨‍🏫 Программа наставничества")
    
    df_mentorship = load_mentorship()
    
    if df_mentorship.empty:
        st.warning("⚠️ Данные о наставничестве не загружены")
        return
    
    st.subheader("Наставники и подопечные")
    
    df_display = df_mentorship[['athlete_id', 'mentor_name', 'consultation_frequency_per_month',
                                'mentee_progress_rating_1_10', 'mentee_feedback']].copy()
    df_display.columns = ['ID спортсмена', 'Наставник', 'Консультации/месяц',
                          'Оценка прогресса', 'Отзыв']
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)

# ===== ГЛАВНАЯ ФУНКЦИЯ =====

def main():
    """Главная функция приложения"""
    
    # Инициализация сессии
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        dashboard()

if __name__ == "__main__":
    main()
