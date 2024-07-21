import requests


class HeadHunterAPI:
    """
    Класс для подключения к HH api  преобразования полученных данных
    """
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'employer_id': ''}
        self.vacancies_list = []

    def load_vacancies(self, employer_id):
        """
        Загрузка данных через API c сайта HH
        :param employer_id: id работодателей - список работодателей
        :return: список вакансий с сайта
        """
        for e_id in employer_id:
            self.params['employer_id'] = e_id
            response = requests.get(self.url, headers=self.headers, params=self.params)
            data = response.json()
            vacancies = data.get('items', [])
            self.vacancies_list.extend(vacancies)
        return self.vacancies_list
