# Космический Инстаграм
___
Данная программа производит загрузку фотографий в Instargan из:
1. <https://api.spacexdata.com/v4/launches> 
2. <https://hubblesite.org/api/v3/images>

## Как установить
[TODO: объясните пользователю, откуда брать ключи, куда их класть и как они выглядят]

Переменые `login_instagra` и `password_instagram` хранят данные для авторизации 
(_login_ и _password_ соответсвенно) в [Instagram.com](https://www.instagram.com)
и подтягивают из файла .env

>login_instagram = os.getenv('LOGIN_INSTAGRAM') 
>
>password_instagram = os.getenv('PASSWORD_INSTAGRAM')

В файле `.env` ключи записываются следующим образом:

>LOGIN_INSTAGRAM = [_login_]
>
>PASSWORD_INSTAGRAM = [_password_]
 

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть 
конфликт с Python2) для установки зависимостей:

'pip install -r requirements.txt'

##Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org.](https://dvmn.org/modules/)