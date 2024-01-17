import csv
from datetime import datetime
from djangoProject.settings import BASE_DIR
from collections import Counter

class VacancyManager:
    def __init__(self):
        self.vacancies = []

# Чтение вакансий из файла
    def read_from_csv(self, csv_file):
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                vacancy = Vacancy(row)
                self.vacancies.append(vacancy)

# Получаем все вакансии
    def get_all_vacancies(self):
        return self.vacancies

# Удаляем вакансии где есть пустые поля
    def remove_empty_vacancies(self):
        self.vacancies = [vacancy for vacancy in self.vacancies if vacancy.is_valid()]
        return self

# Удаляем вакансии которые не относятся к нашей профессии
    def remove_non_matching_vacancies(self, keywords=(
                'web develop', 'веб разработчик', 'web разработчик', 'web programmer', 'web программист',
                'веб программист', 'битрикс разработчик', 'bitrix разработчик', 'drupal разработчик', 'cms разработчик',
                'wordpress разработчик', 'wp разработчик', 'joomla разработчик', 'drupal developer', 'cms developer',
                'wordpress developer', 'wp developer', 'joomla developer')
                ):
        self.vacancies = [vacancy for vacancy in self.vacancies if
                          any(keyword.lower() in vacancy.name.lower() for keyword in keywords)]
        return self

    @staticmethod
    def load_currency_rates(currency_rates_file):
        currency_rates = {}
        with open(currency_rates_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                date_str = row['date']
                currency_rates[date_str] = {currency: float(row[currency]) if row[currency] else None for currency in
                                            row.keys() if currency != 'date'}
        return currency_rates

    @staticmethod
    def get_currency_rate(currency_rates, currency, published_at):
        date_str = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%S%z').strftime('%d/%m/%Y')
        return currency_rates.get(date_str, {}).get(currency)

# Все зарплаты переводит в рубли
    def update_salary_in_rubles(self, currency_rates_file=BASE_DIR / 'static/analytics/currency.csv'):
        # Загрузка курсов валют из файла
        currency_rates = self.load_currency_rates(currency_rates_file)

        # Обновление зарплат в рублях для каждой вакансии
        updated_vacancies = []
        for vacancy in self.vacancies:
            if vacancy.salary_currency != 'RUR':
                # Получение курса для указанной валюты и даты публикации вакансии
                rate = self.get_currency_rate(currency_rates, vacancy.salary_currency, vacancy.published_at)
                if rate is not None:
                    # Конвертация и форматирование зарплаты в рубли
                    vacancy.salary = format(vacancy.salary * rate, '.1f')
                    vacancy.salary_currency = 'RUR'
                    if float(vacancy.salary) < 400000:  # Удаляю фейк стаитистику
                        updated_vacancies.append(vacancy)
            else:
                if float(vacancy.salary) < 400000:  # Удаляю фейк стаитистику
                    updated_vacancies.append(vacancy)

        # Замена списка вакансий на обновленный
        self.vacancies = updated_vacancies
        return self

# Получаем словарик год - средняя зарплата
    def get_avg_salary(self):
        # Словарь для хранения динамики уровня зарплат по годам
        salary_dynamics = {}

        for vacancy in self.vacancies:
            if vacancy.salary_currency == 'RUR':
                # Получение года из даты публикации вакансии
                year = datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z').year

                # Добавление зарплаты в словарь
                salary_dynamics.setdefault(year, []).append(float(vacancy.salary))

        # Вычисление средней зарплаты для каждого года
        average_salary_dynamics = {year: sum(salaries) / len(salaries) for year, salaries in salary_dynamics.items()}

        return average_salary_dynamics

    # Метод возвращает словарь год - количество вакансий
    def get_vacancy_count_by_year(self):
        # Словарь для хранения количества вакансий по годам
        vacancy_count_by_year = Counter()

        for vacancy in self.vacancies:
            # Получение года из даты публикации вакансии
            year = datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z').year

            # Увеличение счетчика вакансий для указанного года
            vacancy_count_by_year[year] += 1

        return vacancy_count_by_year


class Vacancy:
    def __init__(self, data):
        self.name = data.get('name', '')
        self.key_skills = data.get('key_skills', [])
        self.salary = self.calculate_salary(data)
        self.salary_currency = data.get('salary_currency', '')
        self.area_name = data.get('area_name', '')
        self.published_at = data.get('published_at', '')
        self.time = data.get('time', '')

    @staticmethod
    def calculate_salary(data):
        salary_from_str = data.get('salary_from', '')
        salary_to_str = data.get('salary_to', '')

        try:
            salary_from = float(salary_from_str) if salary_from_str else None
            salary_to = float(salary_to_str) if salary_to_str else None

            if salary_from is not None and salary_to is not None:
                return (salary_from + salary_to) / 2
            elif salary_from is not None:
                return salary_from
            elif salary_to is not None:
                return salary_to
            else:
                return None
        except ValueError:
            return None

    def is_valid(self):
        return all([self.name, self.salary, self.salary_currency, self.area_name, self.published_at])

    def __repr__(self):
        key_skills_str = ''.join(self.key_skills).replace('\n', ', ') if self.key_skills else ""
        salary_info = f"{self.salary} {self.salary_currency}" if self.salary else ""
        return (f"name={self.name}, "
                f"area={self.area_name}, "
                f"salary={salary_info}, "
                f"published_at={self.published_at}, "
                f"key_skills={key_skills_str}")

    def __str__(self):
        key_skills_str = ''.join(self.key_skills).replace('\n', ', ') if self.key_skills else ""
        salary_info = f"{self.salary} {self.salary_currency}" if self.salary else ""
        return (f"name={self.name}, "
                f"area={self.area_name}, "
                f"salary={salary_info}, "
                f"published_at={self.published_at}, "
                f"key_skills={key_skills_str}")
