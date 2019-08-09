# Quiz bot

Bot quiz for Telegram and VK

Commands for Telegram's bot:

1. /start – start quiz
2. /help – about this bot
3. /exit, /cancel – quit game

To start in VK, type начать, старт, start

## How to install

1. Create a bot in Telegram @via BotFather, and get it API token.
2. Create redis account in [Redislabs](https://redislabs.com/), and after that create [cloud database](https://docs.redislabs.com/latest/rc/quick-setup-redis-cloud/) (you can choose free plan).
Get your endpoint database url and port.
3. Create VK's group, allow it send messages, and get access token for it.

Create .env file in the root directory and fill it:

```.env
TG_TOKEN=your tg bot token
REDIS_DATABASE=redis database endpoint without port
REDIS_PORT=redis database port
REDIS_PSWRD=redis password
VK_TOKEN=vk access token
```

Python3 must be already installed.

Should use virtual env for project isolation.

Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

## How add new questions for bots

To create new questions, you must create a folder into the root directory and call it `quiz-questions`. After that, create new txt files with `KOI8-R` encoding and write into it new questions and answers separating them two spaces.

File for example:

```txt
Вопрос 1:
С одним советским туристом в Марселе произошел такой случай. Спустившись
из своего номера на первый этаж, он вспомнил, что забыл закрутить кран в
ванной. Когда он поднялся, вода уже затопила комнату. Он вызвал
горничную, та попросила его обождать внизу. В страхе он ожидал расплаты
за свою оплошность. Но администрация его не ругала, а, напротив,
извинилась сама перед ним. За что?

Ответ:
За то, что не объяснила ему правила пользования кранами.


Вопрос:
Средневековый обычай: рыцаря, совершившего поступок, порочащий честь,
заставляли пробежать некоторую дистанцию, положив ему на спину седло,
мешок с камнями или... Кого?

Ответ:
Собаку. Отсюда, по одной из версий, происходит выражение "навешать
собак".


Вопрос:
Цветы этого декоративного растения семейства крестоцветных могут иметь
самую разнообразную окраску, хотя судя по его названию, они обязательно
должны быть белыми. Назовите это растение.

Ответ:
Левкой (от греческого leukos - белый).
```

Or you can [download questions](http://dvmn.org/media/modules_dist/quiz-questions.zip) and unzip archive in the root.

## How to use

To run Telegram bot:

```bash
python tg_bot.py
```

To run VK bot:

```bash
python vk_bot.py
```
