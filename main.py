from file_processing import load_company_vacancies, get_user_input, process_datetime
from database.db_manager import DBManager
from database.config import connector_db
from colorama import Fore

# Вызов функции load_company_vacancies из файла utils [получает данные о работодателях и их вакансиях с сайта hh.ru]
load_company_vacancies()


def run_operations():
    """
    Функция - интерактив с пользователем,
    предоставляет выбор действий по отображению информации из БД
    :return:
    """
    db_manager = DBManager(connector_db)

    point = get_user_input()

    if point == 1:
        # Код для получения списка всех компаний и количества вакансий у каждой компании
        companies_vacancies_count = db_manager.get_companies_and_vacancies_count()
        print(f'{Fore.YELLOW}Получение списка всех компаний и количества вакансий у каждой компании:')
        count = 1
        for company, vacancies_count in companies_vacancies_count:
            print(f'{Fore.LIGHTWHITE_EX}{count}). Компания - "{company}", [Количество вакансий: {vacancies_count}]')
            count += 1

    elif point == 2:
        # Код для получения списка всех вакансий
        all_vacancies = db_manager.get_all_vacancies()
        print(f'{Fore.YELLOW}Общий список вакансий. Всего - {Fore.LIGHTWHITE_EX}{len(all_vacancies)}')
        count = 1
        for company, title, salary, url in all_vacancies:
            print(f'{Fore.LIGHTWHITE_EX}{count}). Компания: {company}, Вакансия: {title}, Зарплата: {salary}, URL: {url}')
            count += 1

    elif point == 3:
        # Код для получения средней зарплаты по вакансиям
        avg_salary = db_manager.get_avg_salary()
        print(f'{Fore.LIGHTWHITE_EX}Средняя зарплата: {int(avg_salary)} руб.')

    elif point == 4:
        # Код для получения списка вакансий с зарплатой выше средней
        vacancies_higher_salary = db_manager.get_vacancies_with_higher_salary()
        print(f'{Fore.YELLOW}найдено {len(vacancies_higher_salary)} ваканий.')
        for vacancy in vacancies_higher_salary:
            print(f'{Fore.LIGHTWHITE_EX}компания: {vacancy[1]}, З/П: {vacancy[2]}, ссылка на вакансию: {vacancy[7]}')

    elif point == 5:
        keyword = input(f'{Fore.YELLOW}введите ключевое слова для поиска интересующих вас ваканий ')
        vacancies = db_manager.get_vacancies_with_keyword(keyword)
        print(keyword)

        # Далее вы можете использовать полученный список вакансий по ключевому слову
        for vacancy in vacancies:
            print(f'{Fore.YELLOW}название: {Fore.LIGHTWHITE_EX}{vacancy[1]}, '
                  f'{Fore.YELLOW}город: {Fore.LIGHTWHITE_EX}{vacancy[5]}, '
                  f'{Fore.YELLOW}дата публикации: {Fore.LIGHTWHITE_EX}{process_datetime(vacancy[6])}, '
                  f'{Fore.YELLOW}ссылка на вакансию: {Fore.LIGHTWHITE_EX}{vacancy[7]}, '
                  f'{Fore.YELLOW}опыт: {Fore.LIGHTWHITE_EX}{vacancy[9]}')
    else:
        print("Некорректный выбор операции")


run_operations()
