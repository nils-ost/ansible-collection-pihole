# nils_ost.pihole.install_with_docker

**installs PiHole within docker**

Version added: 1.0.0

- [Synopsis](#synopsis)
- [Role Variables](#role-variables)
- [Example](#example)


## Synopsis

A role for installing PiHole as a docker container with the help of compose.

This role mainly just creates the compose directory, places the compose-file and executes `docker compose up`.
It requires docker to be already installed on target system, including the compose plugin.
You might want to take a look at [geerlingguy.docker](https://github.com/geerlingguy/ansible-role-docker) to install docker on your system.


## Role Variables

| Variable            | Type | Default       | Comment                                                       |
| ------------------- | ---- | ------------- | ------------------------------------------------------------- |
| pihole_compose_dir  | str  | /opt/pihole   | location where compose-file and volume directorys are created |
| pihole_auto_upgrade | bool | false         | whether container image is updated on role run or not         |
| pihole_port         | int  | 80            | port to be used for web and API communication                 |
| pihole_timezone     | str  | Europe/Berlin | timezone to be set for container                              |
| pihole_api_password | str  | secret        | password configured for login (only applys on initial run)    |


## Example

`group_vars/pihole.yml`

```yaml
---
pihole_compose_dir: "/opt/services/pihole"
pihole_port: 8080
pihole_api_password: mysecret
```
