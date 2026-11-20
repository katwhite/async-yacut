import string

# Длины полей
MAX_LENGTH_ORIGINAL = 256
MAX_LENGTH_SHORT = 16
SHORT_ID_LENGTH = 6

# Для генерации ID
ALLOWED_CHARS = string.ascii_letters + string.digits
MAX_GENERATION_ATTEMPTS = 1000

# Регулярное выражение для custom_id
SHORT_ID_PATTERN = r'^[a-zA-Z0-9]+$'