# store
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
## Создание авторизированного пользователя
## Создание супер пользователя
## Документация Swagger

## Запуск тестов
