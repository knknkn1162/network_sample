# cml2_sample

## prerequisites

+ windows PC
  + CML2 (as server)
  + ngrok
+ mac or linux
  + this repo
    + virl2_client
    + pyats
      + genie
      + testbed
      + ...


```sh
make all
# or make rtest for the 2nd time
make test
```

# TODO

+ DHCP
  + [x] router as server
  + [x] router as client
  + [x] relay agent
  + [ ] conflict
+ WAN
  + NAT
    + [x] Static NAT(SNAT)
    + [x] Dynamic NAT(DNAT)
    + [x] NAPT(PAT)
+ switch
  + vlan
    + [x] access port
      + `interface <int>`
      + `switchport mode access`
      + `switchport access vlan <vlan_num>`
    + [x] trunk port
      + `interface <int>`
      + `switchport trunk encapsulation dot1q`
      + `switchport mode trunk`
    + [x] default gateway on switch
      + `ip default-gateway <ip_addr>`
    + [ ] voice vlan
      + `switchport mode access`
      + `switchport voice vlan <vlan_phone_num>`
      + (`switchport access vlan <vlan2_num>`) for server
    + [ ] DTP
      + `switchport mode dynamic <auto/desirable>`
    + [x] sub interface
    + [x] VTP
    + [x] SVI
      + `ip routing`
      + `interface vlan <vlan_id>`
    + [x] routed port
      + `ip routing`
      + `interface <int>`
      + `no switchport`
  + L3 switch
    + 
+ routing
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
    + [x] split horizen
    + [x] poison reverse
    + [ ] hold-down timer
    + [ ] distribute default routing
      + `default-information originate`
    + [ ] triggered update
    + [x] check hop limit <= 15
      + `offset-list <acl-num> in/out <add-hop-count> <interface>`
    + [x] passive interface
      + `passive-interface <interface>`
    + [ ] neighbor(unicast)
      + `router rip`
      + `neighbor <address>`
    + [x] redistribute static
      + `router rip`
      + `redistribute static metric 1`
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
      + static route
        + `ip route 0.0.0.0 0.0.0.0 <addr>`
        + `router eigrp <as_num>`
        + `redistribute static metric 1`
    + [ ] set distribute list
      + `router eigrp <as_num>`
      + `distribute-list <acl_num> out <interface>`
  + OSPF
    + [x] DR, BDR
    + [x] change priority, cost
      + `ip ospf priority <val>`
      + `ip ospf cost <val>`
    + advertise default route
      + `default-information originate`
    + passive interface
      + `passive-interface <interface>`
    + single area
      + [x] AS = 1
      + [ ] AS = 2
    + multi area
      + [x] Standard area
      + [ ] Stub area
      + [ ] Totally Stubby Area(TSA)
      + [ ] Not-So-Stubby Area(NSSA)
      + [ ] Totally Not-So-Stubby Area (T-NSSA)
      + [ ] virtual link
  + BGP
    + [ ] eBGP peer
    + [ ] iBGP peer
    + [ ] best path
    + [ ] redistribute
    + [ ] route summary
    + [ ] route reflector
    + [ ] confederation