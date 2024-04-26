# Установка
Склонировать репозиторий

    https://github.com/DinarDi/rlt-test.git

Установить зависимости

    poetry install

Поднять docker container

    docker-compose up

Узнать id контейнера

    docker ps

Войти в контейнер

    docker exec -it {id} bash

Загрузить dump

    mongorestore --username {username} --password {password} /backup/sampleDB/*.bson

Запуск бота из

    bot/main.py
