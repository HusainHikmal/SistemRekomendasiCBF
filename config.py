import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'instance/smartphones.db')
    MODEL_NAME = os.getenv('EMBEDDING_MODEL', 'all-mpnet-base-v2')