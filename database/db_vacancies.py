import psycopg2


class DatabaseVacancies:
    """
    Класс для работы с базой данных вакансий.
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
        c.execute('''CREATE TABLE IF NOT EXISTS vacancies
                     (id TEXT UNIQUE, area TEXT, salary_from INTEGER, salary_to INTEGER,
                     type TEXT, city TEXT, published_at TEXT, apply_alternate_url TEXT,
                     employer_id TEXT, experience TEXT, employment TEXT)''')

        conn.commit()
        conn.close()

    def insert_data(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            vacancy_count = 0
            for vacancy in data:
                id = vacancy.get('id')
                area = vacancy.get('area')
                salary_from = vacancy.get('salary_from')
                salary_to = vacancy.get('salary_to')
                type = vacancy.get('type')
                city = vacancy.get('city')
                published_at = vacancy.get('published_at')
                apply_alternate_url = vacancy.get('apply_alternate_url')
                employer_id = vacancy.get('employer_id')
                experience = vacancy.get('experience')
                employment = vacancy.get('employment')

                # Проверить, существует ли уже запись с таким идентификатором
                cursor.execute("SELECT COUNT(*) FROM vacancies WHERE id = %s", (id,))
                result = cursor.fetchone()
                if result[0] == 0:
                    cursor.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                   (id, area, salary_from, salary_to, type, city, published_at,
                                    apply_alternate_url, employer_id, experience, employment))

                    vacancy_count += 1

            conn.commit()
            print(f"Вакансии сохранены в БД - {vacancy_count}.")
        except Exception as e:
            conn.rollback()
            print("Ошибка:", str(e))
        finally:
            conn.close()
