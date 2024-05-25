from src.hh_api import HeadHunterAPI
import json
import os.path

def write_vacancies(data):
    path = os.path.join(os.getcwd(), 'data', 'employers.json')
    with open(path, "w", encoding="utf-8") as file:
        add_vacancies = []
        for vacancy in data:
            add_vacancies.append(vacancy)
        json.dump(add_vacancies, file, ensure_ascii=False, indent=4)
        return

companies = [1740,  # Яндекс
             78638,  # Тинькофф
             84585,  # Авито
             1942330,  # Пятерочка
             49357,  # Тандер (Магнит)
             2180,  # Ozon
             1272486,  # Сбермаркет
             87021,  # WILDBERRIES
             1122462,  # Skyeng
             15478  # VK
            ]

hh_e = HeadHunterAPI()
emp = hh_e.load_vacancies(companies)

write_vacancies(emp)