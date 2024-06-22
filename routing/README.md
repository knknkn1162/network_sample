

+ RIP
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
+ EIGRP
  + [ ] authentication
    + `ip authentication key-chain eigrp <as_num> <chain-name>`
    + `ip authentication mode eigrp <as_num> md5`
  + [ ] split horizon
  + [ ] poison reverse
  + [x] no auto-summary
    +  `no auto-summary`
  + [ ] route summary
    + `ip summary-address eigrp <as_num> <address> <mask> <?AD>`
  + [ ] passive interface
    + `passive-interface <interface>`
  + [x] fix value
    + [x] bandwidth
      + `interface <interface>`
      + `bandwidth <val>`
  + [x] load balance
    + [ ] Equal Cost Load Balancing
      + `router eigrp <as_num>`
      + `maximum-paths <val>`
    + [x] UnEqual Cost Load Balancing
      + `router eigrp <as_num>`
      + `variance <val>`
  + [ ] stub
  + [ ] Redistribute
    + RIP
      + `router rip`
      + `redistribute eigrp <as_num> metric 1`
      + `router eigrp <as_num> metric <v1> <v2> <v3> <v4> <v5>`
      + `redistribute rip`
    + default route
      + `ip route 0.0.0.0 0.0.0.0 <addr>`
      + `router eigrp <as_num>`
      + `redistribute static`
  + [ ] set distribute list
    + `router eigrp <as_num>`
    + `distribute-list <acl_num> out <interface>`