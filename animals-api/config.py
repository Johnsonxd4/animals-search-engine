import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:password@database:5432')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BROKER_HOST = 'broker'
    BROKER_USERNAME = 'guest'
    BROKER_PASSWORD = 'guest'