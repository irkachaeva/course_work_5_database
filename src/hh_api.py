import requests


class HeadHunterAPI:

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'employer_id': '', 'page': 0, 'per_page': 100}
        self.vacancies_list = []

    def load_vacancies(self, employer_id):
        """
        Загрузка данных через API c сайта HH
        :param employer_id: id работодателей - список работодателей
        :return: список вакансий с сайта
        """
        for e_id in employer_id:

            while self.params['page'] != 20:
                self.params['employer_id'] = e_id
                response = requests.get(self.url, headers=self.headers, params=self.params)
                data = response.json()
                vacancies = data.get('items', [])
                self.vacancies_list.extend(vacancies)
                self.params['page'] += 1

        return self.vacancies_list
