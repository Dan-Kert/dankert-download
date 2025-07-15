from dankert_install.extractor.generic import GenericIE


class _UnderscoreOverrideGenericIE(GenericIE, plugin_name='underscore-override'):
    SECONDARY_TEST_FIELD = 'underscore-override'
