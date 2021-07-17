import json
import sys
import time

import requests


def get_data(url, headers_filename='headers.json'):
    with open(headers_filename, encoding='utf-8') as json_file:
        headers = json.loads(json_file.read())
    params = {'size': 1}
    first_response = requests.post(url, params=params, headers=headers)
    if not first_response:
        print('You fucked up, you idiot!')
        sys.exit(-1)
    size = 100
    total = int(first_response.json()['data']['results']['totalElements'])
    pages = int(total / size) + 1 if total / size > int(total) else int(total / size)
    params['size'] = size
    params['page'] = 0
    output = []
    for _ in range(pages):
        start_time = time.time()
        params['page'] += 1
        response = requests.post(url, params=params, headers=headers)
        if not response:
            print(f'Failed to get data from page {params["page"]}, continuing')
            continue
        available_cars = [car for car in response.json()['data']['results']['content']
                          if car['bndc'] == 'BUY IT NOW']
        output.extend(available_cars)
        print(f'Page: {params["page"]}, count: {len(available_cars)}, '
              f'time passed: {time.time() - start_time:.2f}')
    return output


def main(url):
    data = get_data(url)
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(data))
    print('\nOK')


if __name__ == '__main__':
    api_url = 'https://www.copart.com/public/lots/search'
    main(api_url)
