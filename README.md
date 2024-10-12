# YaCut
### О проекте.
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис. 
___
### При создании проекта использовалось:
- язык программирования Python 3;
- фреймворк Flask.
___
Чтобы развернуть проект необходимо следующие:
- Клонировать репозиторий со своего GitHub и перейти в него в командной строке:

```
git clone git@github.com:levisserena/yacut.git
```
>*Активная ссылка на репозиторий под этой кнопкой* -> [КНОПКА](https://github.com/levisserena/yacut)
- Перейдите в папку с проектом:
```
cd yacut
```
- Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

- Запустите сервер:

```
flask run --app=yacut
```
___
### API проекта.
В папке `postman_collection` есть коллекция запросов, с которой можно ознакомится, например, в программе [Postman](https://www.postman.com/).<br>
В корне проекта есть файл `openapi.yml` - Подробное описание работы API проекта. Ознакомится можно, загрузив файл, например, на сайте [Swagger Editor](https://editor.swagger.io/).<br>

Примеры:<br>
___
Эндпоинт:
```
http://127.0.0.1:5000/api/id/
```
POST-запрос (JSON):
```
{
  "url": "string",
  "custom_id": "string"
}
```
Ответ (JSON):
```
{
  "url": "string",
  "short_link": "string"
}
```
___
Эндпоинт:
```
http://127.0.0.1:5000/api/id/{short_id}/
```
Ответ на GET-запрос(JSON):
```
{
  "url": "string"
}
```
___
### Информация об авторах.
Акчурин Лев Ливатович.<br>Студент курса Яндекс Практикума Python-разработчик плюс.<br>
[Страничка GitHub](https://github.com/levisserena)
___
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)