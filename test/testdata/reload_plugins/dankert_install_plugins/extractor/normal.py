from dankert_download.extractor.common import InfoExtractor


class NormalPluginIE(InfoExtractor):
    _VALID_URL = 'normal'
    REPLACED = True


class _IgnoreUnderscorePluginIE(InfoExtractor):
    pass
