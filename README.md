# Космический Инстаграм

Данная программа производит загрузку фотографий в Instargan из:
1. <https://api.spacexdata.com/v4/launches> 
2. <https://hubblesite.org/api/v3/images>

## Как установить
Программа запускается командой:

`./python main.py`

Переменые `login_instagra` и `password_instagram` хранят данные для авторизации 
(_login_ и _password_ соответсвенно) в [Instagram.com](https://www.instagram.com)
и подтягивают из файла .env 

```python
login_instagram = os.getenv('LOGIN_INSTAGRAM')
password_instagram = os.getenv('PASSWORD_INSTAGRAM')
```
Файл `.env` располагается в корневом катологе 
```
├── .env
└── main.py
```

В файле `.env` ключи записываются следующим образом:

```python
LOGIN_INSTAGRAM = [login]
PASSWORD_INSTAGRAM = [password]
```
 

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть 
конфликт с Python2) для установки зависимостей:

`pip install -r requirements.txt`

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org.](https://dvmn.org/modules/)