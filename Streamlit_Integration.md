# Olympic Reserve Database - Streamlit Integration Code
# Код для интеграции базы данных с приложением Streamlit
# Автор: Senior Web Developer (15 лет опыта в спорте и базах данных)
# Дата: 18 ноября 2025 г.

```python
import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ===== КОНФИГУРАЦИЯ =====
DB_NAME = 'olympic_reserve.db'
CACHE_DURATION = 3600  # 1 час

# ===== ФУНКЦИИ ПОДКЛЮЧЕНИЯ К БД =====

@st.cache_resource
def get_db_connection():
    """Получить подключение к базе данных"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_data(ttl=CACHE_DURATION)
def load_athletes():
    """Загрузить всех спортсменов из БД"""
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM athletes', conn)
    conn.close()
    return df

@st.cache_data(ttl=CACHE_DURATION)
def load_medical_records():
    """Загрузить медицинские записи"""
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM medical_records', conn)
    conn.close()
    return df

@st.cache_data(ttl=CACHE_DURATION)
def load_functional_tests():
    """Загрузить функциональные тесты"""
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM functional_tests', conn)
    conn.close()
    return df

@st.cache_data(ttl=CACHE_DURATION)
def load_psychological_records():
    """Загрузить психологические оценки"""
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM psychological_records', conn)
    conn.close()
    return df

@st.cache_data(ttl=CACHE_DURATION)
def load_financial_records():
    """Загрузить финансовые записи"""
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM financial_records', conn)
    conn.close()
    return df

@st.cache_data(ttl=CACHE_DURATION)
def load_mentorship_data():
    """Загрузить данные наставничества"""
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM mentorship', conn)
    conn.close()
    return df

@st.cache_data(ttl=CACHE_DURATION)
def load_training_camps():
    """Загрузить данные тренировочных сборов"""
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM training_camps', conn)
    conn.close()
    return df

# ===== ФУНКЦИИ АНАЛИЗА =====

def get_athlete_by_id(athlete_id):
    """Получить данные спортсмена по ID"""
    df = load_athletes()
    return df[df['athlete_id'] == athlete_id].to_dict('records')[0] if athlete_id in df['athlete_id'].values else None

def get_athlete_medical_history(athlete_id):
    """Получить медицинскую историю спортсмена"""
    df = load_medical_records()
    return df[df['athlete_id'] == athlete_id].sort_values('exam_date', ascending=False)

def get_athlete_functional_tests(athlete_id):
    """Получить функциональные тесты спортсмена"""
    df = load_functional_tests()
    return df[df['athlete_id'] == athlete_id].sort_values('test_date', ascending=False)

def get_athlete_psychological_profile(athlete_id):
    """Получить психологический профиль спортсмена"""
    df = load_psychological_records()
    return df[df['athlete_id'] == athlete_id].to_dict('records')[0] if athlete_id in df['athlete_id'].values else None

def get_athlete_mentorship(athlete_id):
    """Получить информацию о наставничестве"""
    df = load_mentorship_data()
    return df[df['athlete_id'] == athlete_id].to_dict('records')[0] if athlete_id in df['athlete_id'].values else None

def get_athlete_financial_info(athlete_id):
    """Получить финансовую информацию спортсмена"""
    df = load_financial_records()
    return df[df['athlete_id'] == athlete_id].to_dict('records')[0] if athlete_id in df['athlete_id'].values else None

def get_sport_statistics(sport):
    """Получить статистику по виду спорта"""
    df = load_athletes()
    sport_df = df[df['sport'] == sport]
    
    stats = {
        'total_athletes': len(sport_df),
        'main_pool': len(sport_df[sport_df['reserve_level'] == 'Основной пул']),
        'extended_pool': len(sport_df[sport_df['reserve_level'] == 'Расширенный пул']),
        'avg_age': sport_df['age'].mean(),
        'avg_height': sport_df['height_cm'].mean(),
        'avg_weight': sport_df['weight_cm'].mean(),
        'avg_vo2_max': sport_df['vo2_max_ml_kg_min'].mean(),
        'male_count': len(sport_df[sport_df['gender'] == 'М']),
        'female_count': len(sport_df[sport_df['gender'] == 'Ж'])
    }
    return stats

# ===== ВИЗУАЛИЗАЦИЯ =====

def plot_vo2_distribution(sport):
    """График распределения VO2max"""
    df = load_athletes()
    sport_df = df[df['sport'] == sport]
    
    fig = px.histogram(sport_df, x='vo2_max_ml_kg_min', nbins=15, 
                       color='gender', barmode='overlay',
                       title=f'Распределение VO₂max в {sport}',
                       labels={'vo2_max_ml_kg_min': 'VO₂max (мл·кг⁻¹·мин⁻¹)', 'count': 'Количество'})
    return fig

def plot_anthropometry(sport):
    """График антропометрических данных"""
    df = load_athletes()
    sport_df = df[df['sport'] == sport]
    
    fig = px.scatter(sport_df, x='height_cm', y='weight_kg', color='gender',
                     size='vo2_max_ml_kg_min', hover_name='full_name',
                     title=f'Антропометрия спортсменов {sport}',
                     labels={'height_cm': 'Рост (см)', 'weight_kg': 'Вес (кг)'})
    return fig

def plot_performance_correlation(sport):
    """График корреляции показателей производительности"""
    df = load_athletes()
    sport_df = df[df['sport'] == sport]
    
    fig = px.scatter(sport_df, x='vo2_max_ml_kg_min', y='rating_position', 
                     color='reserve_level', size='training_experience_years',
                     hover_name='full_name',
                     title=f'Корреляция VO₂max и рейтинга в {sport}',
                     labels={'vo2_max_ml_kg_min': 'VO₂max (мл·кг⁻¹·мин⁻¹)', 
                            'rating_position': 'Позиция в рейтинге'})
    return fig

def plot_psychological_profile(athlete_id):
    """График психологического профиля"""
    psych = get_athlete_psychological_profile(athlete_id)
    if not psych:
        return None
    
    categories = ['Мотивация', 'Устойчивость к стрессу', 'Уверенность в себе', 
                 'Концентрация', 'Командное взаимодействие', 'Восстановление']
    values = [
        psych['motivation_level_1_10'],
        psych['stress_resilience_1_10'],
        psych['self_confidence_1_10'],
        psych['concentration_ability_1_10'],
        psych['team_cooperation_1_10'],
        psych['recovery_rate_1_10']
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
    ))
    
    fig.update_layout(
        title='Психологический профиль спортсмена',
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False
    )
    
    return fig

def plot_functional_tests_trend(athlete_id):
    """График тренда функциональных тестов"""
    df = get_athlete_functional_tests(athlete_id)
    if df.empty:
        return None
    
    df['test_date'] = pd.to_datetime(df['test_date'])
    df = df.sort_values('test_date')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df['test_date'], y=df['vo2_max_ml_kg_min'],
                            mode='lines+markers', name='VO₂max',
                            line=dict(color='royalblue', width=2)))
    
    fig.update_layout(
        title='Динамика функциональных показателей',
        xaxis_title='Дата теста',
        yaxis_title='VO₂max (мл·кг⁻¹·мин⁻¹)',
        hovermode='x unified'
    )
    
    return fig

# ===== ГЛАВНОЕ ПРИЛОЖЕНИЕ =====

def main():
    st.set_page_config(page_title="Программа мониторинга олимпийского резерва", 
                       layout="wide", initial_sidebar_state="expanded")
    
    st.title("🎯 Программа мониторинга и управления олимпийским резервом РФ")
    
    # Боковая навигация
    with st.sidebar:
        st.image("https://olympic.ru/wp-content/uploads/2021/11/logo_okr.png", width=150)
        st.markdown("---")
        page = st.radio("Навигация", 
                       ["📊 Общая статистика", 
                        "👤 Профиль спортсмена",
                        "🏃 Анализ по видам спорта",
                        "📈 Аналитика данных",
                        "💰 Финансирование"])
    
    # ===== СТРАНИЦА 1: ОБЩАЯ СТАТИСТИКА =====
    if page == "📊 Общая статистика":
        st.header("Общая статистика программы")
        
        df_athletes = load_athletes()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Всего спортсменов", len(df_athletes))
        
        with col2:
            main_pool = len(df_athletes[df_athletes['reserve_level'] == 'Основной пул'])
            st.metric("🎯 Основной пул", main_pool)
        
        with col3:
            extended_pool = len(df_athletes[df_athletes['reserve_level'] == 'Расширенный пул'])
            st.metric("📋 Расширенный пул", extended_pool)
        
        with col4:
            avg_age = df_athletes['age'].mean()
            st.metric("📅 Средний возраст", f"{avg_age:.1f} лет")
        
        st.markdown("---")
        
        # Распределение по видам спорта
        col1, col2 = st.columns(2)
        
        with col1:
            sport_counts = df_athletes['sport'].value_counts()
            fig = px.pie(values=sport_counts.values, names=sport_counts.index,
                        title="Распределение спортсменов по видам спорта")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            gender_sport = df_athletes.groupby(['sport', 'gender']).size().unstack()
            fig = px.bar(gender_sport, barmode='stack',
                        title="Распределение по полам и видам спорта",
                        labels={'value': 'Количество', 'index': 'Вид спорта'})
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Таблица спортсменов
        st.subheader("Список спортсменов")
        
        filter_sport = st.selectbox("Фильтр по виду спорта", 
                                   ["Все"] + df_athletes['sport'].unique().tolist())
        
        if filter_sport != "Все":
            df_filtered = df_athletes[df_athletes['sport'] == filter_sport]
        else:
            df_filtered = df_athletes
        
        st.dataframe(df_filtered[['athlete_id', 'full_name', 'gender', 'age', 'sport', 
                                  'reserve_level', 'vo2_max_ml_kg_min', 'rating_position']],
                    use_container_width=True)
    
    # ===== СТРАНИЦА 2: ПРОФИЛЬ СПОРТСМЕНА =====
    elif page == "👤 Профиль спортсмена":
        st.header("Профиль спортсмена")
        
        df_athletes = load_athletes()
        athlete_id = st.selectbox("Выберите спортсмена", df_athletes['athlete_id'])
        
        athlete = get_athlete_by_id(athlete_id)
        
        if athlete:
            # Основная информация
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("📋 Основная информация")
                st.write(f"**ФИО:** {athlete['full_name']}")
                st.write(f"**Возраст:** {athlete['age']} лет")
                st.write(f"**Пол:** {'Мужской' if athlete['gender'] == 'М' else 'Женский'}")
                st.write(f"**Вид спорта:** {athlete['sport']}")
                st.write(f"**Статус:** {athlete['status']}")
            
            with col2:
                st.subheader("💪 Антропометрия")
                st.write(f"**Рост:** {athlete['height_cm']} см")
                st.write(f"**Вес:** {athlete['weight_kg']} кг")
                st.write(f"**Жировая ткань:** {athlete['body_fat_percent']}%")
                st.write(f"**Мышечная масса:** {athlete['muscle_mass_percent']}%")
                st.write(f"**Опыт тренировок:** {athlete['training_experience_years']} лет")
            
            with col3:
                st.subheader("🏃 Физические показатели")
                st.write(f"**VO₂max:** {athlete['vo2_max_ml_kg_min']} мл·кг⁻¹·мин⁻¹")
                st.write(f"**ЧСС покоя:** {athlete['resting_heart_rate_bpm']} уд/мин")
                st.write(f"**Макс. ЧСС:** {athlete['heart_rate_peak_bpm']} уд/мин")
                st.write(f"**Резерв:** {athlete['reserve_level']}")
                st.write(f"**Рейтинг:** {athlete['rating_position']} место")
            
            st.markdown("---")
            
            # Медицинские данные
            st.subheader("🏥 Медицинские данные")
            medical_history = get_athlete_medical_history(athlete_id)
            
            if not medical_history.empty:
                latest_medical = medical_history.iloc[0]
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Вес (последний осмотр)", f"{latest_medical['weight_kg']} кг")
                    st.metric("VO₂max (пик)", f"{latest_medical['vo2_peak_ml_kg_min']} мл·кг⁻¹·мин⁻¹")
                
                with col2:
                    st.metric("Статус здоровья", latest_medical['health_status'])
                    st.metric("Гемоглобин", f"{latest_medical['hemoglobin_g_dl']} г/дл")
                
                with col3:
                    st.metric("Кровяное давление", f"{latest_medical['systolic_blood_pressure']}/{latest_medical['diastolic_blood_pressure']}")
                    st.metric("Допуск к тренировкам", latest_medical['medical_clearance'])
                
                st.write("**История медицинских осмотров:**")
                st.dataframe(medical_history[['exam_date', 'weight_kg', 'vo2_peak_ml_kg_min', 
                                              'health_status', 'medical_clearance']])
            
            st.markdown("---")
            
            # Психологический профиль
            st.subheader("🧠 Психологический профиль")
            psych = get_athlete_psychological_profile(athlete_id)
            
            if psych:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.write(f"**Мотивация:** {psych['motivation_level_1_10']}/10")
                    st.write(f"**Устойчивость к стрессу:** {psych['stress_resilience_1_10']}/10")
                    st.write(f"**Тревога:** {psych['anxiety_level_1_10']}/10")
                    st.write(f"**Уверенность в себе:** {psych['self_confidence_1_10']}/10")
                    st.write(f"**Концентрация:** {psych['concentration_ability_1_10']}/10")
                    st.write(f"**Восстановление:** {psych['recovery_rate_1_10']}/10")
                
                with col2:
                    fig = plot_psychological_profile(athlete_id)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Наставничество
            st.subheader("👨‍🏫 Программа наставничества")
            mentorship = get_athlete_mentorship(athlete_id)
            
            if mentorship:
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Наставник:** {mentorship['mentor_name']}")
                    st.write(f"**Начало программы:** {mentorship['program_start_date']}")
                
                with col2:
                    st.write(f"**Консультации в месяц:** {mentorship['consultation_frequency_per_month']}")
                    st.write(f"**Прогресс подопечного:** {mentorship['mentee_progress_rating_1_10']}/10")
                    st.write(f"**Отзыв:** {mentorship['mentee_feedback']}")
            
            st.markdown("---")
            
            # Финансирование
            st.subheader("💰 Финансирование")
            finance = get_athlete_financial_info(athlete_id)
            
            if finance:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Стипендия", f"₽{finance['monthly_stipend_rub']:,}")
                    st.metric("Питание/проживание", f"₽{finance['accommodation_budget_rub']:,}")
                
                with col2:
                    st.metric("Медицинское обслуживание", f"₽{finance['medical_services_budget_rub']:,}")
                    st.metric("Психологическое сопровождение", f"₽{finance['psychological_services_budget_rub']:,}")
                
                with col3:
                    st.metric("Итого в месяц", f"₽{finance['total_monthly_budget_rub']:,.0f}")
                    st.write(f"**Источник:** {finance['funding_source']}")
            
            st.markdown("---")
            
            # Функциональные тесты
            st.subheader("📊 Динамика функциональных показателей")
            fig = plot_functional_tests_trend(athlete_id)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            functional_tests = get_athlete_functional_tests(athlete_id)
            if not functional_tests.empty:
                st.write("**История тестов:**")
                st.dataframe(functional_tests[['test_date', 'test_type', 'vo2_max_ml_kg_min', 
                                               'peak_power_watts', 'notes']])
    
    # ===== СТРАНИЦА 3: АНАЛИЗ ПО ВИДАМ СПОРТА =====
    elif page == "🏃 Анализ по видам спорта":
        st.header("Анализ по видам спорта")
        
        df_athletes = load_athletes()
        sport = st.selectbox("Выберите вид спорта", df_athletes['sport'].unique())
        
        stats = get_sport_statistics(sport)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Всего спортсменов", stats['total_athletes'])
        
        with col2:
            st.metric("Основной пул", stats['main_pool'])
        
        with col3:
            st.metric("Расширенный пул", stats['extended_pool'])
        
        with col4:
            st.metric("М/Ж", f"{stats['male_count']}/{stats['female_count']}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = plot_vo2_distribution(sport)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = plot_anthropometry(sport)
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        fig3 = plot_performance_correlation(sport)
        st.plotly_chart(fig3, use_container_width=True)
    
    # ===== СТРАНИЦА 4: АНАЛИТИКА =====
    elif page == "📈 Аналитика данных":
        st.header("Аналитика данных")
        
        df_athletes = load_athletes()
        df_psychological = load_psychological_records()
        df_financial = load_financial_records()
        
        # Корреляция VO2max и рейтинга
        fig1 = px.scatter(df_athletes, x='vo2_max_ml_kg_min', y='rating_position',
                         color='sport', size='training_experience_years',
                         title='Корреляция VO₂max и рейтинга',
                         labels={'vo2_max_ml_kg_min': 'VO₂max (мл·кг⁻¹·мин⁻¹)',
                                'rating_position': 'Позиция в рейтинге'})
        st.plotly_chart(fig1, use_container_width=True)
        
        # Распределение по возрасту
        fig2 = px.histogram(df_athletes, x='age', nbins=10,
                           color='sport',
                           title='Распределение спортсменов по возрасту',
                           labels={'age': 'Возраст', 'count': 'Количество'})
        st.plotly_chart(fig2, use_container_width=True)
        
        # Средний психологический балл по видам спорта
        df_combined = df_athletes.merge(df_psychological, on='athlete_id', how='left')
        psycho_sport = df_combined.groupby('sport')['overall_psychological_score_1_100'].mean()
        
        fig3 = px.bar(x=psycho_sport.index, y=psycho_sport.values,
                     title='Средний психологический балл по видам спорта',
                     labels={'x': 'Вид спорта', 'y': 'Средний балл (0-100)'})
        st.plotly_chart(fig3, use_container_width=True)
    
    # ===== СТРАНИЦА 5: ФИНАНСИРОВАНИЕ =====
    elif page == "💰 Финансирование":
        st.header("Финансирование программы")
        
        df_athletes = load_athletes()
        df_financial = load_financial_records()
        
        # Общий бюджет
        total_budget = df_financial['total_monthly_budget_rub'].sum()
        st.metric("Общий ежемесячный бюджет", f"₽{total_budget:,.0f}")
        
        st.markdown("---")
        
        # Распределение по статьям
        budget_by_source = df_financial.groupby('funding_source')['total_monthly_budget_rub'].sum()
        
        fig1 = px.pie(values=budget_by_source.values, names=budget_by_source.index,
                     title='Распределение бюджета по источникам финансирования')
        st.plotly_chart(fig1, use_container_width=True)
        
        # Статьи расходов
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_stipend = df_financial['monthly_stipend_rub'].sum()
            st.metric("Стипендии спортсменов", f"₽{avg_stipend:,}")
        
        with col2:
            avg_medical = df_financial['medical_services_budget_rub'].sum()
            st.metric("Медицинское обслуживание", f"₽{avg_medical:,}")
        
        with col3:
            avg_equipment = df_financial['equipment_budget_rub'].sum()
            st.metric("Экипировка", f"₽{avg_equipment:,}")
        
        st.markdown("---")
        
        # Финансирование по видам спорта
        df_combined = df_athletes.merge(df_financial, on='athlete_id', how='left')
        budget_by_sport = df_combined.groupby('sport')['total_monthly_budget_rub'].sum()
        
        fig2 = px.bar(x=budget_by_sport.index, y=budget_by_sport.values,
                     title='Бюджет по видам спорта',
                     labels={'x': 'Вид спорта', 'y': 'Бюджет (₽)'})
        st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    main()
```

---

## Инструкция по интеграции с Streamlit

### 1. Требования
```bash
pip install streamlit pandas sqlite3 plotly numpy
```

### 2. Структура проекта
```
olympicreserve/
├── streamlit_app.py          # Основное приложение
├── olympic_reserve.db        # База данных (из этого кода)
├── requirements.txt          # Зависимости
└── .streamlit/
    └── config.toml          # Конфигурация Streamlit
```

### 3. Файл requirements.txt
```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
numpy>=1.24.0
```

### 4. Запуск локально
```bash
streamlit run streamlit_app.py
```

### 5. Развертывание на Streamlit Cloud
```bash
git push origin main  # Загрузить код в GitHub
# Перейти на https://share.streamlit.io
# Выбрать репозиторий и развернуть
```

---

## Описание таблиц базы данных

### 1. **athletes** - Основная информация о спортсменах
- athlete_id: Уникальный идентификатор
- full_name: ФИО
- gender: М/Ж
- age: Возраст
- sport: Вид спорта (Гребля, Лыжные гонки, Биатлон)
- vo2_max_ml_kg_min: VO₂max в мл·кг⁻¹·мин⁻¹
- reserve_level: Основной/Расширенный пул

### 2. **medical_records** - Медицинские данные
- medical_record_id: Уникальный ID
- athlete_id: Ссылка на спортсмена
- exam_date: Дата осмотра
- vo2_peak_ml_kg_min: VO₂peak
- health_status: Статус здоровья

### 3. **functional_tests** - Функциональные тесты
- test_id: Уникальный ID
- athlete_id: Ссылка на спортсмена
- test_type: Тип теста
- vo2_max_ml_kg_min: Результат VO₂max
- performance_time_seconds: Время выполнения

### 4. **psychological_records** - Психологические оценки
- psych_record_id: Уникальный ID
- athlete_id: Ссылка на спортсмена
- motivation_level_1_10: Мотивация (1-10)
- stress_resilience_1_10: Устойчивость к стрессу (1-10)
- overall_psychological_score_1_100: Общий балл (0-100)

### 5. **financial_records** - Финансирование
- finance_record_id: Уникальный ID
- athlete_id: Ссылка на спортсмена
- monthly_stipend_rub: Стипендия в руб.
- total_monthly_budget_rub: Общий ежемесячный бюджет

### 6. **mentorship** - Наставничество
- mentorship_id: Уникальный ID
- athlete_id: Ссылка на спортсмена
- mentor_id: Ссылка на наставника
- consultation_frequency_per_month: Частота консультаций

### 7. **training_camps** - Тренировочные сборы
- camp_id: Уникальный ID
- athlete_id: Ссылка на спортсмена
- location: Место проведения
- duration_days: Продолжительность

---

## Примеры SQL запросов

```sql
-- Получить всех спортсменов основного пула
SELECT * FROM athletes WHERE reserve_level = 'Основной пул';

-- Среднее VO₂max по видам спорта
SELECT sport, AVG(vo2_max_ml_kg_min) as avg_vo2
FROM athletes
GROUP BY sport;

-- История медицинских осмотров спортсмена
SELECT a.full_name, m.exam_date, m.vo2_peak_ml_kg_min, m.health_status
FROM athletes a
JOIN medical_records m ON a.athlete_id = m.athlete_id
WHERE a.athlete_id = 'ROWINGM001'
ORDER BY m.exam_date DESC;

-- Финансовые затраты по видам спорта
SELECT a.sport, SUM(f.total_monthly_budget_rub) as total_budget
FROM athletes a
JOIN financial_records f ON a.athlete_id = f.athlete_id
GROUP BY a.sport;

-- Спортсмены с наставниками
SELECT a.full_name, m.mentor_name, m.mentee_progress_rating_1_10
FROM athletes a
JOIN mentorship m ON a.athlete_id = m.athlete_id
ORDER BY m.mentee_progress_rating_1_10 DESC;
```

---

## Научная база данных

### Источники данных:
1. **Гребля:** Barthalos et al. (2025) "Analysis of the Physiological Characteristics of Elite Male and Female Junior Rowers During Extreme Exercise"
   - Мужчины (15-17 лет): VO₂peak = 58.73 ± 5.25 мл·кг⁻¹·мин⁻¹
   - Женщины (15-18 лет): VO₂peak = 48.32 ± 6.09 мл·кг⁻¹·мин⁻¹

2. **Лыжные гонки:** Данные основаны на текущих исследованиях элитных юных лыжников
   - Мужчины: VO₂max ≈ 65 мл·кг⁻¹·мин⁻¹
   - Женщины: VO₂max ≈ 55 мл·кг⁻¹·мин⁻¹

3. **Биатлон:** Исследования физиологических характеристик юных элитных биатлонистов
   - Мужчины: VO₂max ≈ 68 мл·кг⁻¹·мин⁻¹
   - Женщины: VO₂max ≈ 58 мл·кг⁻¹·мин⁻¹

---

**Автор:** Senior Web Developer (15 лет опыта в спорте, Python, SQL, Streamlit)
**Дата создания:** 18 ноября 2025 г.
**Версия:** 1.0