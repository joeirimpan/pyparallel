# -*- coding: utf-8 -*-
"""
    pyparallel.py
    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import os
from multiprocessing import Process

import requests
from requests.exceptions import HTTPError


class Part:

    def __init__(self, id, url, dlsize, size, filename, offset=0):
        self.id = id
        self.url = url
        self.offset = offset
        self.dlsize = dlsize
        self.size = size
        self.filename = filename

    def download(self):
        """Initiate download of this part
        """
        return Download()(part=self)


class Download:

    def __call__(self, part, *args, **kwargs):
        """Download given part and write to the file
        at the right position

        :param part: Part instance
        """
        response = requests.get(
            url=part.url,
            headers={
                'Range': 'bytes=%d-%d' % (
                    part.offset,
                    part.offset + (part.size-1)
                )
            }
        )
        try:
            response.raise_for_status()
        except HTTPError:
            raise

        with open(part.filename, 'w+') as fd:
            fd.seek(part.offset + part.dlsize)
            fd.write(response.content)


class Downloader:

    def __init__(self, url, conns, filename):
        self.url = url
        self.conns = conns
        self.filename = filename
        self.parts = []
        self.divide_and_conquer()

    def divide_and_conquer(self):
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

        size = content_length / self.conns
        for index in range(self.conns):
            if index == self.conns - 1:
                size = content_length - size * index
            print "Part %s Size %s" % (index, size)
            self.parts.append(
                Part(**{
                    'id': index,
                    'url': self.url,
                    'size': size,
                    'dlsize': 0,
                    'filename': self.filename
                })
            )

    def start_download(self):
        """Start downloading with each process assigned to tasks
        """
        processes = []
        for part in self.parts:
            p = Process(target=Part.download, args=(part,))
            processes.append(p)
            p.start()
        # Join them
        map(lambda p: p.join(), processes)


if __name__ == '__main__':
    downloader = Downloader(
        url='https://upload.wikimedia.org/wikipedia/commons/f/ff/Pizigani_1367_Chart_10MB.jpg',
        conns=4,
        filename='chart.jpg'
    )
    downloader.start_download()
