import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'film_contest_secret_key_jwt_2026'
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1']
    TESTING = False
    DATABASE_URI = os.environ.get('POSTGREE_DATABASE_URL') or 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/film_contest_db'
    CORS_HEADERS = 'Content-Type'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = os.environ.get('POSTGREE_DATABASE_URL') or 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/film_contest_db'

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URL') or Config.DATABASE_URI

class FactoryConfig:
    @staticmethod
    def get_config(env: str = None):
        if not env:
            env = os.environ.get('FLASK_ENV', 'development').lower()
        if env == 'development':
            return DevelopmentConfig
        elif env == 'testing':
            return TestingConfig
        elif env == 'production':
            return ProductionConfig
        return Config
