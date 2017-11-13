#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click

from pyparallel.pyparallel import Downloader


@click.command()
@click.option('--url', required=True, help='Download URL')
@click.option('--conns', required=True, help='Number of parts')
@click.option('--filename', required=True, help='Output filename')
def cli(url, conns, filename):
    downloader = Downloader(
        url=url,
        conns=int(conns),
        filename=filename
    )
    downloader.start_download()
