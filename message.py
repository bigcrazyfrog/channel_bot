

import json
import random

import requests


def get_one_vacancies(channel_name, vacancies_number=5):
    vacancies = json.load(open("vacancies.txt"))
    # print(vacancies[1])
    
    text = "❗️ **Новые вакансии Python**\n\n"

    rands = set()
    for i in range(random.randint(3, vacancies_number)):
        rands.add(random.randint(0, len(vacancies) - 1))

    success_count = 0
    errors = []
    for rand in rands:
        try:
            response = requests.get(vacancies[rand]["url"])
            response.raise_for_status()
        except Exception as e:
            errors.append(repr(e))

        s = response.json()

        if s["type"]["id"] != "open":
            continue

        text += f"▪️ **{s['name']}**\n"
        text += f"{s['employment']['name']}\n"
        if 'key_skills' in s and len(s['key_skills']) > 0:
            text += f"{' • '.join([skill['name'] for skill in s['key_skills'][:3]])}\n"

        text += f"{s['alternate_url']}"
        text += "\n\n"
        success_count += 1
    
    text += channel_name

    # text = f"❗️ **{v['name']}**\n" \
    # f"✉️ Компания - ||{v['employer']['name']}||\n" \
    # f"💸 - " \
    # f"{v['employment']['name']}\n" \
    # f"💪 Skills: {', '.join([skill['name'] for skill in s['key_skills'][:3]])}" \
    # f"\n\n{v['alternate_url']}"

    if success_count < 2:
        raise Exception(f"No vacancies - {success_count} number\n{' '.join(errors)}")

    return text
