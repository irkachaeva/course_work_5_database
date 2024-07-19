import psycopg2


def create_db(name, params):
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""
    try:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f'DROP DATABASE IF EXISTS {name}')
        cur.execute(f'CREATE DATABASE {name}')
        conn.close()

        conn = psycopg2.connect(dbname=name, **params)
        with conn.cursor() as cur:
            cur.execute(f'CREATE TABLE IF NOT EXISTS employers '
                        f'(company_id int, '
                        f'company_name varchar(100), '
                        f'company_url varchar (100))')
        with conn.cursor() as cur:
            cur.execute(f'CREATE TABLE IF NOT EXISTS vacancies '
                        f'(company_id int, '
                        f'company_name varchar (100), '
                        f'job_title varchar(100), '
                        f'link_to_vacancy varchar(100), '
                        f'salary_from int, '
                        f'currency varchar(10), '
                        f'description text, '
                        f'requirement text)')
        conn.commit()
        conn.close()

        return "База данных и таблицы успешно созданы."

    except Exception as e:
        return f"Произошла ошибка: {e}"


def insert_data(conn, vacancies):
    """Сохранение данных о компаниях и вакансиях в БД pgAdmin. """

    with conn.cursor() as cur:
        for item in vacancies:
            employer_data = item['employer']
            cur.execute(
                """
                INSERT INTO employers (company_id, company_name, company_url) VALUES (%s, %s, %s)
                """,
                (employer_data['id'],
                 employer_data['name'],
                 employer_data['alternate_url']
                 )
            )
            if item['salary'] is None:
                salary_from = 0
                currency = 0
            else:
                if item['salary'].get('from') is None:
                    salary_from = 0
                else:
                    salary_from = int(item['salary'].get('from'))
                currency = item['salary'].get('currency')
            cur.execute(
                """
                INSERT INTO vacancies (company_name, job_title, link_to_vacancy, salary_from, currency, description, requirement)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (employer_data['name'],
                 item['name'],
                 item['apply_alternate_url'],
                 salary_from,
                 currency,
                 item['snippet'].get('responsibility'),
                 item['snippet'].get('requirement')))
        conn.commit()
        conn.close()


def get_vacancies(vacancies):
    list_vacancies = []
    for item in vacancies:
        company_id = int(item['employer']['id'])
        company_name = item['employer']['name']
        company_url = item['employer']['alternate_url']
        job_title = item['name']
        link_to_vacancy = item['apply_alternate_url']
        if item['salary'] is None:
            salary_from = 0
            currency = 0
        else:
            salary_from = item['salary'].get('from')
            currency = item['salary'].get('currency')
        description = item['snippet'].get('responsibility')
        requirement = item['snippet'].get('requirement')
        item = [company_id, company_name, company_url, job_title, link_to_vacancy, salary_from, currency, description, requirement]
    list_vacancies.append(item)
    return list_vacancies
