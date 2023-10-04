#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community',
}

DOCUMENTATION = '''
---
module: interpreter

short_description: version of ansible python interpreter

'''

EXAMPLES = '''
- name: ansible python interpreter
  interpretor: {}
'''

from ansible.module_utils.basic import AnsibleModule  # noqa: flake8=E402
import sys

def matched(module,result):
    import re
    regex = re.compile(module.params['version'])
    if not regex.match(result['version']):
        module.fail_json(msg=('Interpreter does not match the desired version'), **result)
    result['msg'] = 'Interpreter has the desired version'
    return


def test(module,result):
    if module.check_mode:
        return
    if not module.params['version']:
        return
    matched(module,result)


def run_module():
    result = dict(
        changed=False,
        version=(sys.version.split(' '))[0]
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(version=dict(type='str', required=False))
    )

    test(module,result) 

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
