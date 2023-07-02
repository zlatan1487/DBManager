import requests


class CompanyVacancies:
    """
    Класс для получения информации о компаниях и их вакансий из сайта hh.ru.
    """
    def __init__(self):
        self.base_url = 'https://api.hh.ru'
        self.employer_endpoint = '/employers'
        self.vacancies_endpoint = '/vacancies'
        self.employer_id = 'employer_id'

    def get_company(self):
        """
        Метод для получения информации о компаниях.
        """
        url = f"{self.base_url}{self.employer_endpoint}"
        employers = []

        page = 1
        per_page = 80
        total_companies = 0

        while total_companies < 21:
            params = {
                "page": page,
                "per_page": per_page,
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                companies = response.json()

                if not companies['items']:
                    print("No items found")
                    break

                for employer in companies['items']:
                    if employer['open_vacancies'] > 7:
                        employers.append(employer)
                        total_companies += 1

                        if total_companies == 20:
                            break

                page += 1
            else:
                print("Error:", response.status_code)
                print(response.content)
                break

        return employers

    def get_company_vacancies(self):
        """
        Метод для получения информации о вакансиях.
        """
        employers = self.get_company()

        all_vacancies = []

        for company_id in [item['id'] for item in employers]:
            url = f'{self.base_url}{self.vacancies_endpoint}?{self.employer_id}={company_id}'

            response = requests.get(url)
            if response.status_code == 200:
                vacancies = response.json()
                for vacancy in vacancies['items']:
                    id = vacancy.get('id', '')
                    area = vacancy.get('name', '')
                    salary_from = vacancy.get('salary', {}).get('from') if vacancy.get('salary') else None
                    salary_to = vacancy.get('salary', {}).get('to') if vacancy.get('salary') else None
                    type = vacancy.get('type', '').get('name')
                    address = vacancy.get('address', {})
                    published_at = vacancy.get('published_at', {})
                    apply_alternate_url = vacancy.get('apply_alternate_url')
                    employer_id = vacancy.get('employer', {}).get('id')
                    experience = vacancy.get('experience', {}).get('name')
                    employment = vacancy.get('employment', {}).get('name')
                    vacancy_data = {'id': id, 'area': area,
                                    'salary_from': salary_from, 'salary_to': salary_to,
                                    'type': type, 'city': address.get('city') if address else None,
                                    'published_at': published_at, 'apply_alternate_url': apply_alternate_url,
                                    'employer_id': employer_id, 'experience': experience,
                                    'employment': employment
                                    }
                    all_vacancies.append(vacancy_data)
            else:
                print(f"Ошибка выполнения запроса: {response.status_code}")

        return all_vacancies

