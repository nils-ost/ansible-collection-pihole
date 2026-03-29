#!/usr/bin/python

# Copyright: (c) 2026, Nils Ost <@nils-ost>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule
from pihole6api import PiHole6Client


DOCUMENTATION = r"""
---
module: list

author: Nils Ost (@nils-ost)

version_added: "1.0.0"

short_description: lists all elements

description:
    - Fetches a list of all existing elements from type target

options:
    url:
        description:
            - url of PiHole instance
        required: true
        type: str
    password:
        description:
            - password to authenticate on PiHole instance
        required: true
        type: str
    target:
        description:
            - element type to get list of
        required: false
        type: str
        default: "local_a_record"
        choices: ["local_a_record"]
"""

EXAMPLES = r"""
# fetches all existing local_a_records (domain names)
- name: Pulling existing local_a_record
  nils_ost.pihole.list:
    url: http://pihole.local
    password: somethingsecret
    target: local_a_record
  delegate_to: localhost
  register: existing_local_a_record
"""

RETURN = r"""
data:
    description:
        - list of existing elements of type target
    type: list
    returned: always
"""


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        url=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        target=dict(
            type="str",
            required=False,
            default="local_a_record",
            choices=["local_a_record"],
        ),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        data=list(),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    try:
        c = PiHole6Client(module.params["url"], module.params["password"])

        if module.params["target"] == "local_a_record":
            key = "dns/hosts"
        else:
            module.fail_json(msg="invalid target", **result)

        r = c.config.get_config(key)
        r = r["config"]
        for e in key.split("/"):
            r = r[e]

        if module.params["target"] == "local_a_record":
            for parts in [e.split(None, 1) for e in r]:  # expected format: "ip host"
                if len(parts) == 2 and parts[1] not in result["data"]:
                    result["data"].append(parts[1])

        module.exit_json(msg="fetching list successful", **result)

    except Exception as e:
        module.fail_json(msg=f"Error: {e}", **result)


def main():
    run_module()


if __name__ == "__main__":
    main()
