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
+ ACL
  + standard ACL
    + [ ] number
      + `access-list <num> permit/deny <src_ip> <wild_mask>`
      + `interface <int>`
      + `ip access-group <num> in/out`
    + [ ] label
      + `ip access-list standard <label>`
      + `[<seq_num>] [ permit/deny ] <src_ip> <wild_mask>`
      + `interface <int>`
      + `ip access-group <label> in/out`
  + extended ACL
    + [ ] number
      + `access-list <num> permit/deny <proto> <src_ip> <wild_mask> <src_port> <dst_ip> <wild_mask> <dst_port> [ established/log/log-input ]`
      + `interface <int>`
      + `ip access-group <num> [ in | out ]`
    + [ ] label
      + `ip access-list extended <label>`
      + `[<seq_num>] permit/deny <proto> <src_ip> <wild_mask> <src_port> <dst_ip> <wild_mask> <dst_port> [ established/log/log-input ]`
      + `interface <int>`
      + `ip access-group <label> in/out`
  + [ ] vty access control
    + `line vty 0 4`
    + `access-class <num> <in/out>`
  + delete acl
    + `ip access-list standard <num>/<label>`
    + `no <seq_num>`
  + show info
    + [ ] `show access-lists [<num>/<label>]`
    + [ ] `show ip interface <int>`
+ ARP
  + [x] address table
    + `show mac address-table`
+ serial
  + [ ] frame relay
    + `frame-relay switching`
    + `interface <ser>`
    + `clock rate <64000>`
    + `encapsulation frame-relay`
    + `frame-relay intf-type dce`
    + `frame-relay route <> interface <serial_name> <>`
    + `no shutdown`
  + PPP
    + [ ] PAP
      + `username <user> password <pass>`
      + `interface <ser>`
      + `encapsulation ppp`
      + `ppp authentication pap`
      + `ppp pap sent-username <peer_user> password <peer_pass>`
    + [ ] CHAP
      + `username <user> password <pass>`
      + `interface <ser>`
      + `encapsulation ppp`
      + `ppp authentication chap`
      + `ppp chap hostname <peer_user>`
  + PPPoE
    + [ ] client
    + [ ] server
+ security
  + [x] password
    + `line console <num>`
    + `password <pass>`
    + [x] encrypt
      + `service password-encryption`
  + [x] login local
    + `username <user> [privilege <num>] password <pass>`
    + `line console <num>`
    + `login local`
  + [x] enable password
    + `enable secret <pass>`
  + [x] disable auto logout
    + `line console <num>`
    + `exec-timeout 0 0`
  + [x] ssh
    + `ip domain-name {ini.domain_name}`
    + `crypto key generate rsa modulus 1024`
    + `username <username> password <pass>`
    + `ip ssh version 2`
    + `line vty 0 4`
    + `transport input ssh`
    + `login local`
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
    + [ ] change topology
    + [x] PortFast
      + `interface <int>`
      + `spanning-tree portfast`
    + [ ] uplinkFast
      + `spanning-tree uplinkfast`
    + [ ] backboneFast
      + `spanning-tree backbonefast`
    + [x] BPDU guard
      + `interface <int>`
      + `spanning-tree bpduguard enable`
    + [ ] (BPDU filtering)
      + `spanning-tree bpdufilter enable`
    + [x] root guard
      + `spanning-tree guard root`
    + [ ] loop guard
      + `spanning-tree loopguard default`
    + [x] RSTP(Rapid STP; IEEE 802.1w)
    + [x] PVST+(Per Vlan Spanning Tree+)
      + `spanning-tree mode pvst` (default)
    + [x] Rapid PVST+
      + `spanning-tree mode rapid-pvst`
    + [ ] MSTP(Multiple Spanning Tree Protocol; IEEE 802.1s)
  + EtherChannel
    + [ ] load balance
      + `port-channel load-balance <opt>`
    + [ ] PAgP(Cisco)
      + `channel-group <group_num> mode desirable/auto`
      + `channel-protocol pagp`
    + [ ] LACP(IEEE 802.3ad)
      + `channel-group <group_num> mode active/passive`
      + `channel-protocol lacp`
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
  + show info
    + [x] `show ip route`
    + [x] `show ip interface [brief]`
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
  + EIGRP(Cisco)
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
    + show info
      + [x] neighbor table
        + `show ip ospf neighbor`
      + [x] LSDB
        + `show ip ospf database`
      + [x] route table
        + `show ip route`
      + [x] show protocol info
        + `show ip protocols`
      + [x] check interface
        + `show ip ospf interface <int>`
    + [x] DR, BDR
      + [ ] restart ospf process
        + `clear ip ospf process`
    + [x] change priority, cost
      + `ip ospf priority <val>`
      + `ip ospf cost <val>`
      + (`bandwidth <num>`)
    + [ ] advertise default route
      + `default-information originate`
    + [ ] passive interface
      + `passive-interface <interface>`
    + [ ] MTU ignore
      + `ip ospf mtu-ignore`
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
+ FHRP(First Hop Redandancy Protocol)
  + HSRP(Hot Standby Router Protocol; Cisco)
  + GLBP(ateway Load balancing Protocol; Cisco)
  + VRRP(Virtual Router Redundancy Protocol)