# -*- coding: utf-8 -*-
"""
    pyparallel.py
    :copyright: (c) 2017 by Joe Paul.
    :license: see LICENSE for details.
"""
import os
from multiprocessing import Process

from tqdm import tqdm
import requests
from requests.exceptions import HTTPError


class Part:
    id = None
    url = ''
    offset = 0
    dlsize = 0
    size = 0
    file = None

    def download(self):
        """Initiate download of this part
        """
        download = Download()
        return download(part=self)


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
            },
            stream=True
        )
        try:
            response.raise_for_status()
        except HTTPError:
            raise

        pbar = tqdm(unit='B', total=int(response.headers['Content-Length']))
        chunk_size = 10 ** 6
        for chunk in response.iter_content(chunk_size=chunk_size):
            if not chunk:
                break
            part.file.seek(part.offset + part.dlsize)
            pbar.update(len(chunk))
            part.file.write(chunk)
            part.file.flush()
            part.dlsize += len(chunk)
            remaining = part.size - part.dlsize
            if remaining == 0:
                break
            elif remaining < chunk_size:
               chunk_size = remaining


class Downloader:

    def __init__(self, url, conns, filename):
        self.url = url
        self.conns = conns
        self.filename = filename
        self.size = 0
        self.file_descriptor = None
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

        self.size = int(response.headers.get('Content-Length'))
        if os.path.exists(self.filename):
            os.remove(self.filename)
        self.parts = [Part() for _ in range(self.conns)]
        self.file_descriptor = open(self.filename, 'w+')

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
        """Start downloading with each process assigned to tasks
        """
        processes = []
        for part in self.parts:
            p = Process(target=Part.download, args=(part,))
            processes.append(p)
            p.start()
        # Join them
        map(lambda p: p.join(), processes)
        self.file_descriptor.close()


if __name__ == '__main__':
    downloader = Downloader(
        url='https://upload.wikimedia.org/wikipedia/commons/f/ff/Pizigani_1367_Chart_10MB.jpg',
        conns=4,
        filename='chart.jpg'
    )
    downloader.start_download()
