from vacancies import VacancyManager
from png_creator import *
from djangoProject.settings import BASE_DIR
import copy

if __name__ == '__main__':
    # ----- Страница «Востребованность» -----
    all_vacancy = VacancyManager()  # Экземпляр класса менеджера вакансий

    all_vacancy.read_from_csv(BASE_DIR / 'static/analytics/vacancies.csv')  # Читаем вакансии из CSV файла

    vacancy_count_by_year = all_vacancy.get_vacancy_count_by_year()  # Получаем словарь год - количество всех вакансий
    my_vacancy_count_by_year = copy.deepcopy(all_vacancy).remove_empty_vacancies().get_vacancy_count_by_year()  # Получаем словарь год - количество вакансий web-программиста

    avg_salary_by_year = copy.deepcopy(all_vacancy).remove_empty_vacancies().update_salary_in_rubles().get_avg_salary()  # Получаем словарь год - средняя зарплата всех вакансий
    my_avg_salary_by_year = copy.deepcopy(all_vacancy).remove_empty_vacancies().remove_non_matching_vacancies().update_salary_in_rubles().get_avg_salary()  # Получаем словарь год - средняя зарплата web-программистов

    plot_dynamics(avg_salary_by_year, BASE_DIR / 'static/vendor/img/chart1.1.png', 'Год', 'Зарплата программиста в рублях')
    plot_table_dynamics(avg_salary_by_year, BASE_DIR / 'static/vendor/img/table1.1.png')

    plot_dynamics(vacancy_count_by_year, BASE_DIR / 'static/vendor/img/chart1.2.png', 'Год', 'Количество вакансий')
    plot_table_dynamics(vacancy_count_by_year, BASE_DIR / 'static/vendor/img/table1.2.png')

    plot_dynamics(my_avg_salary_by_year, BASE_DIR / 'static/vendor/img/chart1.3.png', 'Год', 'Зарплата WEB-программиста в рублях')
    plot_table_dynamics(my_avg_salary_by_year, BASE_DIR / 'static/vendor/img/table1.3.png')

    plot_dynamics(my_vacancy_count_by_year, BASE_DIR / 'static/vendor/img/chart1.4.png', 'Год', 'Количество вакансий WEB-программиста')
    plot_table_dynamics(my_vacancy_count_by_year, BASE_DIR / 'static/vendor/img/table1.4.png')



