# Лабортаорная работа №3: Внедрение Dependency Injection и SQLAlchemy в Litestar

## Цель работы
Цель работы: Освоить принципы Dependency Injection и интеграцию SQLAlchemy ORM в веб-приложении на базе фреймворка Litestar написав CRUD.

## Состав проекта:
* app/repositories/user_repository.py: Репозиторий для взаимодействия с БД
* app/services/user_service.py: Сервис для реализации бизнес логики приложения
* app/controllers/user_controller.py: Контроллер для обработки запросов и валидации данных
* app/main.py: Главное стартовое приложение

## Инструкция по запуску
* uv pip install -r requirements.txt
* alembic upgrade head
* В app/main.py указать DATABASE_URL или указать соответсвующую переменную в окружении проекта
* (Опционально) выполнить: python lab2.py
* python app/main.py
* http://127.0.0.1:8000/users Для get запросов к api пользователей.

Для остальных следует использовать средства разработки и отпарвки сообщений
