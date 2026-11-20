from datetime import datetime

from yacut import db


class URLMap(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)  # поле для оригинальной длинной ссылки;
    short = db.Column(db.String(16), unique=True, nullable=False)  # поле для короткого идентификатора;
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def from_dict(self, data):
            # API присылает 'url', а в модели это поле 'original'
            if 'url' in data:
                self.original = data['url']
            # API присылает 'custom_id', а в модели это поле 'short'
            if 'custom_id' in data:
                self.short = data['custom_id']
