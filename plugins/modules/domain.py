#!/usr/bin/python

# Copyright: (c) 2026, Nils Ost <home@nijos.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type
from ansible.module_utils.basic import AnsibleModule
from pihole6api import PiHole6Client


DOCUMENTATION = r"""
---
module: domain

short_description: manage domain deny or allow

version_added: "1.0.0"

description:
    - module that is capable of adding or removing domains to and from block- and whitelists
    - always creates entrys with exact match and without group assignment

options:
    url:
        description: url of PiHole instance
        required: true
        type: str
    password:
        description: password to authenticate on PiHole instance
        required: true
        type: str
    domain:
        description: domain to manage
        required: true
        type: str
    list:
        description: list domain should be added to (or removed from either)
        required: false
        type: str
        default: deny
        choices: ["deny", "allow", "remove"]

author:
    - Nils Ost (@nils-ost)
"""

EXAMPLES = r"""
# creates domain test3.local on deny list
- name: create doamin
  nils_ost.pihole.domain:
    url: http://pihole.local
    password: somethingsecret
    domain: test3.local
    list: deny
  delegate_to: localhost

# updates domain test3.local to allow list
- name: create doamin
  nils_ost.pihole.domain:
    url: http://pihole.local
    password: somethingsecret
    domain: test3.local
    list: allow
  delegate_to: localhost

# deletes domain test3.local from either list
- name: create doamin
  nils_ost.pihole.domain:
    url: http://pihole.local
    password: somethingsecret
    domain: test3.local
    list: remove
  delegate_to: localhost
"""

RETURN = r"""
"""


def all_domains(connection):
    result = dict()
    r = connection.domain_management.get_all_domains()
    for d in r.get("whitelist", dict()).get("domains", list()):
        result[d.get("domain", "")] = d
    for d in r.get("blacklist", dict()).get("domains", list()):
        result[d.get("domain", "")] = d
    return result


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        url=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        domain=dict(type="str", required=True),
        list=dict(
            type="str",
            required=False,
            default="deny",
            choices=["deny", "allow", "remove"],
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
        c = PiHole6Client(module.params["url"], module.params["password"])
        domain = all_domains(c).get(module.params["domain"], None)

        if module.params["list"] == "remove" and domain is None:
            module.exit_json(msg="domain already removed", **result)

        elif module.params["list"] == "remove":
            if not module.check_mode:
                c.domain_management.delete_domain(
                    module.params["domain"],
                    domain.get("type"),
                    "exact",
                )
            result["changed"] = True
            module.exit_json(msg="domain removed", **result)

        elif domain is None:
            if not module.check_mode:
                c.domain_management.add_domain(
                    module.params["domain"],
                    module.params["list"],
                    "exact",
                )
            result["changed"] = True
            module.exit_json(msg="domain created", **result)

        elif not domain.get("type", "") == module.params["list"]:
            if not module.check_mode:
                c.domain_management.delete_domain(
                    module.params["domain"],
                    domain.get("type"),
                    "exact",
                )
                c.domain_management.add_domain(
                    module.params["domain"],
                    module.params["list"],
                    "exact",
                )
            result["changed"] = True
            module.exit_json(msg="domain updated", **result)

        else:
            module.exit_json(msg="domain already configured as expected", **result)

    except Exception as e:
        module.fail_json(msg=f"Error managing domain: {e}", **result)

    finally:
        if c is not None:
            c.close_session()


def main():
    run_module()


if __name__ == "__main__":
    main()
