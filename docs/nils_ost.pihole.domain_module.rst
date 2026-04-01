.. _nils_ost.pihole.domain_module:


**********************
nils_ost.pihole.domain
**********************

**manage domain deny or allow**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- module that is capable of adding or removing domains to and from block- and whitelists
- always creates entrys with exact match and without group assignment




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>domain</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>domain to manage</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>deny</b>&nbsp;&larr;</div></li>
                                    <li>allow</li>
                                    <li>remove</li>
                        </ul>
                </td>
                <td>
                        <div>list domain should be added to (or removed from either)</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>password to authenticate on PiHole instance</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>url of PiHole instance</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

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




Status
------


Authors
~~~~~~~

- Nils Ost (@nils-ost)
