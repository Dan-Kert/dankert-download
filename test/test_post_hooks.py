#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from test.helper import get_params, is_download_test, try_rm
import dankert_download.YoutubeDL  # isort: split
from dankert_download.utils import DownloadError


class YoutubeDL(dankert_download.YoutubeDL):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.to_stderr = self.to_screen


TEST_ID = 'gr51aVj-mLg'
EXPECTED_NAME = 'gr51aVj-mLg'


@is_download_test
class TestPostHooks(unittest.TestCase):
    def setUp(self):
        self.stored_name_1 = None
        self.stored_name_2 = None
        self.params = get_params({
            'skip_download': False,
            'writeinfojson': False,
            'quiet': True,
            'verbose': False,
            'cachedir': False,
        })
        self.files = []

    def test_post_hooks(self):
        self.params['post_hooks'] = [self.hook_one, self.hook_two]
        ydl = YoutubeDL(self.params)
        ydl.download([TEST_ID])
        self.assertEqual(self.stored_name_1, EXPECTED_NAME, 'Not the expected name from hook 1')
        self.assertEqual(self.stored_name_2, EXPECTED_NAME, 'Not the expected name from hook 2')

    def test_post_hook_exception(self):
        self.params['post_hooks'] = [self.hook_three]
        ydl = YoutubeDL(self.params)
        self.assertRaises(DownloadError, ydl.download, [TEST_ID])

    def hook_one(self, filename):
        self.stored_name_1, _ = os.path.splitext(os.path.basename(filename))
        self.files.append(filename)

    def hook_two(self, filename):
        self.stored_name_2, _ = os.path.splitext(os.path.basename(filename))
        self.files.append(filename)

    def hook_three(self, filename):
        self.files.append(filename)
        raise Exception(f'Test exception for \'{filename}\'')

    def tearDown(self):
        for f in self.files:
            try_rm(f)


if __name__ == '__main__':
    unittest.main()
