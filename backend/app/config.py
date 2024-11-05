class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/canteen_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'