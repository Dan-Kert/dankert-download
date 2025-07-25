#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import contextlib
import subprocess

from dankert_download.utils import Popen

rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAZY_EXTRACTORS = 'dankert_download/extractor/lazy_extractors.py'


class TestExecution(unittest.TestCase):
    def run_dankert_download(self, exe=(sys.executable, 'dankert_download/__main__.py'), opts=('--version', )):
        stdout, stderr, returncode = Popen.run(
            [*exe, '--ignore-config', *opts], cwd=rootDir, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(stderr, file=sys.stderr)
        self.assertEqual(returncode, 0)
        return stdout.strip(), stderr.strip()

    def test_main_exec(self):
        self.run_dankert_download()

    def test_import(self):
        self.run_dankert_download(exe=(sys.executable, '-c', 'import dankert_download'))

    def test_module_exec(self):
        self.run_dankert_download(exe=(sys.executable, '-m', 'dankert_download'))

    def test_cmdline_umlauts(self):
        _, stderr = self.run_dankert_download(opts=('ä', '--version'))
        self.assertFalse(stderr)

    def test_lazy_extractors(self):
        try:
            subprocess.check_call([sys.executable, 'devscripts/make_lazy_extractors.py', LAZY_EXTRACTORS],
                                  cwd=rootDir, stdout=subprocess.DEVNULL)
            self.assertTrue(os.path.exists(LAZY_EXTRACTORS))

            _, stderr = self.run_dankert_download(opts=('-s', 'test:'))
            # `MIN_RECOMMENDED` emits a deprecated feature warning for deprecated Python versions
            if stderr and stderr.startswith('Deprecated Feature: Support for Python'):
                stderr = ''
            self.assertFalse(stderr)

            subprocess.check_call([sys.executable, 'test/test_all_urls.py'], cwd=rootDir, stdout=subprocess.DEVNULL)
        finally:
            with contextlib.suppress(OSError):
                os.remove(LAZY_EXTRACTORS)


if __name__ == '__main__':
    unittest.main()
