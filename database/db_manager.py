import psycopg2


class DBManager:
    """
    Класс для управления операциями базы данных с использованием psycopg2.
    """
    def __init__(self, conn):
        self.dbname = conn['dbname']
        self.user = conn['user']
        self.password = conn['password']
        self.host = conn['host']

    def get_connection(self):
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host
        )

    def get_companies_and_vacancies_count(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT employers.name, COUNT(vacancies.id)
            FROM employers
            LEFT JOIN vacancies ON employers.id = vacancies.employer_id
            GROUP BY employers.name
        ''')
        result = cursor.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT employers.name, vacancies.area, vacancies.salary_from, vacancies.apply_alternate_url
            FROM employers
            JOIN vacancies ON employers.id = vacancies.employer_id
        ''')
        result = cursor.fetchall()
        conn.close()
        return result

    def get_avg_salary(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT AVG(salary_from) FROM vacancies')
        result = cursor.fetchone()
        conn.close()
        return result[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vacancies WHERE salary_from > %s', (avg_salary,))
        result = cursor.fetchall()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vacancies WHERE area ILIKE %s', ('%' + keyword + '%',))
        result = cursor.fetchall()
        conn.close()
        return result
