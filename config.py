import os


class Config:
    # General Configs
    TESTING = True
    DEBUG = True
    PORT = 5012

    # Database Configs
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../pos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
