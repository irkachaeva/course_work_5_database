import requests


class HHemployer:

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'page': 0, 'per_page': 100}
        self.employer_id = []

    def load_employer(self):
        """
        Загрузка данных через API c сайта HH
        :param employer_id: id работодателей - список
        :return: список вакансий с сайта
        """

        while self.params['page'] != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            data = response.json()
            employers = data.get('items', [])
            self.employer_id.extend(employers)
            self.params['page'] += 1

        return self.employer_id
