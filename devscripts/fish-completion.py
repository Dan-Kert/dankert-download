#!/usr/bin/env python3

# Allow direct execution
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import optparse

import dankert_download
from dankert_download.utils import shell_quote

FISH_COMPLETION_FILE = 'completions/fish/yt-dlp.fish'
FISH_COMPLETION_TEMPLATE = 'devscripts/fish-completion.in'

EXTRA_ARGS = {
    'remux-video': ['--arguments', 'mp4 mkv', '--exclusive'],
    'recode-video': ['--arguments', 'mp4 flv ogg webm mkv', '--exclusive'],

    # Options that need a file parameter
    'download-archive': ['--require-parameter'],
    'cookies': ['--require-parameter'],
    'load-info': ['--require-parameter'],
    'batch-file': ['--require-parameter'],
}


def build_completion(opt_parser):
    commands = []

    for group in opt_parser.option_groups:
        for option in group.option_list:
            long_option = option.get_opt_string().strip('-')
            complete_cmd = ['complete', '--command', 'yt-dlp', '--long-option', long_option]
            if option._short_opts:
                complete_cmd += ['--short-option', option._short_opts[0].strip('-')]
            if option.help != optparse.SUPPRESS_HELP:
                complete_cmd += ['--description', option.help]
            complete_cmd.extend(EXTRA_ARGS.get(long_option, []))
            commands.append(shell_quote(complete_cmd))

    with open(FISH_COMPLETION_TEMPLATE) as f:
        template = f.read()
    filled_template = template.replace('{{commands}}', '\n'.join(commands))
    with open(FISH_COMPLETION_FILE, 'w') as f:
        f.write(filled_template)


parser = dankert_download.parseOpts(ignore_config_files=True)[0]
build_completion(parser)
