import requests
from datetime import datetime, timedelta
import csv
import xml.etree.ElementTree as ET
from djangoProject.settings import BASE_DIR


# Функция для выполнения SOAP-запроса с повторными попытками
def get_currency_rate_with_retry(date_str, currency_code, max_retries=3):
    formatted_date = datetime.strptime(date_str, '%d/%m/%Y').strftime('%d.%m.%Y')
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={formatted_date}'

    for _ in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка наличия ошибок при запросе

            xml_data = ET.fromstring(response.content)

            # Попробуйте сначала найти валюту с кодом 'BYR'
            valute_node = xml_data.find(f'.//Valute[CharCode="{currency_code}"]')

            # Если 'BYR' отсутствует, попробуйте найти валюту с кодом 'BYN'
            if valute_node is None and currency_code == 'BYR':
                valute_node = xml_data.find('.//Valute[CharCode="BYN"]')

            if valute_node is not None:
                nominal = float(valute_node.find('Nominal').text.replace(',', '.'))
                value = float(valute_node.find('Value').text.replace(',', '.'))
                return nominal, value
            else:
                return None, None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе данных: {e}")
            print(f"Повторная попытка...")

    return None, None


if __name__ == '__main__':
    # Заголовок CSV-файла
    csv_header = ['date', 'BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']

    # Определите период
    start_date = datetime(2001, 1, 1)
    end_date = datetime(2024, 1, 1)

    # Определение валют
    currencies = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']

    # Создайте CSV-файл и записывайте в него заголовок
    with open(BASE_DIR / 'static/analytics/currency.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(csv_header)

        # Цикл по месяцам
        current_date = start_date
        while current_date <= end_date:
            formatted_date = current_date.strftime('%d/%m/%Y')

            # Получите номинал и курс валюты для каждого кода с повторными попытками
            currency_data = [get_currency_rate_with_retry(formatted_date, currency) for currency in currencies]

            # Разделите значение на номинал, чтобы получить правильный курс
            rates = [round(value / nominal, 4) if nominal and nominal != 0 else None for nominal, value in currency_data]

            # Запишите данные в CSV-файл
            csv_row = [formatted_date] + rates
            csv_writer.writerow(csv_row)
            print(csv_row)

            # Переход к следующему месяцу
            current_date = current_date.replace(day=1) + timedelta(days=32)
            current_date = current_date.replace(day=1)

    print("CSV-файл успешно создан.")
