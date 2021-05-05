import os
import threading
from datetime import datetime
from time import sleep
from uuid import UUID
from url_creator import create_request_url, parse_config_to_params


import requests
import json


def query_number_of_items(config):
    url = create_request_url(config, 0, 1)
    res = requests.get(url)
    return res.json()["response"]["numFound"]

def slice_generator(config, item_count, items_per_request=100):
    start = 0
    while start < item_count:
        n_items = min(items_per_request, item_count - start)
        print('Fetching items: ' + str(start) + ":" + str(start + n_items))
        yield start, n_items
        start += items_per_request


class LockedIterator(object):
    def __init__(self, it):
        self._lock = threading.Lock()
        self._it = iter(it)

    def __iter__(self):
        return self

    def __next__(self):
        with self._lock:
            return next(self._it)


with open('config.json') as f:
    config = json.load(f)
    outFileFolder = datetime.now().strftime('out_%H_%M_%S__%Y_%m_%d')
    os.makedirs(outFileFolder);
    nItems = query_number_of_items(config)
    iterator = LockedIterator(slice_generator(config, nItems))

    def consumer():
        while True:
            start, n_items = next(iterator)
            url = create_request_url(config, start, n_items);
            res = requests.get(url)
            with open(outFileFolder + "/" + str(start) + "_" + str(start + n_items) + ".json", "w") as file:
                file.write(res.text)
            sleep(2)


    # The higher the number the more we torture the sercer
    nThreads = 5
    for i in range(5):
        t = threading.Thread(target=consumer)
        t.daemon = True
        t.start()

    while True:
        pass
