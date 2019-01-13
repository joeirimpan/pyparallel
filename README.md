## PyParallel

Split downloader using HTTP range headers.

Python port of https://github.com/t3rm1n4l/godownload


![https://pypi.python.org/pypi/pyparallel](https://img.shields.io/pypi/v/pyparallel.svg)
![https://travis-ci.org/joeirimpan/pyparallel](https://img.shields.io/travis/joeirimpan/pyparallel.svg)
![https://pyparallel.readthedocs.io/en/latest/?badge=latest](https://readthedocs.org/projects/pyparallel/badge/?version=latest)
![https://pyup.io/repos/github/joeirimpan/pyparallel/](https://pyup.io/repos/github/joeirimpan/pyparallel/shield.svg)


## Installation

```bash
pip install split-downloader
```

## Usage

### CLI

```bash
download --url "https://speed.hetzner.de/100MB.bin" --conns 10 --filename 100MB.bin
```

### Python API

```python
from pyparallel import Downloader

d = Downloader(
        url='https://upload.wikimedia.org/wikipedia/commons/f/ff/Pizigani_1367_Chart_10MB.jpg',
        conns=3,
        filename='chart.jpg'
)
d.start()
```

## TODO

* [ ] Progress bar
