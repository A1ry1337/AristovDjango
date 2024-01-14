import os
import sys
from datetime import datetime
import pandas as pd

# Получите путь к текущему скрипту
script_path = os.path.dirname(os.path.realpath(__file__))

# Добавьте путь к корневому каталогу проекта Django в sys.path
project_path = os.path.abspath(os.path.join(script_path, "..", ".."))
sys.path.append(project_path)

# Установите переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")

# Вызовите setup() для настройки Django
import django
django.setup()

from main.models import Vacancy


def convert_currency(amount, currency_from, currency_to, exchange_rates):
    if currency_from == "RUR":
        return amount
    elif currency_to == "RUR" and currency_from in exchange_rates:
        return amount / exchange_rates[currency_from]
    else:
        return None


def import_data_from_csv(file_path, currency_file_path):
    # Загрузка данных из CSV-файла в DataFrame
    df = pd.read_csv(file_path, dtype={'key_skills': str})  # Указываем, что 'key_skills' должен быть строкового типа

    # Загрузка курсов валют из CSV-файла
    exchange_rates_df = pd.read_csv(currency_file_path, parse_dates=['date'], dayfirst=True)
    exchange_rates = {}
    for index, row in exchange_rates_df.iterrows():
        exchange_rates[row['date'].strftime('%m/%d/%Y')] = row.to_dict()

    # Итерация по строкам DataFrame и добавление записей в базу данных
    for _, row in df.iterrows():
        data = {
            'name': row['name'],
            'key_skills': str(row['key_skills']).split(',') if not pd.isnull(row['key_skills']) else [],
            # Преобразуем в строку перед split
            'salary_currency': row['salary_currency'],
            'area_name': row['area_name'],
            'published_at': datetime.strptime(row['published_at'], '%Y-%m-%dT%H:%M:%S%z'),
        }

        # Расчет среднего значения для зарплаты
        if not pd.isnull(row['salary_from']) and not pd.isnull(row['salary_to']):
            data['salary'] = (float(row['salary_from']) + float(row['salary_to'])) / 2
        elif not pd.isnull(row['salary_from']):
            data['salary'] = float(row['salary_from'])
        elif not pd.isnull(row['salary_to']):
            data['salary'] = float(row['salary_to'])
        else:
            data['salary'] = None

        # Заполнение поля time из published_at
        data['time'] = data['published_at']

        # Конвертация валюты
        exchange_rate_date = data['published_at'].strftime('%m/%d/%Y')
        if data['salary_currency'] != "RUR" and exchange_rate_date in exchange_rates:
            exchange_rate = exchange_rates[exchange_rate_date]
            converted_salary = convert_currency(data['salary'], data['salary_currency'], "RUR", exchange_rate)
            if converted_salary is not None:
                data['salary'] = converted_salary
                data['salary_currency'] = "RUR"
            else:
                continue  # Пропускаем вакансию, если не удалось конвертировать валюту
        elif data['salary_currency'] == "RUR":
            pass  # Уже в RUR
        print(data)
        vacancy = Vacancy(**data)
        vacancy.save()


if __name__ == "__main__":
    # Замените на актуальные пути к файлам
    csv_file_path = project_path + '\\static\\analytics\\vacancies.csv'
    currency_file_path = project_path + '\\static\\analytics\\currency.csv'
    import_data_from_csv(csv_file_path, currency_file_path)
