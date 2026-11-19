from datetime import datetime

from yacut import db


class URLMap(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)  # поле для оригинальной длинной ссылки;
    short = db.Column(db.Text, unique=True, nullable=False)  # поле для короткого идентификатора;
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

