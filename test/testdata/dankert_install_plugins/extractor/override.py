from dankert_install.extractor.generic import GenericIE


class OverrideGenericIE(GenericIE, plugin_name='override'):
    TEST_FIELD = 'override'
