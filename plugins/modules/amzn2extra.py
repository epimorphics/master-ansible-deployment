#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright: (c) 2019, Kazuya Takei <attakei@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

DOCUMENTATION = '''
---
module: amzn2extra

short_description: Manage topics of amazon-linux-extras

version_added: "2.8"

description:
  - "Manage topics of amazon-linux-extras"

options:
  name:
    description:
      - Topic name
    required: true
  state:
    description:
      - Set "present" To enable, and set "absent" to disable
    required: true
    choices: [ "absent", "present" ]
    default: "present"
'''

EXAMPLES = '''
# Enable "vim" topic
- name: Enable vim
  amzn2extra:
    name: vim
'''

from ansible.module_utils.basic import AnsibleModule  # noqa: flake8=E402


COMMAND_PATH = '/usr/bin/amazon-linux-extras'


class Topic(object):
    """Topic on amazon extra library
    """
    def __init__(self, name, version, status):
        self.name = name
        self.version = version
        self.status = status

def from_text(line):
    import re
    regex = re.compile(
        r'\s+[-_\d]+\s.'
        r'(?P<name>\S+)\s+'
        r'(?P<status>\S+)\s+'
        r'.+'
    )
    matched = regex.match(line)
    if matched:
        name_version = matched.group('name').split('=')
        name = name_version[0]
        version = name_version[1] if len(name_version) > 1 else None
        status = matched.group('status')
        return Topic(name, version, status)


# TODO: Test cases are not exists
def fetch_list(module):
    cmd = [COMMAND_PATH, 'list']
    rc, out, err = module.run_command(cmd)
    topics = []
    append_cur_line = False
    l = ''
    for o in out.split('\n'):
        if o == '':
            continue
        l += o.rstrip('\\') 
        if not o.endswith('\\'):
            t = from_text(l)
            if t:
                topics.append(t)
            l = ''
    return topics


def update_topic_state(module, topic, next_state):
    subcommand = 'enable' if next_state == 'present' else 'disable'
    cmd = [COMMAND_PATH, subcommand, topic.name]
    rc, out, err = module.run_command(cmd)
    return rc == 0


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=False, default='present'),
    )

    result = dict(
        changed=False,
        original_message='',
        message='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(**result)

    topic_name = module.params['name']
    topic_state = module.params['state']
    # Topic matching
    # TODO: Not test
    extras = fetch_list(module)
    topics = [e for e in extras if e.name == topic_name]
    if not topics:
        module.fail_json(msg=('Topic %s not found' % topic_name), **result)

    topic = topics[0]
    if topic_state == 'present' and topic.status == 'enabled':
        # Not run (already enabled)
        pass
    elif topic_state == 'absent' and topic.status == 'available':
        # Not run (already disabled)
        pass
    else:
        # TODO: It is stub
        cmd_ok = update_topic_state(module, topic, topic_state)
        if not cmd_ok:
            module.fail_json(msg=('Toggle on topic %s failed' % topic_name), **result)
        result['changed'] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
