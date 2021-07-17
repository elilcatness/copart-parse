import json
import logging
import os
import sys
import time
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
            print({'page': p, **params})

    def get_data(self):
        params = {'filter[FETI]': 'buy_it_now_code:B1', 'size': 1}
        first_response = requests.post(self.url, params=params, headers=self.headers)
        if not first_response:
            print('You fucked up, you idiot!')
            sys.exit(-1)
        size = 100
        total = int(first_response.json()['data']['results']['totalElements'])
        print(f'total: {total}')
        pages = int(total / size) + 1 if total / size > int(total / size) else int(total / size)
        print(f'pages: {pages}')
        params['size'] = size
        tasks = [{'from': p, 'to': p + self.pages_per_process
        if p + self.pages_per_process <= pages else p + (pages - p) + 1,
                  'params': params}
                 for p in range(0, int(pages / self.pages_per_process) + 1
            if pages / self.pages_per_process > int(pages)
            else total // size, self.pages_per_process)]
        pool = Pool(processes=len(tasks))
        print('Started')
        pool.map(self.parse_pages, tasks)
        print('Finished')
        return sorted(self.output, key=lambda car: car['page'])