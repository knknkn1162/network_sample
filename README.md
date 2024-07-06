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
    + [ ] flash vlan dat
      + (only Catalyst switch)
      + `erase startup-config`
      + `delete flash:vlan.dat`
      + `reload`
    + [x] access port
      + `interface <int>`
      + `switchport mode access`
      + `switchport access vlan <vlan_num>`
    + [x] trunk port
      + `interface <int>`
      + `switchport trunk encapsulation dot1q`
      + `switchport mode trunk`
      + [ ] ISL
        + `switchport trunk encapsulation isl`(not supported in iosvl2)
      + [x] IEEE 802.1Q
        + `switchport trunk encapsulation dot1q`
      + [ ] native vlan
        + `switchport trunk native vlan <vlan_num>`
    + [x] default gateway on switch
      + `ip default-gateway <ip_addr>`
    + [ ] voice vlan
      + `switchport mode access`
      + `switchport voice vlan <vlan_phone_num>`
      + (`switchport access vlan <vlan2_num>`) for server
    + [x] DTP
      + `switchport mode dynamic <auto/desirable>`
    + inter VLAN routing
      + [x] Router on a stick
        + `encapsulation <dot1q/isl> <vlan_num>`
      + [x] sub interface
        + `interface <int>.<sub_num>`
    + [x] VTP
      + `vtp domain <domain_name>`
      + `vtp mode <server/transparent/client>`
  + STP(IEEE 802.1D)
    + [ ] Root
    + [ ] change topology
    + [ ] PortFast
      + `interface <int>`
      + `spanning-tree portfast`
    + [ ] uplinkFast
      + `spanning-tree uplinkfast`
    + [ ] backboneFast
      + `spanning-tree backbonefast`
    + [ ] BPDU guard
      + `interface <int>`
      + `spanning-tree bpduguard enable`
    + [ ] (BPDU filtering)
      + `spanning-tree bpdufilter enable`
    + [ ] root guard
      + `spanning-tree guard root`
    + [ ] loop guard
      + `spanning-tree loopguard default`
    + [ ] RSTP(Rapid STP; IEEE 802.1w)
    + [ ] PVST+(Per Vlan Spanning Tree+)
    + [ ] MSTP(Multiple Spanning Tree Protocol)
  + L3 switch
    + inter VLAN routing
      + [x] SVI
        + `ip routing`
        + `interface vlan <vlan_id>`
      + [x] routed port
        + `ip routing`
        + `interface <int>`
        + `no switchport`
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