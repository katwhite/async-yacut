from datetime import datetime
from random import choices

from flask import url_for

from yacut import db
from .constants import ALLOWED_CHARS, MAX_GENERATION_ATTEMPTS
from .constants import MAX_LENGTH_ORIGINAL, MAX_LENGTH_SHORT, SHORT_ID_LENGTH


class URLMap(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @classmethod
    def check_unique(cls, short_id):
        """Проверяет уникальна ли ссылка в бд
        Возвращает True если такой ссылки нет в бд
        Возвращает False если ссылка не уникальна"""
        return not bool(cls.query.filter_by(short=short_id).first())

    @classmethod
    def get_unique_short_id(cls):
        """Формирует короткие идентификаторы переменной длины
        с ограниченным количеством попыток"""
        for _ in range(MAX_GENERATION_ATTEMPTS):
            # Генерируем 6 случайных символов
            short_id = ''.join(choices(ALLOWED_CHARS, k=SHORT_ID_LENGTH))
            if cls.check_unique(short_id):
                return short_id
        raise RuntimeError('Не удалось сгенерировать уникальный ID')

    def from_dict(self, data):
        if 'url' in data:
            self.original = data['url']
        if 'custom_id' in data:
            self.short = data['custom_id']

    def to_dict(self):
        """формирует ответ для апи"""
        return {
            'url': self.original,
            'short_link': url_for(
                'redirect_view', short_id=self.short, _external=True
            )
        }
