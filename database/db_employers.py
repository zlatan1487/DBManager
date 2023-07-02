import psycopg2


class DatabaseEmployers:
    """
    Класс для получения информации о компаниях и их вакансий из сайта hh.ru.
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

    def create_table(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS employers
                     (id TEXT UNIQUE, name TEXT, url TEXT, alternate_url TEXT, vacancies_url TEXT)''')

        conn.commit()
        conn.close()

    def insert_data(self, data):
        conn = self.get_connection()
        connector = conn.cursor()
        try:
            employer_count = 0
            for employer in data:
                id = employer.get('id')
                name = employer.get('name')
                url = employer.get('url')
                alternate_url = employer.get('alternate_url')
                vacancies_url = employer.get('vacancies_url')

                # Проверить, существует ли уже запись с таким идентификатором
                connector.execute("SELECT COUNT(*) FROM employers WHERE id = %s", (id,))
                result = connector.fetchone()
                if result[0] == 0:
                    connector.execute("INSERT INTO employers VALUES (%s, %s, %s, %s, %s)",
                                      (id, name, url, alternate_url, vacancies_url))

                    employer_count += 1

            conn.commit()
            print(f'Компаний работодателей сохранены в БД - {employer_count}.')
        except Exception as e:
            conn.rollback()
            print("Ошибка:", str(e))
        finally:
            conn.close()
