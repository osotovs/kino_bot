KinoLis
=======

KinoLis - это бот, который расскажет Вам о сеансах кино в кинотеатрах Вашего города.

Установка
---------

Создайте виртуальное окружение и активируйте его. Затем в выполните:

.. code-block:: text

    pip install -r requirements.txt

Настройка
---------

Создайте файл settings.py и добавьте следующие настройки:

.. code-block:: python

    API_KEY = "API ключ, который выдал Вам BotFather"          

    PROXY = {'proxy_url': 'socks5://ВАШ ПРОКСИ:1080',
	    'urllib3_proxy_kwargs':{'username':'ЛОГИН','password':'ПАРОЛЬ'}}

    USER_EMOJI = [":smiley_cat:", ":smiling_imp:", ":panda_face:", ":dog:",":smirk_cat:",
        " :joy_cat:","/play rumble"]

Запуск
------

.. code-block:: python

    python3 bot.py