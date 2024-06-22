

+ rip
  + [x] no auto-summary
    +  `no auto-summary`
  + [x] route summary
    + `ip summary-address rip <network> <subnetmask>`
  + [x] authentication
    + `ip rip authentication key-chain <chain-name>`
    + `ip rip authentication mode md5`
  + [ ] acl
  + [x] route poisoning(経路取り消し情報の送信)
  + [ ] split horizen
  + [ ] poison reverse
  + [ ] hold-down timer
  + [ ] distribute default routing
    + `default-information originate`
  + [ ] trigger update
  + [x] check hop limit <= 15
    + `offset-list <acl-num> in/out <add-hop-count> <interface>`
  + [x] passive interface
    + `passive-interface <interface>`
  + [ ] neighbor(unicast)
    + `router rip`
    + `neighbor <address>`
  + [ ] redistribute static
    + `router rip`
    + `redistribute static`