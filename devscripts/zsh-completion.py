#!/usr/bin/env python3

# Allow direct execution
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import dankert_download

ZSH_COMPLETION_FILE = 'completions/zsh/_dankert_download'
ZSH_COMPLETION_TEMPLATE = 'devscripts/zsh-completion.in'


def build_completion(opt_parser):
    opts = [opt for group in opt_parser.option_groups
            for opt in group.option_list]
    opts_file = [opt for opt in opts if opt.metavar == 'FILE']
    opts_dir = [opt for opt in opts if opt.metavar == 'DIR']

    fileopts = []
    for opt in opts_file:
        if opt._short_opts:
            fileopts.extend(opt._short_opts)
        if opt._long_opts:
            fileopts.extend(opt._long_opts)

    diropts = []
    for opt in opts_dir:
        if opt._short_opts:
            diropts.extend(opt._short_opts)
        if opt._long_opts:
            diropts.extend(opt._long_opts)

    flags = [opt.get_opt_string() for opt in opts]

    with open(ZSH_COMPLETION_TEMPLATE) as f:
        template = f.read()

    template = template.replace('{{fileopts}}', '|'.join(fileopts))
    template = template.replace('{{diropts}}', '|'.join(diropts))
    template = template.replace('{{flags}}', ' '.join(flags))

    with open(ZSH_COMPLETION_FILE, 'w') as f:
        f.write(template)


parser = dankert_download.parseOpts(ignore_config_files=True)[0]
build_completion(parser)
