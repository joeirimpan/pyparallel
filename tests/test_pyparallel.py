# -*- coding: utf-8 -*-
import os.path

class TestDownloader:

    def test_downloader(self, downloder):
        downloder.start()

        # Check if the file exits
        assert os.path.exists('chart.jpg') is True
