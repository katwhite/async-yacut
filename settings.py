import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
    API_HOST = 'https://cloud-api.yandex.net/'
    API_VERSION = 'v1'
    REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
    AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}
