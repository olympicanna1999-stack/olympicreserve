from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import json

class User(UserMixin):
    def __init__(self, id, username, role, sport=None):
        self.id = id
        self.username = username
        self.role = role  # 'admin', 'curator'
        self.sport = sport  # None for admin, sport type for curators
    
    @staticmethod
    def get(user_id, users_db):
        return users_db.get(user_id)

class Athlete:
    def __init__(self, data):
        self.id = data['id']
        self.full_name = data['full_name']
        self.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        self.sport = data['sport']
        self.gender = data['gender']
        self.region = data['region']
        self.coach = data['coach']
        self.contact_phone = data['contact_phone']
        
        # Физические показатели
        self.physical_data = data.get('physical_data', {})
        
        # Медицинские данные
        self.medical_data = data.get('medical_data', {})
        
        # Психологические оценки
        self.psychological_data = data.get('psychological_data', {})
        
        # Спортивные результаты
        self.competition_results = data.get('competition_results', [])
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
