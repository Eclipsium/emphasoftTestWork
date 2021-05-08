from datetime import datetime
import requests
from bs4 import BeautifulSoup

from CONSTANTS import BASE_URL
from services import download_file_service


class BS4Worker:
    response: str
    soup: BeautifulSoup()
    payload: list

    def __init__(self, query: str, task_type: str) -> None:
        self.payload = []
        self.task_type = task_type
        self.query = query
        self.url = BASE_URL + f'&value={self.query.replace(" ", "+")}'  # replacing space char
        self.session = requests.session()

    @staticmethod
    def download(data: list) -> None:
        download_file_service(data)

    def parse(self) -> dict:
        soup = self.get_soup()
        # if have empty search signature in response body
        if soup.find('p', id='errorText'):
            return {'error': 'No results provided!'}

        data = soup.find_all('tr', 'even')
        data.extend(soup.find_all('tr', 'odd'))

        for item in data:
            item_data = {}  # noqa
            item_data['form_number'] = item.find('a').get_text().strip()
            item_data['form_title'] = item.find('td', 'MiddleCellSpacer').get_text().strip()
            item_data['min_year'] = int(item.find('td', 'EndCellSpacer').get_text().strip())

            # idk where i can search max_year property :/ i thing is current year
            item_data['max_year'] = datetime.now().year
            item_data['download_pdf'] = item.find('a')['href']

            self.payload.append(item_data)

        try:
            # Recursion to iterate over all pages
            pagination_link = soup.find('div', 'paginationBottom').find_all('a')[-1]
            # if next_page is clickable
            if pagination_link.get_text() == 'Next »':
                self.url = f'https://apps.irs.gov/{pagination_link["href"]}'
                self.parse()

        except (AttributeError, IndexError):
            # check if pagination is None
            pass

        if self.task_type == 'download':
            self.download(self.payload)

        return {"count": len(self.payload), "query": self.query, "data": self.payload}

    def get_soup(self):
        # synchronous data acquisition
        response = self.session.get(self.url)
        self.soup = BeautifulSoup(response.text, 'lxml')
        return self.soup


def background_bs4_worker(query: str, task_type: str) -> None:
    # Provide background worker
    worker = BS4Worker(query, task_type)
    worker.parse()
