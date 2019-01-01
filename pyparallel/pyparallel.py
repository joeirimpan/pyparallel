# -*- coding: utf-8 -*-
"""
    pyparallel.py
    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import os
import time
import multiprocessing as mp

import requests
from requests.exceptions import HTTPError


class Part:

    def __init__(self, id, url, size, offset, session):
        self.id = id
        self.url = url
        self.offset = offset
        self.size = size
        self.session = session


def producer(part, q):
    """Download given part and write to the file
    at the right position

    :param part: Part instance
    """
    response = part.session.get(
        url=part.url,
        headers={
            'Range': 'bytes=%d-%d' % (
                part.offset,
                part.offset + (part.size-1)
            )
        },
        stream=True
    )

    try:
        response.raise_for_status()
    except HTTPError:
        raise

    # Push data into queue
    q.put((part.id, response.content))


def consumer(q, name):
    data = []

    # Pull data from queue
    while 1:
        m = q.get()
        if m == 'kill':
            break
        data.append(m)

    # Sort based on part id and write into file
    with open(name, 'ab') as f:
        for k, v in sorted(dict(data).iteritems()):
            f.write(v)


class Downloader:

    def __init__(self, url, conns, filename):
        self.url = url
        self.conns = conns
        self.filename = filename
        self.parts = []

    def download(self):
        """Analyze the url content size and create parts for later downloading
        """
        response = requests.head(self.url)
        try:
            response.raise_for_status()
        except HTTPError:
            raise

        content_length = int(response.headers.get('Content-Length'))
        if os.path.exists(self.filename):
            os.remove(self.filename)

        # Init a process manager
        manager = mp.Manager()
        q = manager.Queue()
        pool = mp.Pool(mp.cpu_count() + 2)

        # File writer consumer which listens to queue
        pool.apply_async(consumer, (q, self.filename))

        session = requests.Session()

        print "total_length: ", content_length
        size = content_length / self.conns
        offset = 0
        jobs = []
        for index in range(self.conns):
            old_size = size
            if index == self.conns - 1:
                size = content_length - size * index

            if index == 0:
                offset = 0
            elif index == self.conns - 1:
                offset += old_size
            else:
                offset += size

            part = Part(**{
                'id': index,
                'url': self.url,
                'size': size,
                'offset': offset,
                'session': session,
            })

            job = pool.apply_async(producer, (part, q))
            jobs.append(job)

        # Collect all job results
        for job in jobs:
            job.get()

        # Kill the consumer
        q.put('kill')
        pool.close()
        pool.join()


if __name__ == '__main__':
    start_time = time.time()
    downloader = Downloader(
        url='https://upload.wikimedia.org/wikipedia/commons/f/ff/Pizigani_1367_Chart_10MB.jpg',  # noqa
        conns=3,
        filename='chart.jpg'
    )
    downloader.download()
    end_time = time.time()
    print "Time taken: ", (end_time - start_time)
