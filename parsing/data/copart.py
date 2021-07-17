import json
import os
from multiprocessing.dummy import Pool


import requests


class Copart:
    url: str = 'https://www.copart.com/public/lots/search'
    pages_per_process: int = 25

    def __init__(self, headers_filename=os.path.join('data', 'headers.json')):
        with open(headers_filename, encoding='utf-8') as json_file:
            self.headers = json.loads(json_file.read())
        self.output = []

    def parse_pages(self, task):
        params: dict = task['params']
        for p in range(task['from'], task['to']):
            response = requests.post(self.url, params={'page': p, **params}, headers=self.headers)
            if not response:
                print(f'Failed to get data from page {params["page"]}, continuing')
                continue
            cars = [{'page': p, **car} for car in response.json()['data']['results']['content']]
            self.output.extend(cars)

    def get_data(self, filters=None):
        params = {'filter[FETI]': 'buy_it_now_code:B1', 'size': 1}
        first_response = requests.post(self.url, params=params, headers=self.headers)
        if not first_response:
            return None
        size = 100
        total = int(first_response.json()['data']['results']['totalElements'])
        pages = int(total / size) + 1 if total / size > int(total / size) else int(total / size)
        params['size'] = size
        tasks = [{'from': p, 'to': p + self.pages_per_process
        if p + self.pages_per_process <= pages else p + (pages - p) + 1,
                  'params': params}
                 for p in range(0, int(pages / self.pages_per_process) + 1
            if pages / self.pages_per_process > int(pages)
            else total // size, self.pages_per_process)]
        pool = Pool(processes=len(tasks))
        pool.map(self.parse_pages, tasks)
        if filters:
            self.output = [car for car in self.output
                           if (filters['year_from'] <= car['lcy'] <= filters['year_to']) and
                           (filters['price_from'] <= car['bnp'] <= filters['price_to'])]
        return sorted(self.output, key=lambda car: car['page'])
