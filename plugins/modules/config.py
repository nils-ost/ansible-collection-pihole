#!/usr/bin/python

# Copyright: (c) 2026, Nils Ost <home@nijos.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule
from pihole6api import PiHole6Client


DOCUMENTATION = r"""
---
module: config

short_description: read or write PiHole config key

version_added: "1.0.0"

description:
    - module that is capable to read or write any PiHole config element, but requires specific config-key

options:
    url:
        description: url of PiHole instance
        required: true
        type: str
    password:
        description: password to authenticate on PiHole instance
        required: true
        type: str
    key:
        description: which part of the config to handle (sections are separated by /)
        required: true
        type: str
    value:
        description: the value that the element should get
        required: false (true if action is write)
        type: raw
    action:
        description: action to be performed
        required: false
        type: str
        default: read
        choices: ["read", "write"]

author:
    - Nils Ost (@nils-ost)
"""

EXAMPLES = r"""
# changes the DNS rateLimit
- name: set ratelimit to 2000
  nils_ost.pihole.config:
    url: http://pihole.local
    password: somethingsecret
    key: dns/rateLimit/count
    value: 2000
    action: write
  delegate_to: localhost
"""

RETURN = r"""
value:
    description:
        - value of requested key, or value the key was set to
    type: raw
    returned: always
"""


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        url=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        key=dict(type="str", required=True),
        value=dict(type="raw", required=False),
        action=dict(
            type="str",
            required=False,
            default="read",
            choices=["read", "write"],
        ),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        value=None,
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
        if module.params["action"] == "write" and "value" not in module.params:
            module.fail_json(
                msg="value is required when performing a write action",
                **result,
            )

        c = PiHole6Client(module.params["url"], module.params["password"])
        r = c.config.get_config(module.params["key"])
        if len(r.get("config", {})) == 0:
            module.fail_json(
                msg="the provided key does not point to a config element",
                **result,
            )

        r = r["config"]
        for e in module.params["key"].split("/"):
            r = r[e]

        if module.params["action"] == "read":
            result["value"] = r
            module.exit_json(**result)

        try:
            if r == type(r)(module.params["value"]):
                module.exit_json(**result)  # element does already have desired value
        except Exception:
            module.fail_json(
                msg="desired value does not have the correct value-type",
                **result,
            )

        if not module.check_mode:
            r = type(r)(module.params["value"])
            result["value"] = r  # save typed value for result
            for e in reversed(module.params["key"].split("/")):
                r = {e: r}
            c.config.update_config(r)

        result["changed"] = True
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"Error modifying config element: {e}", **result)

    finally:
        if c is not None:
            c.close_session()


def main():
    run_module()


if __name__ == "__main__":
    main()
