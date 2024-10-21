# Simple telegram bot
Example for SPb Python meetup.

## Installation

Python 3.12

Create virtualenv, if needed.

Create `.env` in root, fill with your data:
```text
SECRET_KEY='<DJANGO_SECRET_KEY>'
TOKEN='<YOUR_TG_TOKEN>'
DEBUG='1'

```

```shell
pip install -r requirements.txt
python manage.py migrate
```

## Usage

Run polling
```shell
python manage.py polling
```

Run server
```shell
python manage.py runserver
```

Go to your bot and type '/start'

