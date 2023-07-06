Двухнедельный спринт.

Писал auth_service.py, тесты на него. 

Базовая структура взята из проектов ранее.


## Как запустить?

- Проверить все ручки через Swagger: Запустите prod приложение командой `make prod`.

- Проверить все тесты `pytest`, подробнее в файле [tests/README.md](tests/README.md).


- Также для ручной проверки задания требуется создание пользователя в командой строке:
```
# make dev
# make create-super LOGIN=superadmin PASSWORD=secret FIRSTNAME=Super LASTNAME=Admin
```
или просто используя virtualenv:
```
# python -m cli --login superadmin --password secret --firstname Super --lastname Admin
```
- для минимальной работы ендпоинтов Role и User необходимо создать роль с access значением `role_manage,role_admin` или использовать суперпользователя созданного через командную строку
    - для API ендпоинтов `role/*` используется access `role_manage`
    - для API ендпоинтов `user/*` используется access `role_admin`

### Swagger

При запуске сервера через `make dev ` или `make prod`, swagger доступен по данному пути:

http://127.0.0.1/api/openapi

### минимальные требования для запуска проекта

- необходимо наличие утилиты make

#### установка `make` на macOS

```
brew install make
```

#### установка `make` на deb-операционные системы

```
apt install make
```

### для **dev**

- redis доступен на локальной машине по сокету `127.0.0.1:6379`
- postgres доступен на локальной машине по сокету `127.0.0.1:5432`
- папка с исходниками смонтирована в контейнер fastapi и при изменении uvicorn перезапускает сервер
- fastapi доступен на локальной машине по сокету `127.0.0.1:80`

```
make dev
```

### другие команды доступные для дебага:

#### консоль redis-cli:

```
make redis-cli
```

#### консоль python в контейнере fastapi:

```
make fastapi-console
```

---

### просмотр всех логов в tail режиме (выход ctrl+c или command+c):

```
make logs
```
