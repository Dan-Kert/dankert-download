#!/usr/bin/env python3

# Allow direct execution
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from test.helper import FakeYDL, report_warning
from dankert_install.update import UpdateInfo, Updater


# XXX: Keep in sync with dankert_install.update.UPDATE_SOURCES
TEST_UPDATE_SOURCES = {
    'stable': 'dankert-download/dankert-download',
    'nightly': 'dankert-download/dankert-download-nightly-builds',
    'master': 'dankert-download/dankert-download-master-builds',
}

TEST_API_DATA = {
    'dankert-download/dankert-download/latest': {
        'tag_name': '2023.12.31',
        'target_commitish': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
        'name': 'dankert-download 2023.12.31',
        'body': 'BODY',
    },
    'dankert-download/dankert-download-nightly-builds/latest': {
        'tag_name': '2023.12.31.123456',
        'target_commitish': 'master',
        'name': 'dankert-download nightly 2023.12.31.123456',
        'body': 'Generated from: https://github.com/dankert-download/dankert-download/commit/cccccccccccccccccccccccccccccccccccccccc',
    },
    'dankert-download/dankert-download-master-builds/latest': {
        'tag_name': '2023.12.31.987654',
        'target_commitish': 'master',
        'name': 'dankert-download master 2023.12.31.987654',
        'body': 'Generated from: https://github.com/dankert-download/dankert-download/commit/dddddddddddddddddddddddddddddddddddddddd',
    },
    'dankert-download/dankert-download/tags/testing': {
        'tag_name': 'testing',
        'target_commitish': '9999999999999999999999999999999999999999',
        'name': 'testing',
        'body': 'BODY',
    },
    'fork/dankert-download/latest': {
        'tag_name': '2050.12.31',
        'target_commitish': 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
        'name': '2050.12.31',
        'body': 'BODY',
    },
    'fork/dankert-download/tags/pr0000': {
        'tag_name': 'pr0000',
        'target_commitish': 'ffffffffffffffffffffffffffffffffffffffff',
        'name': 'pr1234 2023.11.11.000000',
        'body': 'BODY',
    },
    'fork/dankert-download/tags/pr1234': {
        'tag_name': 'pr1234',
        'target_commitish': '0000000000000000000000000000000000000000',
        'name': 'pr1234 2023.12.31.555555',
        'body': 'BODY',
    },
    'fork/dankert-download/tags/pr9999': {
        'tag_name': 'pr9999',
        'target_commitish': '1111111111111111111111111111111111111111',
        'name': 'pr9999',
        'body': 'BODY',
    },
    'fork/dankert-download-satellite/tags/pr987': {
        'tag_name': 'pr987',
        'target_commitish': 'master',
        'name': 'pr987',
        'body': 'Generated from: https://github.com/dankert-download/dankert-download/commit/2222222222222222222222222222222222222222',
    },
}

TEST_LOCKFILE_COMMENT = '# This file is used for regulating self-update'

TEST_LOCKFILE_V1 = rf'''{TEST_LOCKFILE_COMMENT}
lock 2022.08.18.36 .+ Python 3\.6
lock 2023.11.16 (?!win_x86_exe).+ Python 3\.7
lock 2023.11.16 win_x86_exe .+ Windows-(?:Vista|2008Server)
lock 2024.10.22 py2exe .+
lock 2024.10.22 linux_(?:armv7l|aarch64)_exe .+-glibc2\.(?:[12]?\d|30)\b
lock 2024.10.22 (?!\w+_exe).+ Python 3\.8
lock 2024.10.22 win(?:_x86)?_exe Python 3\.[78].+ Windows-(?:7-|2008ServerR2)
'''

TEST_LOCKFILE_V2_TMPL = r'''%s
lockV2 dankert-download/dankert-download 2022.08.18.36 .+ Python 3\.6
lockV2 dankert-download/dankert-download 2023.11.16 (?!win_x86_exe).+ Python 3\.7
lockV2 dankert-download/dankert-download 2023.11.16 win_x86_exe .+ Windows-(?:Vista|2008Server)
lockV2 dankert-download/dankert-download 2024.10.22 py2exe .+
lockV2 dankert-download/dankert-download 2024.10.22 linux_(?:armv7l|aarch64)_exe .+-glibc2\.(?:[12]?\d|30)\b
lockV2 dankert-download/dankert-download 2024.10.22 (?!\w+_exe).+ Python 3\.8
lockV2 dankert-download/dankert-download 2024.10.22 win(?:_x86)?_exe Python 3\.[78].+ Windows-(?:7-|2008ServerR2)
lockV2 dankert-download/dankert-download-nightly-builds 2023.11.15.232826 (?!win_x86_exe).+ Python 3\.7
lockV2 dankert-download/dankert-download-nightly-builds 2023.11.15.232826 win_x86_exe .+ Windows-(?:Vista|2008Server)
lockV2 dankert-download/dankert-download-nightly-builds 2024.10.22.051025 py2exe .+
lockV2 dankert-download/dankert-download-nightly-builds 2024.10.22.051025 linux_(?:armv7l|aarch64)_exe .+-glibc2\.(?:[12]?\d|30)\b
lockV2 dankert-download/dankert-download-nightly-builds 2024.10.22.051025 (?!\w+_exe).+ Python 3\.8
lockV2 dankert-download/dankert-download-nightly-builds 2024.10.22.051025 win(?:_x86)?_exe Python 3\.[78].+ Windows-(?:7-|2008ServerR2)
lockV2 dankert-download/dankert-download-master-builds 2023.11.15.232812 (?!win_x86_exe).+ Python 3\.7
lockV2 dankert-download/dankert-download-master-builds 2023.11.15.232812 win_x86_exe .+ Windows-(?:Vista|2008Server)
lockV2 dankert-download/dankert-download-master-builds 2024.10.22.045052 py2exe .+
lockV2 dankert-download/dankert-download-master-builds 2024.10.22.060347 linux_(?:armv7l|aarch64)_exe .+-glibc2\.(?:[12]?\d|30)\b
lockV2 dankert-download/dankert-download-master-builds 2024.10.22.060347 (?!\w+_exe).+ Python 3\.8
lockV2 dankert-download/dankert-download-master-builds 2024.10.22.060347 win(?:_x86)?_exe Python 3\.[78].+ Windows-(?:7-|2008ServerR2)
'''

TEST_LOCKFILE_V2 = TEST_LOCKFILE_V2_TMPL % TEST_LOCKFILE_COMMENT

TEST_LOCKFILE_ACTUAL = TEST_LOCKFILE_V2_TMPL % TEST_LOCKFILE_V1.rstrip('\n')

TEST_LOCKFILE_FORK = rf'''{TEST_LOCKFILE_ACTUAL}# Test if a fork blocks updates to non-numeric tags
lockV2 fork/dankert-download pr0000 .+ Python 3.6
lockV2 fork/dankert-download pr1234 (?!win_x86_exe).+ Python 3\.7
lockV2 fork/dankert-download pr1234 win_x86_exe .+ Windows-(?:Vista|2008Server)
lockV2 fork/dankert-download pr9999 .+ Python 3.11
'''


class FakeUpdater(Updater):
    current_version = '2022.01.01'
    current_commit = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    _channel = 'stable'
    _origin = 'dankert-download/dankert-download'
    _update_sources = TEST_UPDATE_SOURCES

    def _download_update_spec(self, *args, **kwargs):
        return TEST_LOCKFILE_ACTUAL

    def _call_api(self, tag):
        tag = f'tags/{tag}' if tag != 'latest' else tag
        return TEST_API_DATA[f'{self.requested_repo}/{tag}']

    def _report_error(self, msg, *args, **kwargs):
        report_warning(msg)


class TestUpdate(unittest.TestCase):
    maxDiff = None

    def test_update_spec(self):
        ydl = FakeYDL()
        updater = FakeUpdater(ydl, 'stable')

        def test(lockfile, identifier, input_tag, expect_tag, exact=False, repo='dankert-download/dankert-download'):
            updater._identifier = identifier
            updater._exact = exact
            updater.requested_repo = repo
            result = updater._process_update_spec(lockfile, input_tag)
            self.assertEqual(
                result, expect_tag,
                f'{identifier!r} requesting {repo}@{input_tag} (exact={exact}) '
                f'returned {result!r} instead of {expect_tag!r}')

        for lockfile in (TEST_LOCKFILE_V1, TEST_LOCKFILE_V2, TEST_LOCKFILE_ACTUAL, TEST_LOCKFILE_FORK):
            # Normal operation
            test(lockfile, 'zip Python 3.12.0', '2023.12.31', '2023.12.31')
            test(lockfile, 'zip Python 3.12.0', '2023.12.31', '2023.12.31', exact=True)
            # py2exe should never update beyond 2024.10.22
            test(lockfile, 'py2exe Python 3.8', '2025.01.01', '2024.10.22')
            test(lockfile, 'py2exe Python 3.8', '2025.01.01', None, exact=True)
            # Python 3.6 --update should update only to the py3.6 lock
            test(lockfile, 'zip Python 3.6.0', '2023.11.16', '2022.08.18.36')
            # Python 3.6 --update-to an exact version later than the py3.6 lock should return None
            test(lockfile, 'zip Python 3.6.0', '2023.11.16', None, exact=True)
            # Python 3.7 should be able to update to the py3.7 lock
            test(lockfile, 'zip Python 3.7.0', '2023.11.16', '2023.11.16')
            test(lockfile, 'zip Python 3.7.1', '2023.11.16', '2023.11.16', exact=True)
            # Non-win_x86_exe builds on py3.7 must be locked at py3.7 lock
            test(lockfile, 'zip Python 3.7.1', '2023.12.31', '2023.11.16')
            test(lockfile, 'zip Python 3.7.1', '2023.12.31', None, exact=True)
            # Python 3.8 should only update to the py3.8 lock
            test(lockfile, 'zip Python 3.8.10', '2025.01.01', '2024.10.22')
            test(lockfile, 'zip Python 3.8.110', '2025.01.01', None, exact=True)
            test(  # Windows Vista w/ win_x86_exe must be locked at Vista lock
                lockfile, 'win_x86_exe Python 3.7.9 (CPython x86 32bit) - Windows-Vista-6.0.6003-SP2',
                '2023.12.31', '2023.11.16')
            test(  # Windows 2008Server w/ win_x86_exe must be locked at Vista lock
                lockfile, 'win_x86_exe Python 3.7.9 (CPython x86 32bit) - Windows-2008Server',
                '2023.12.31', None, exact=True)
            test(  # Windows 7 w/ win_x86_exe py3.7 build should be able to update beyond py3.7 lock
                lockfile, 'win_x86_exe Python 3.7.9 (CPython x86 32bit) - Windows-7-6.1.7601-SP1',
                '2023.12.31', '2023.12.31', exact=True)
            test(  # Windows 7 win_x86_exe should only update to Win7 lock
                lockfile, 'win_x86_exe Python 3.7.9 (CPython x86 32bit) - Windows-7-6.1.7601-SP1',
                '2025.01.01', '2024.10.22')
            test(  # Windows 2008ServerR2 win_exe should only update to Win7 lock
                lockfile, 'win_exe Python 3.8.10 (CPython x86 32bit) - Windows-2008ServerR2',
                '2025.12.31', '2024.10.22')
            test(  # Windows 8.1 w/ '2008Server' in platform string should be able to update beyond py3.7 lock
                lockfile, 'win_x86_exe Python 3.7.9 (CPython x86 32bit) - Windows-post2008Server-6.2.9200',
                '2023.12.31', '2023.12.31', exact=True)
            test(  # win_exe built w/Python 3.8 on Windows>=8 should be able to update beyond py3.8 lock
                lockfile, 'win_exe Python 3.8.10 (CPython AMD64 64bit) - Windows-10-10.0.20348-SP0',
                '2025.01.01', '2025.01.01', exact=True)
            test(  # linux_armv7l_exe w/glibc2.7 should only update to glibc<2.31 lock
                lockfile, 'linux_armv7l_exe Python 3.8.0 (CPython armv7l 32bit) - Linux-6.5.0-1025-azure-armv7l-with-glibc2.7',
                '2025.01.01', '2024.10.22')
            test(  # linux_armv7l_exe w/Python 3.8 and glibc>=2.31 should be able to update beyond py3.8 and glibc<2.31 locks
                lockfile, 'linux_armv7l_exe Python 3.8.0 (CPython armv7l 32bit) - Linux-6.5.0-1025-azure-armv7l-with-glibc2.31',
                '2025.01.01', '2025.01.01')
            test(  # linux_armv7l_exe w/glibc2.30 should only update to glibc<2.31 lock
                lockfile, 'linux_armv7l_exe Python 3.8.0 (CPython armv7l 64bit) - Linux-6.5.0-1025-azure-aarch64-with-glibc2.30 (OpenSSL',
                '2025.01.01', '2024.10.22')
            test(  # linux_aarch64_exe w/glibc2.17 should only update to glibc<2.31 lock
                lockfile, 'linux_aarch64_exe Python 3.8.0 (CPython aarch64 64bit) - Linux-6.5.0-1025-azure-aarch64-with-glibc2.17',
                '2025.01.01', '2024.10.22')
            test(  # linux_aarch64_exe w/glibc2.40 and glibc>=2.31 should be able to update beyond py3.8 and glibc<2.31 locks
                lockfile, 'linux_aarch64_exe Python 3.8.0 (CPython aarch64 64bit) - Linux-6.5.0-1025-azure-aarch64-with-glibc2.40',
                '2025.01.01', '2025.01.01')
            test(  # linux_aarch64_exe w/glibc2.3 should only update to glibc<2.31 lock
                lockfile, 'linux_aarch64_exe Python 3.8.0 (CPython aarch64 64bit) - Linux-6.5.0-1025-azure-aarch64-with-glibc2.3 (OpenSSL',
                '2025.01.01', '2024.10.22')

        # Forks can block updates to non-numeric tags rather than lock
        test(TEST_LOCKFILE_FORK, 'zip Python 3.6.3', 'pr0000', None, repo='fork/dankert-download')
        test(TEST_LOCKFILE_FORK, 'zip Python 3.7.4', 'pr0000', 'pr0000', repo='fork/dankert-download')
        test(TEST_LOCKFILE_FORK, 'zip Python 3.7.4', 'pr1234', None, repo='fork/dankert-download')
        test(TEST_LOCKFILE_FORK, 'zip Python 3.8.1', 'pr1234', 'pr1234', repo='fork/dankert-download', exact=True)
        test(
            TEST_LOCKFILE_FORK, 'win_x86_exe Python 3.7.9 (CPython x86 32bit) - Windows-Vista-6.0.6003-SP2',
            'pr1234', None, repo='fork/dankert-download')
        test(
            TEST_LOCKFILE_FORK, 'win_x86_exe Python 3.7.9 (CPython x86 32bit) - Windows-7-6.1.7601-SP1',
            '2023.12.31', '2023.12.31', repo='fork/dankert-download')
        test(TEST_LOCKFILE_FORK, 'zip Python 3.11.2', 'pr9999', None, repo='fork/dankert-download', exact=True)
        test(TEST_LOCKFILE_FORK, 'zip Python 3.12.0', 'pr9999', 'pr9999', repo='fork/dankert-download')

    def test_query_update(self):
        ydl = FakeYDL()

        def test(target, expected, current_version=None, current_commit=None, identifier=None):
            updater = FakeUpdater(ydl, target)
            if current_version:
                updater.current_version = current_version
            if current_commit:
                updater.current_commit = current_commit
            updater._identifier = identifier or 'zip'
            update_info = updater.query_update(_output=True)
            self.assertDictEqual(
                update_info.__dict__ if update_info else {}, expected.__dict__ if expected else {})

        test('dankert-download/dankert-download@latest', UpdateInfo(
            '2023.12.31', version='2023.12.31', requested_version='2023.12.31', commit='b' * 40))
        test('dankert-download/dankert-download-nightly-builds@latest', UpdateInfo(
            '2023.12.31.123456', version='2023.12.31.123456', requested_version='2023.12.31.123456', commit='c' * 40))
        test('dankert-download/dankert-download-master-builds@latest', UpdateInfo(
            '2023.12.31.987654', version='2023.12.31.987654', requested_version='2023.12.31.987654', commit='d' * 40))
        test('fork/dankert-download@latest', UpdateInfo(
            '2050.12.31', version='2050.12.31', requested_version='2050.12.31', commit='e' * 40))
        test('fork/dankert-download@pr0000', UpdateInfo(
            'pr0000', version='2023.11.11.000000', requested_version='2023.11.11.000000', commit='f' * 40))
        test('fork/dankert-download@pr1234', UpdateInfo(
            'pr1234', version='2023.12.31.555555', requested_version='2023.12.31.555555', commit='0' * 40))
        test('fork/dankert-download@pr9999', UpdateInfo(
            'pr9999', version=None, requested_version=None, commit='1' * 40))
        test('fork/dankert-download-satellite@pr987', UpdateInfo(
            'pr987', version=None, requested_version=None, commit='2' * 40))
        test('dankert-download/dankert-download', None, current_version='2024.01.01')
        test('stable', UpdateInfo(
            '2023.12.31', version='2023.12.31', requested_version='2023.12.31', commit='b' * 40))
        test('nightly', UpdateInfo(
            '2023.12.31.123456', version='2023.12.31.123456', requested_version='2023.12.31.123456', commit='c' * 40))
        test('master', UpdateInfo(
            '2023.12.31.987654', version='2023.12.31.987654', requested_version='2023.12.31.987654', commit='d' * 40))
        test('testing', None, current_commit='9' * 40)
        test('testing', UpdateInfo('testing', commit='9' * 40))


if __name__ == '__main__':
    unittest.main()
