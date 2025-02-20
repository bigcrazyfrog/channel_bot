import json
import requests

import codecs

params = {"text": "Python OR Питон", "search_field": "name", "schedule": "remote"}


def get_python_vacancies():
    responce = requests.get('https://api.hh.ru/vacancies', params=params)
    responce.raise_for_status()

    res = []

    for page in range(min(responce.json()["pages"], 20)):
        responce = requests.get('https://api.hh.ru/vacancies', params={"text": "Python OR Питон", "search_field": "name", "schedule": "remote", "page": page})
        responce.raise_for_status()

        res.extend(responce.json()["items"])

    return res


def to_file():
    print("Запись вакансий в файл")
    with codecs.open("vacancies.txt", "w", encoding="utf-8") as file:
        json.dump(get_python_vacancies(), file)
