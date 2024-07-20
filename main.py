from src.hh_api import HeadHunterAPI
import psycopg2
from src.db_manager import DBManager
from src.utils import create_db, insert_data
from config import config

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

params = config()
vacancies = HeadHunterAPI().load_vacancies(companies)

bd_name = 'best_vacancies'
create_db(bd_name, params)
conn = psycopg2.connect(dbname=bd_name, **params)

insert_data(conn, vacancies)


def main():
    # Инициализация менеджера базы данных
    db_manager = DBManager(bd_name)
    while True:
        print(f'Выберите запрос либо введите слово "стоп": \n'
              f'1 - Список всех компаний и количество вакансий у каждой компании\n'
              f'2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на '
              f'вакансию\n'
              f'3 - Средняя зарплата по вакансиям\n'
              f'4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
              f'5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n')
        user_request = input()
        if user_request == '1':
            companies_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список всех компаний и количество вакансий у каждой компании: {companies_vacancies_count}")
        elif user_request == '2':
            vacancy_list = db_manager.get_all_vacancies()
            print(f"Cписок всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию: "
                  f"{vacancy_list}")
        elif user_request == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплату по вакансиям: {avg_salary}")
        elif user_request == '4':
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print(f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям: "
                  f"{vacancies_with_higher_salary}")
        elif user_request == '5':
            user_input = input(f'Введите слово: ')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input)
            print(f"список всех вакансий, в названии которых содержатся {user_input}: {vacancies_with_keyword}")
        elif user_request == 'стоп':
            break
        else:
            print(f"Введён неверный запрос")


if __name__ == "__main__":
    main()
