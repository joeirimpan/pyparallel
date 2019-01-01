# -*- coding: utf-8 -*-
"""
    pyparallel.py
    :copyright: (c) 2019 by Joe Paul.
    :license: see LICENSE for details.
"""
import os
import time
import multiprocessing as mp

import requests
from requests.exceptions import HTTPError


session = requests.Session()
session.stream = True


class Part:
    __slots__ = ['url', 'offset', 'size']

    def __init__(self, url, size, offset):
        self.url = url
        self.offset = offset
        self.size = size


def producer(part, q):
    """Download given part and push to consumer queue

    :param part: Part instance
    :param q: Consumer queue
    """
    response = session.get(
        url=part.url,
        headers={
            'Range': 'bytes=%d-%d' % (
                part.offset,
                part.offset + (part.size-1)
            )
        },
    )

    try:
        response.raise_for_status()
    except HTTPError:
        raise

    # Push data into queue
    q.put((part.offset, response.content))


def consumer(q, name):
    """Listen to consumer queue and write file using offset

    :param q: Consumer queue
    :param name: file name
    """
    f = open(name, 'w+b')

    while 1:
        m = q.get()
        if m == 'kill':
            break

        # Unpack tuple
        offset, content = m

        f.seek(offset)
        f.write(content)
        f.flush()

    f.close()


class Downloader:

    def __init__(self, url, conns, filename):
        self.url = url
        self.conns = conns
        self.filename = filename

    def start(self):
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

        size = content_length / self.conns
        offset = 0
        jobs = []
        for index in range(self.conns):
            offset = index * size
            if index == self.conns - 1:
                size = content_length - size * index

            part = Part(**{
                'url': self.url,
                'size': size,
                'offset': offset,
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
