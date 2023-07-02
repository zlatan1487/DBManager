from models.company_vacancy import CompanyVacancies
from database.db_vacancies import DatabaseVacancies
from database.db_employers import DatabaseEmployers
from utilities.progress_bar import progress_bar
from database.config import connector_db
from datetime import datetime
from colorama import Fore


def load_company_vacancies():
    """
    Функция Получает данные о работодателях и их вакансиях с сайта hh.ru,
    сохраняет в БД
    :return:
    """

    # Создание екземпляра класса CompanyVacancies
    company_vacancies = CompanyVacancies()

    print("Загрузка данных о компаниях...")

    # Вызов функции progress_bar для отображения времени загрузки данных
    progress_bar(10, "Загрузка информации о компаниях")

    # Выполнение функции get_company()
    get_company = company_vacancies.get_company()
    if not get_company:
        print('Ошибка при загрузке компаний')
    else:
        print("Информация о компаниях загружена.")

    print("Загрузка данных о вакансиях...")

    # Вызов функции progress_bar для отображения времени загрузки данных
    progress_bar(20, "Загрузка информации о вакансиях")

    # Выполнение функции get_company_vacancies()
    get_company_vacancies = company_vacancies.get_company_vacancies()
    if not get_company_vacancies:
        print("Ошибка при загрузке вакансий")
    else:
        print("Информация о вакансиях загружена.")

    # Создание екземпляра класса DatabaseEmployers и создание таблицы employers с наполнением данными о компаниях
    db_employers = DatabaseEmployers(connector_db)
    db_employers.create_table()
    db_employers.insert_data(get_company)

    # Создание екземпляра класса DatabaseVacancies и создание таблицы vacancies с наполнением данными о вакансиях
    db_vacancies = DatabaseVacancies(connector_db)
    db_vacancies.create_table()
    db_vacancies.insert_data(get_company_vacancies)


def get_user_input():
    """
    Функция предлагает пользователю выбрать операцию для выполнения
    :return: point
    """
    while True:
        try:
            user_input = input(f"{Fore.GREEN}Выберите операцию для выполнения (1-4):\n"
                               f"{Fore.LIGHTWHITE_EX}"
                               f"1. Получение списка всех компаний и количества вакансий у каждой компании\n"
                               f"2. Получение списка всех вакансий\n3. Получение средней зарплаты по вакансиям\n"
                               f"4. Получение списка вакансий с зарплатой выше средней\n"
                               f"{Fore.GREEN}введите нужный номер... ")
            if user_input.strip() == "":
                raise ValueError
            point = int(user_input)
            if point < 1 or point > 5:
                raise ValueError
            return point
        except ValueError:
            print(f"{Fore.RED}Некорректный ввод. Пожалуйста, введите число от 1 до 4.")


def process_datetime(datetime_str):
    """
    Преобразует строковое представление даты и времени в отформатированную строку даты.
    :param datetime_str:
    :return:
    """
    datetime_format = "%Y-%m-%dT%H:%M:%S%z"
    dt = datetime.strptime(datetime_str, datetime_format)
    formatted_datetime = dt.strftime("%d.%m.%Y")
    return formatted_datetime
