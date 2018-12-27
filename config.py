# -*- coding: utf-8 -*-

from enum import Enum

token = "********************************"
db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_NAME = "1"
    S_ENTER_AGE = "2"
    S_SEND_PHONE= "3"
    S_SEND_MAIL= "4"
    S_ENTER_JOB = "5"
    S_LIKE = "6"
    S_KOMUN = "7"
    S_HOBBY = "8"
    S_DISTRICT= "9"
    S_GRAF = "10"
    S_EDUCATION= "11"