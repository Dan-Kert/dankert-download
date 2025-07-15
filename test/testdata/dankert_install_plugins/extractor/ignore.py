from dankert_install.extractor.common import InfoExtractor


class IgnoreNotInAllPluginIE(InfoExtractor):
    pass


class InAllPluginIE(InfoExtractor):
    _VALID_URL = 'inallpluginie'
    pass


__all__ = ['InAllPluginIE']
