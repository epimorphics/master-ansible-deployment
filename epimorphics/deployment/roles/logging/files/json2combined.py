#! /usr/bin/python3

import json
import fileinput

for line in fileinput.input():
    line.rstrip()

    l = json.loads(line)

    print('{}:{} {} {} [{}] "{} {} {}" {} {} "{}" "{}"'.format(
        l.get('host', '-'),
        l.get('post', '-'),
        l.get('log_host', '-'),
        l.get('log_user', '-'),
        l.get('log_localtime', '-'),
        l.get('log_method', '-'),
        l.get('log_path', '-'),
        l.get('log_protocol', '-'),
        l.get('log_status', '-'),
        l.get('log_size', '-'),
        l.get('log_referrer', '-'),
        l.get('log_agent', '-')
        )
    )
