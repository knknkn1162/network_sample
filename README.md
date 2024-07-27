# TODO

+ cisco
  + [README.md](./cisco/README.md)
+ vyos
  + [README.md](./vyos/README.md)


# gns3

## testbed

### iosv

```yaml
devices:
  R1:
    connections:
      a:
        ip: ${ip_addr}
        protocol: telnet
        port: ${port}
      defaults:
        class: unicon.Unicon
    os: ios
    platform: iosv
    type: router
```

### vyos

```yaml
devices:
  vyos99:
    connections:
      a:
        ip: ${ip_addr}
        protocol: telnet
        port: ${port}
      defaults:
        class: unicon.Unicon
    credentials:
      default:
        password: vyos
        username: vyos
    os: linux
    type: linux
```

### vpcs

```yaml
devices:
  pc0:
    connections:
      a:
        ip: ${ip_addr}
        protocol: telnet
        port: ${port}
      defaults:
        class: unicon.Unicon
    os: linux
    type: linux
```