from models import Athlete, User
from datetime import date, timedelta
import random

# Мок-данные пользователей
users_db = {
    1: User(1, 'admin', 'admin'),
    2: User(2, 'curator_ski', 'curator', 'лыжные гонки'),
    3: User(3, 'curator_biathlon', 'curator', 'биатлон'),
    4: User(4, 'curator_row', 'curator', 'академическая гребля')
}

# Пароли: password123
users_credentials = {
    'admin': 'scrypt:32768:8:1$6vH3cP1Wv6Z4wA7u$afc939fad62c9b4e5c6d...',
    'curator_ski': 'scrypt:32768:8:1$6vH3cP1Wv6Z4wA7u$afc939fad62c9b4e5c6d...',
    'curator_biathlon': 'scrypt:32768:8:1$6vH3cP1Wv6Z4wA7u$afc939fad62c9b4e5c6d...',
    'curator_row': 'scrypt:32768:8:1$6vH3cP1Wv6Z4wA7u$afc939fad62c9b4e5c6d...'
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
            # Случайный пол (для академической гребли больше женщин)
            if sport == 'академическая гребля':
                is_male = random.choice([True, False, False])
            else:
                is_male = random.choice([True, True, False])
            
            if is_male:
                first_name = random.choice(male_names)
                gender = 'М'
            else:
                first_name = random.choice(female_names)
                gender = 'Ж'
            
            last_name = random.choice(last_names)
            full_name = f"{last_name} {first_name}"
            
            # Возраст 14-18 лет
            birth_year = 2005 + random.randint(0, 4)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            birth_date = date(birth_year, birth_month, birth_day)
            
            athlete_data = {
                'id': athlete_id,
                'full_name': full_name,
                'birth_date': birth_date.strftime('%Y-%m-%d'),
                'sport': sport,
                'gender': gender,
                'region': random.choice(regions),
                'coach': f"Тренер {random.choice(['А', 'Б', 'В'])}",
                'contact_phone': f"+7{random.randint(9000000000, 9999999999)}",
                'physical_data': generate_physical_data(sport, gender, is_male),
                'medical_data': generate_medical_data(),
                'psychological_data': generate_psychological_data(),
                'competition_results': generate_competition_results(sport)
            }
            
            athletes.append(Athlete(athlete_data))
            athlete_id += 1
    
    return athletes

def generate_physical_data(sport, gender, is_male):
    # Базовые параметры в зависимости от спорта и пола
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
    
    return {
        'vo2max': round(random.uniform(*vo2max_range), 1),
        'max_strength': random.randint(*strength_range),
        'lean_body_mass': round(random.uniform(*lean_mass_range), 1),
        'anaerobic_threshold': round(random.uniform(3.5, 6.5), 1),
        'resting_hr': random.randint(45, 65),
        'max_hr': random.randint(185, 205),
        'stroke_volume': random.randint(80, 130)
    }

def generate_medical_data():
    blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    return {
        'blood_type': random.choice(blood_types),
        'last_medical_check': (date.today() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
        'injuries': random.choice(['Нет', 'Легкое растяжение', 'Старая травма колена', 'Нет']),
        'recommendations': random.choice(['Допущен без ограничений', 'Ограничение нагрузок 20%', 'Допущен']),
        'doctor_notes': 'Регулярные медицинские осмотры'
    }

def generate_psychological_data():
    return {
        'motivation': random.randint(7, 10),
        'stress_resistance': random.randint(6, 10),
        'concentration': random.randint(7, 10),
        'teamwork': random.randint(6, 10),
        'discipline': random.randint(8, 10),
        'assessment_date': (date.today() - timedelta(days=random.randint(0, 60))).strftime('%Y-%m-%d')
    }

def generate_competition_results(sport):
    competitions = []
    
    if sport == 'лыжные гонки':
        events = ['10 км классика', '15 км свободный стиль', 'Спринт', 'Эстафета']
        places = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    elif sport == 'биатлон':
        events = ['Спринт 10 км', 'Гонка преследования', 'Индивидуальная гонка', 'Эстафета']
        places = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    else:  # академическая гребля
        events = ['Одиночка', 'Двойка парная', 'Четверка парная', 'Восьмерка']
        places = [1, 2, 3, 4, 5, 6]
    
    for i in range(random.randint(3, 8)):
        competition_date = (date.today() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        competitions.append({
            'date': competition_date,
            'competition': f'Чемпионат {random.choice(["области", "федерального округа", "России"])}',
            'event': random.choice(events),
            'place': random.choice(places),
            'result': f'Результат: {random.randint(75, 98)} баллов'
        })
    
    return sorted(competitions, key=lambda x: x['date'], reverse=True)

# Инициализация данных
athletes_db = generate_mock_athletes()
