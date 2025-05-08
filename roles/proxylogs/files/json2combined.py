#! /usr/bin/python3

import json
import fileinput

for line in fileinput.input():
    line.rstrip()

    l = json.loads(line)

    print('{}:- {} {} [{}] "{} {} {}" {} {} "{}" "{}"'.format(
        l.get('host', '-'),
        l.get('log_client', l.get('log_remote_ip',l.get('log_client_ip', '-'))),
        l.get('log_user', '-'),
        l.get('log_localtime', '-'),
        l.get('log_method', '-'),
        l.get('log_path', l.get('log_request_uri', '-')),
        l.get('log_protocol', '-'),
        l.get('log_code', l.get('log_status', '-')),
        l.get('log_size', '-'),
        l.get('log_referrer', l.get('log_referer', '-')),
        l.get('log_agent', '-')
        )
    )
