[![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/hidden_coding)

[![Static Badge](https://img.shields.io/badge/Telegram-Chat-yes?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/hidden_codding_chat)

[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/muskempire_bot/game?startapp=hero6695971335)

# Бот для [ShitCoinBot](https://t.me/ShitCoinTap_Bot/Game?startapp=0xyoilTXk9NZ4qOcp6E2tg)

![img1](.github/images/start.png)

# Делает все
1. Тапает

## Функционал


| Функция                                 | Поддерживается |
|-----------------------------------------|:--------------:|
| Многопоточность                         |       ✅        |
| Привязка прокси к сессии                |       ✅        |
| Задержка перед запуском каждой сессии   |       ✅        |
| Автоматические тапы                     |       ✅        |
| Docker                                  |       ✅        |

## Настройки

| Опция                 | Описание                                                                                  |
|-----------------------|-------------------------------------------------------------------------------------------|
| **API_ID / API_HASH** | Данные платформы для запуска сессии Telegram                                              |
| **TAPS_ENABLED**      | Тапы включены дефолт `True` возможно(`False`)                                             |
| **RANDOM_SLEEP_TIME** | Время сна после завершения всех действий бота дефолт `[1300, 1700]`                       |
| **REF_ID**            | Время сна после завершения всех действий бота дефолт `[1300, 1700]`                       |

**API_ID** и **API_HASH** вы можете получить после создания приложения
на [my.telegram.org/apps](https://my.telegram.org/apps)

## Быстрый старт

### Windows

1. Убедитесь, что у вас установлен **Python 3.10** или более новая версия.
2. Используйте `INSTALL.bat` для установки, затем укажите ваши API_ID и API_HASH в .env
3. Используйте `START.bat` для запуска бота (или в консоли: `python main.py`)

### Linux

1. Клонируйте репозиторий: `git clone https://github.com/paveL1boyko/MuskEmpireBot.git && cd MuskEmpireBot`
2. Выполните установку: `chmod +x INSTALL.sh START.sh && ./INSTALL.sh`, затем укажите ваши API_ID и API_HASH в .env
3. Используйте `./START.sh` для запуска бота (или в консоли: `python3 main.py`)

## Запуск в Docker

```
$ git clone https://github.com/paveL1boyko/MuskEmpireBot.git
$ cd MuskEmpireBot
$ cp .env-example .env
$ nano .env # укажите ваши API_ID и API_HASH, остальное можно оставить по умолчанию
```

### Docker Compose (рекомендуется)

```
$ docker-compose run bot -a 1 # первый запуск для авторизации (переопределяем аргументы)
$ docker-compose start # запуск в фоновом режиме (аргументы по умолчанию: -a 2)
```

### Docker

```
$ docker build -t muskempire_bot .
$ docker run --name MuskEmpireBot -v .:/app -it muskempire_bot -a 1 # первый запуск для авторизации
$ docker rm MuskEmpireBot # удаляем контейнер для пересоздания с аргументами по умолчанию
$ docker run -d --restart unless-stopped --name MuskEmpireBot -v .:/app muskempire_bot # запуск в фоновом режиме (аргументы по умолчанию: -a 2)
```

## Ручная установка

Вы можете скачать [**Репозиторий**](https://github.com/paveL1boyko/MuskEmpireBot) клонированием на вашу систему и установкой
необходимых зависимостей:

```
$ git clone https://github.com/paveL1boyko/MuskEmpireBot.git
$ cd MuskEmpireBot

# Linux
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ cp .env-example .env
$ nano .env # укажите ваши API_ID и API_HASH, остальное можно оставить по умолчанию
$ python3 main.py

# Windows (сначала установите Python 3.10 или более новую версию)
> python -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt
> copy .env-example .env
> # укажите ваши API_ID и API_HASH, остальное можно оставить по умолчанию
> python main.py
```

Также для быстрого запуска вы можете использовать аргументы:

```
$ python3 main.py --action (1/2)
# или
$ python3 main.py -a (1/2)

# 1 - создать сессию
# 2 - запустить бот
```

## Запуск  бота в фоновом режиме (Linux)

```
$ cd MuskEmpireBot

# с логированием
$ setsid venv/bin/python3 main.py --action 2 >> app.log 2>&1 &

# без логирования
$ setsid venv/bin/python3 main.py --action 2 > /dev/null 2>&1 &

# Теперь вы можете закрыть консоль и бот продолжит свою работу.
```

### Найти процесс бота

```
$ ps aux | grep "python3 main.py" | grep -v grep
```
