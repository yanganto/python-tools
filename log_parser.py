#!/usr/bin/env python
""" log_parser
current only for tornado server

SOURCE
	https://github.com/yanganto/python-tools/blob/master/log_parser.py
"""

import shutil
from collections import Counter
from os import path
from datetime import datetime


def tornado_log_parser(file_path, common_uri_error=3):
    error_counter = Counter()
    ip_counter = Counter()
    uri_counter = Counter()
    unhandle_logs = []

    with open(file_path, 'r') as log:
        for line in log:
            li = line.split(':', maxsplit=2)
            if len(li) < 3:
                continue
            if li[1] == 'tornado.access':
                try:
                    error_counter[li[2].split(' ')[0]] += 1
                    uri_counter[li[2].split(' ')[2]] += 1
                    ip_counter[li[2].split(' ')[3]] += 1
                except Exception:
                    unhandle_logs.append(line)

    d = datetime.now()
    time = d.isoformat().split('.')[0]
    shutil.move(file_path, path.join(path.dirname(file_path),
                                     path.basename(file_path).replace('.', '.{}.'.format(time))))
    with open(path.join(path.dirname(file_path),
                        path.basename(file_path).replace('.', '.{}_unhandle.'.format(time))), 'w') as fout:
        fout.write(''.join(unhandle_logs))
    return dict(time=time, errors=error_counter.most_common(), uri=uri_counter.most_common(common_uri_error),
                ip=ip_counter.most_common())

