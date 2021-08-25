class Config:
    # General Configs
    TESTING = False
    DEBUG = False
    PORT = 5000

    # Database Configs
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../pos.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
