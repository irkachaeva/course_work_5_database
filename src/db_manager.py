import psycopg2
from config import config


class DBManager:

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = psycopg2.connect(dbname=self.db_name, **config())

    def get_companies_and_vacancies_count(self):
        """
        :return: получает список всех компаний и количество вакансий у каждой компании.
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT vacancies.company_name, COUNT(vacancies.job_title) AS vacancies_count
                    FROM vacancies
                    GROUP BY vacancies.company_name
                    """)
                data = cursor.fetchall()
        return print(data)

    def get_all_vacancies(self):
        """
        :return:  получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию.
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT vacancies.company_name, job_title, salary_from, link_to_vacancy 
                    FROM vacancies  
                    """)
                data = cursor.fetchall()
        return data

    def get_avg_salary(self):
        """
        :return: получает среднюю зарплату по вакансиям.
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT AVG(salary_from) 
                    FROM vacancies
                    """)
                data = cursor.fetchall()
        return data

    def get_vacancies_with_higher_salary(self):
        """
        :return: получает список всех вакансий, у которых зарплата выше
        средней по всем вакансиям.
        """

        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT vacancies.company_name, job_title, salary_from, link_to_vacancy 
                    FROM vacancies 
                    WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) 
                    ORDER BY salary_from
                    """)
                data = cursor.fetchall()
        return data

    def get_vacancies_with_keyword(self, keyword):
        """
        :return: получает список всех вакансий, в названии
        которых содержатся переданные в метод слова, например python.
        """
        with self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT * FROM vacancies WHERE LOWER(job_title) LIKE '%{keyword}%'"
                )
                data = cursor.fetchall()
        return data
