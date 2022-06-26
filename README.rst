Телеграм бот.
--------------
Описание.
~~~~~~~~~~~~~~
Реализовано динамическое формирование инлайн-клавиатуры.

Запуск.
~~~~~~~~~~~~~~
* С помощью менеджера зависимостей poetry::

    pip install poetry
    poetry install
    poetry run hwb/app.py
* Через Docker::
  
    sudo apt update
    sudo apt install docker
    chmod +x init.sh
    ./init.sh

Библиотеки и фреймворки.
~~~~~~~~~~~~~~~~~~~~~~~~~
* aiogram
* rich
