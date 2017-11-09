# -*- coding: utf-8 -*-
"""
    pyparallel.py
    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import os

import requests


class Part:
    id = None
    url = ''
    offset = 0
    dlsize = 0
    size = 0
    file = None

    def download(self):
        download = Download()
        return download(part=self)


class Download:

    def __call__(self, part, *args, **kwargs):
        session = requests.Session()
        buffer = []
        response = requests.get(
            url=part.url,
            headers={
                'Range': 'bytes=%d-%d' % (
                    part.offset,
                    part.offset + (part.size-1)
                )
            }
        )
        data = response.content
        part.file.seek(part.offset + part.dlsize)
        part.file.write(data)
        part.file.seek(0)



class Downloader:

    file = None
    size = 0
    parts = []
    start = 0
    end = 0
    status = ''

    def __init__(self, url, conns, filename):
        self.url = url
        self.conns = conns
        self.filename = filename

        self.divide_and_conquer()

    def divide_and_conquer(self):
        response = requests.head(self.url)
        # TODO Handle errors
        self.size = int(response.headers.get('Content-Length'))
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.file_descriptor = open(self.filename, 'w+')
        self.parts = [Part() for _ in range(self.conns)]

        size = self.size / self.conns
        for i, part in enumerate(self.parts):
            part.id = i
            part.url = self.url
            part.offset = i * size
            if i == self.conns - 1:
                part.size = self.size - size * i
            else:
                part.size = size
            part.dlsize = 0
            part.file = self.file_descriptor

    def start_download(self):
        for part in self.parts:
            part.download()


if __name__ == '__main__':
    downloader = Downloader(
        url='https://upload.wikimedia.org/wikipedia/commons/f/ff/Pizigani_1367_Chart_10MB.jpg',
        conns=4,
        filename='testfile'
    )
    downloader.start_download()
