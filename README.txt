Для подключения к PostgreSQL используйте следующие данные:
User: postgres
Password: 5610
database: hotel_db
host: localhost
port: 5432

Для работы приложения необходимо в PgAdmin создать базу данных с именем hotel_db,
пользователя 'postgres' с паролем 5610, и дать ему необходимые права.

Если это сделать нельзя, для тестирования можно создать в корне проекта sqlite базу, и изменить в
HotelAPI/settings.py следующий код на:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'hotel_db'
    }
}

затем в терминале выполнить миграции командой 'python manage.py makemigrations'
и затем 'python manage.py migrate', после чего база будет работать.

Примечание: имя комнаты должно быть в формате int: (1, 2, ..., n)
Приложение запускается с помощью команды: python manage.py runserver
либо комбинацией клавишь Shift+F10