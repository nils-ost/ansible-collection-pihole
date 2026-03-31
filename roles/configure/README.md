# nils_ost.pihole.configure

**configures basic PiHole features**

Version added: 1.0.0

- [Synopsis](#synopsis)
- [Role Variables](#role-variables)
  - [Structure of: pihole\_upstream\_servers](#structure-of-pihole_upstream_servers)
    - [Example (default value)](#example-default-value)
  - [Structure of: pihole\_config](#structure-of-pihole_config)
    - [Example (default value)](#example-default-value-1)
  - [Structure of: pihole\_local\_a\_records](#structure-of-pihole_local_a_records)
    - [Example](#example)


## Synopsis

configures PiHole with some basic / most common features. requires already running PiHole instance (e.g. through role `nils_ost.pihole.install_with_docker`)


## Role Variables

| Variable                | Type | Default      | Comment                                                                                   |
| ----------------------- | ---- | ------------ | ----------------------------------------------------------------------------------------- |
| pihole_port             | int  | 80           | port to be used for web and API communication                                             |
| pihole_api_password     | str  | secret       | password configured for login (only applys on initial run)                                |
| pihole_disable_logging  | bool | false        | disables DNS-Query logging                                                                |
| pihole_max_api_sessions | int  | 100          | set the maximum concurrent API sessions allowed (see note)                                |
| pihole_local_record_ttl | int  | null         | sets the ttl for `local_a_records` (in seconds), if `null` the line is cleard from config |
| pihole_upstream_servers | list | <see below\> | list of upstream DNS servers to be used                                                   |
| pihole_config           | dict | <see below\> | holds additional configuration parameters (see below)                                     |
| pihole_local_a_records  | dict | {}           | DNS A records to be resolved locally on instance (see below)                              |

> [!NOTE]
> don't set `pihole_max_api_sessions` too low, as this role can create a lot of sessions in short time, that might be exceeded otherwise


### Structure of: pihole_upstream_servers

A list of DNS servers to be configured as upstream servers. For obvious reasons this list can only contain IP-addresses.

#### Example (default value)

You can chose to use any DNS servers you like. The following are configured by default, which are the [openDNS](https://www.opendns.com/) servers.

```yaml
pihole_upstream_servers:
  - 208.67.222.222
  - 208.67.220.220
```


### Structure of: pihole_config

With this dict it is possible to alter any configuration parameter of you PiHole instance, that is not covered by any other variable. For exploring the configuration options, you can use the `nils_ost.pihole.config` module from this collection.

#### Example (default value)

This is the default content of this variable, and should give you an idea how it works:

```yaml
pihole_config:
  dns/rateLimit:
    count: 1000
    interval: 60
  dhcp/active: false
```


### Structure of: pihole_local_a_records

This dict contains a mapping of DNS names (FQDN) to IP addresses which are configured to be resolved locally by PiHole instance.

#### Example

```yaml
pihole_local_a_records:
  router.local.domain: 192.168.0.1
  pihole.local.domain: 192.168.0.2
  host1.local.domain: 192.168.0.55
```
