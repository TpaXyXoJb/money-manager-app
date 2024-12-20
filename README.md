README
=====================

Этот README документирует все шаги, необходимые для создания и запуска веб-приложения.


### Настройки Docker

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/engine/install/ubuntu/)

##### Команды для запуска docker без sudo (для локалки)

* `sudo groupadd docker`
* `sudo gpasswd -a ${USER} docker`
* `newgrp docker`
* `sudo service docker restart`

##### Проверка работоспособности docker без sudo

* `docker run hello-world`

### Настройки Docker-compose

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/compose/install/)

##### Команда для запуска docker-compose без sudo (для локалки)

* `sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose`

### Создание окружения для локальной разработки

##### Копирование файлов репозитория на локальную машину

```
$ git clone https://gitlab.com/<название репозитория>.git
$ cd <название репозитория>
```

##### Создание и запуск контейнеров

```
$ docker-compose up 
```
_**Примечание:** остановка контейнеров по CRTL+C._

##### Инициализация базы данных (применение миграций)
```
$ docker-compose exec server python manage.py makemigrations
$ docker-compose exec server python manage.py migrate
```
_**Примечание:** если контейнеры запущены не в режиме демона, ввод команд производится в новом терминале._

##### Создание пользователя (superuser)
```
$ docker-compose exec server python manage.py createsuperuser
```
_**Примечание:** при выполнении данной команды вам необходимо ввести данные нового пользователя. Обязательно сохраните эти данные._

##### Проверка запуска контейнеров

```
$ docker-compose ps
                    Name                                   Command               State                    Ports                  
---------------------------------------------------------------------------------------------------------------------------------
miniproject-stub-python_db_1       docker-entrypoint.sh postgres    Up      5432/tcp                                
miniproject-stub-python_server_1   python manage.py runserver ...   Up      0.0.0.0:8000->8000/tcp,:::8000->8000/tcp

```

##### Проверка доступности панели администратора

Открыть в браузере страницу [http://0.0.0.0:8000/admin/](http://0.0.0.0:8000/admin/) и выполнить вход в систему с учетными данными пользователя (superuser)

##### Проверка доступности api

Открыть в браузере страницу [http://localhost:8000/api/users/me/](http://localhost:8000/api/users/me/) и проверить, что страница с документацией по api отображается корректно.

---------------------

### Разработка

##### Справка по командам docker-compose

_**Примечание:** в зависимости от способа установки, версии docker-compose могут иметь различие в вводе основной команды ("docker-compose" или "docker compose") - [подробности](https://docs.docker.com/compose/#compose-v2-and-the-new-docker-compose-command)._ 

Запустить контейнеры в режиме демона
```
$ docker-compose up -d
```
Подключиться к запущенному контейнеру сервера
```
$ docker-compose exec server /bin/bash
```
Создать файл миграции
```
$ docker-compose exec server python manage.py makemigrations
```
Применить миграции
```
$ docker-compose exec server python manage.py migrate
```
Остановить контейнеры
```
$ docker-compose stop
```
Пересобрать и запустить контейнеры
```
$ docker-compose up --build
```
Выполнить сборку контейнера сервера
```
$ docker-compose build server
```
[Документация по командам docker-compose](https://docs.docker.com/engine/reference/commandline/compose/)

### Развертывание веб-приложения на сервере (работа с nginx)

##### Команды

* `docker-compose -f docker-compose.prod.yml build` - сборка контейнеров 
* `docker-compose -f docker-compose.prod.yml up` - запуск контейнеров 

### Примечания

* При разработке можно убрать или добавить зависимости
    
    `docker-compose run server poetry remove req_name`
    `docker-compose run server poetry add req_name`
