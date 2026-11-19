import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')
    DISK_TOKEN = os.getenv('')  # надо понять что за токен
