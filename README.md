# store
API для магазина продуктов.
## Локальный запуск проекта
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com:alina-afsatarova/store.git
```
```
cd store
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
```
```
source venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
cd grocery_store
```
```
python manage.py migrate
```
Загрузить данные из фикстуры db.json (в фикстуре подготовлены данные для загрузки категорий, подкатегорий и продуктов).
```
python manage.py loaddata db.json
```
Запустить проект:
```
python manage.py runserver
```
## Создание суперпользователя и админка
Создайте суперпользователя командой в терминале:
```
python manage.py createsuperuser
```
Админ-зона Django доступна по адресу: `http://127.0.0.1:8000/admin/`.
## Документация Swagger
Документация для проекта доступна по адресу: `http://127.0.0.1:8000/docs/`.
## Запуск тестов
Для запуска тестов перейдите в директорию:
```
cd store/grocery_store
```
и выполните команду:
```
pytest
```
