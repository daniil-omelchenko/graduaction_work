import csv
import os
from queue import Queue
import re
from threading import Thread
from datetime import datetime

import requests
import pandas
from sklearn.externals import joblib

import classifier.tools as tools
from classifier.bag_of_words import bag_of_words
from scraper.worker import WorkerPool
from scraper.yahoo import search_with_yahoo
import scraper.google as google
import scraper.itunes as itunes


TOP_RESULTS_THRESHOLD = 3
DEFAULT_OUTPUT_FILE_NAME = 'out-{date}.tsv'


def scrap_app_data(app_list, output_file):

    app_list_queue = Queue()
    app_data_queue = Queue()

    for app_name in app_list:
        app_list_queue.put(app_name)

    workers = WorkerPool(
        worker=collect_data,
        tasks=app_list_queue,
        min_interval=0.1,
        context=app_data_queue,
        max_workers=20)
    workers.start()

    track_saving_thread = Thread(target=_save_app_data, args=(app_data_queue, output_file))
    track_saving_thread.start()

    workers.wait_until_done()

    app_data_queue.put(None)
    track_saving_thread.join()


def _save_app_data(app_data_list, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t', quoting=1)
        writer.writerow(['name', 'description', 'genre', 'artwork'])
        while True:
            app_data = app_data_list.get()
            if not app_data:
                break
            writer.writerow(app_data)


def cleanup(data):
    return ' '.join(re.findall(r"[a-zA-Z']+\.|[a-zA-Z']+", data))


def collect_data(app_name, app_data_queue):
    page = google.get_page_by_id(app_name)
    module = google
    if page:
        print('found in google play')
    else:
        url = None
        query = '+'.join(app_name.split()) + ' app'
        for link in search_with_yahoo(query, 10):
            if google.MARKER in link:
                url = link
                module = google
                print('found in google play by search')
                break
            if itunes.MARKER in link:
                url = link
                module = itunes
                print('found in itunes play by search')
                break
        if not url:
            print('ERROR', app_name, '-', 'NOT FOUND GOOGLE PLAY OR ITUNES')
            return
        try:
            res = requests.get(url)
        except Exception as ex:
            print('ERROR', app_name, '-', ex, url)
            return
        if res.status_code == 200:
            page = res.content
        else:
            print('ERROR', app_name, '-', 'NON 200 CODE', url)
            return

    description = module.extract_description(page)
    genre = module.extract_genre(page)
    artwork = module.extract_artwork_link(page)
    if description and genre and artwork:
        app_data_queue.put([app_name, description, genre, artwork])
        print('SUCCESS', genre, app_name, artwork)
    else:
        print('ERROR', app_name, '-', 'NON 200 CODE')


def classify(app_list):
    root = os.path.realpath(os.path.dirname(__file__))
    app_list = [app for app in app_list if len(app.strip()) > 0]
    output_file_name = root + '/train_simplified.tsv'

    scrap_app_data(app_list, output_file_name)

    data_set = pandas.read_csv(root + '/train_simplified.tsv', delimiter='\t', quoting=1)
    v = joblib.load(root + '/models/trimmed.vocabulary')
    m = joblib.load(root + '/models/nn.model')
    sample = tools.dataset_to_sample(bag_of_words(data_set['description'], v))

    app_data = []
    for app_v, artwork, name in zip(sample, data_set['artwork'], data_set['name']):
        app_data.append(
            {
                "name": name,
                "artwork": artwork,
                "genre": m.predict(app_v.reshape(1, -1))[0]
            }
        )
    return app_data

if __name__ == '__main__':
    print(classify(['com.kauf.sticker.funfacechangerextremefree', 'com.grumotara.pixelbounce', 'com.coolappsg.pianotapjustin']))
