import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files


def pycryptodome_module():
    """
    Возвращает имя криптомодуля для hiddenimports.
    Предпочтительно использовать Cryptodome (pycryptodomex).
    Crypto (pycrypto) устарел и не рекомендуется.
    """
    try:
        import Cryptodome  # noqa: F401
        return 'Cryptodome'
    except ImportError:
        try:
            import Crypto  # noqa: F401
            print('WARNING: Using Crypto since Cryptodome is not available. '
                  'Install with: python3 -m pip install pycryptodomex', file=sys.stderr)
            return 'Crypto'
        except ImportError:
            pass
    # Если ничего не найдено, возвращаем Cryptodome для PyInstaller
    return 'Cryptodome'

def get_hidden_imports():
    yield from ('dankert_download.compat._legacy', 'dankert_download.compat._deprecated')
    yield from ('dankert_download.utils._legacy', 'dankert_download.utils._deprecated')
    yield pycryptodome_module()
    # Only `websockets` is required, others are collected just in case
    for module in ('websockets', 'requests', 'urllib3'):
        yield from collect_submodules(module)
    # These are auto-detected, but explicitly add them just in case
    yield from ('mutagen', 'brotli', 'certifi', 'secretstorage', 'curl_cffi')


hiddenimports = list(get_hidden_imports())
print(f'Adding imports: {hiddenimports}')

excludedimports = ['youtube_dl', 'youtube_dlc', 'test', 'ytdlp_plugins', 'devscripts', 'bundle']

datas = collect_data_files('curl_cffi', includes=['cacert.pem'])
