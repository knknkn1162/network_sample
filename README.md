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
+ router settings
  + [x] `no ip domain-lookup`
  + [x] `logging synchronous`
+ interface
  + [x] show info
    + `show interfaces <int>`
    + `show interfaces <status>`
+ DHCP
  + [x] router as server
    + `ip dhcp pool <pool_name>`
    + `network <network> <subnet_mask>`
    + `default-router <ip_addr>`
    + [x] set expired days
      + `lease 10` (optional)
    + [x] set DNS server ip
      + `dns-server {ip_addr}` (optional)
    + `ip dhcp excluded-address <begin_addr> <end_addr>`
  + [x] router as client
    + `ip address dhcp`
  + [x] relay agent
    + `interface <src_interface>`
    + `ip helper-address <dhcp_ip_addr>`
  + [ ] conflict
  + [x] show info
    + `show ip dhcp binding`
    + `show ip dhcp conflict`
    + `show dhcp lease`
+ WAN
  + NAT
    + [x] Static NAT(SNAT)
      + `interface <int>`
      + `ip nat inside/outside`
      + `ip nat inside source static <inside local> <inside_global>`
    + [x] Dynamic NAT(DNAT)
      + `interface <int>`
      + `ip nat inside/outside`
      + `ip nat pool <label> <start_ip> <end_ip> netmask <subnet_mask>`
      + `ip nat inside source list <acl_num> pool <label>`
    + [x] NAPT(PAT)
      + `interface <int>`
      + `ip nat inside/outside`
      + `ip nat inside source list <acl_num> interface <int_name> overload`
    + show info
      + [x] check NAT table
        + `show ip nat translations`
      + [x] show stat
        + `show ip nat statistics`
    + debug command
      + `debug ip nat`
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
+ switch(L2)
  + vlan
    + [ ] ip address setting (only Catalyst switch?)
      + `interface vlan 1`
      + `ip address <ip_addr> <subnet_mask>`
      + `no shutdown`
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
    + [x] DTP(Dynamic Trunking Protocol)
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
    + [x] change parameter
      + [] change root bridge
        + `spanning-tree vlan <vlan_num> root primary`
      + [] change path cost
        + `spanning-tree vlan <vlan_num> cost <cost>`
        + `spanning-tree pathcost method <short/long>`
      + [x] change port priority
        + `spanning-tree vlan <vlan_num> port-priority <prio>`
    + [x] change topology
      + [x] direct recovery
      + [x] indirect recovery
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
      + [x] show info
        + `show spanning-tree inconsistentports`
    + [ ] loop guard
      + `spanning-tree loopguard default`
    + [x] RSTP(Rapid STP; IEEE 802.1w)
    + [x] PVST+(Per Vlan Spanning Tree+; Cisco)
      + `spanning-tree mode pvst` (default)
    + [x] Rapid PVST+
      + `spanning-tree mode rapid-pvst`
    + [ ] MSTP(Multiple Spanning Tree Protocol; IEEE 802.1s)
    + [ ] show info
      + [ ] check interface
        + `show spanning-tree interface <interface>`
    + [ ] debug info
      + `debug spanning-tree events`
  + EtherChannel
    + [ ] load balance
      + `port-channel load-balance <(src|dst)-(mac|ip|port)>`
    + [ ] by hand
      + `channel-group <group_num> mode on`
    + [ ] PAgP(Cisco)
      + `channel-group <group_num> mode desirable/auto`
      + `channel-protocol pagp`
    + [ ] LACP(IEEE 802.3ad)
      + `channel-group <group_num> mode active/passive`
      + `channel-protocol lacp`
    + [x] show info
      + `show etherchannel <summary/detail>`
      + [x] show load balancer
      + `show etherchannel load-balance`
  + CDP
    + [x] show info
      + `show cdp`
      + `show cdp interface`
      + `show cdp neighbors`
      + `show cdp neighbors detail`
      + `show cdp entry *`
  + LLDP
    + [x] enable
      + `lldp run`
    + [x] show info
      + `show lldp`
      + `show lldp neighbors`
      + `show lldp neighbors detail`
      + `show lldp entry *`
  + L3 switch
    + inter VLAN routing
      + [x] SVI
        + `ip routing`
        + `interface vlan <vlan_id>`
      + [x] routed port
        + `ip routing`
        + `interface <int>`
        + `no switchport`
    + [x] etherChannel
      + (`ip routing`)
      + `no switchport`
      + `channel-group <group_num> mode desirable/auto`
      + `channel-protocol pagp`
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
    + [x] basic settings
      + `interface <int>`
      + `standby <group_num> ip <ip_addr>`
      + `standby <group_num> priority <prio>`
      + `standby <group_num> preempt`
      + `standby <group_num> track <interface> decrement <num>`
    + show info
      + `show standby (brief)`
    + [x] MHSRP(Multiple HSRP)
    + [ ] HSRP with vlan
  + GLBP(ateway Load balancing Protocol; Cisco)
  + VRRP(Virtual Router Redundancy Protocol)
+ QoS
  + IntServ
    + [ ] RSVP(Resource reSerVation Protocol)
  + DiffServ
    + [ ] DSCP(Differentiated Services Code Point
+ ipv6
  + [x] set link local unicast
    + [x] auto
      + `ipv6 enable`
    + [x] manually
      + `ipv6 address <addr> link-local`
  + [x] set global unicast
    + [x] auto(SLAAC: StateLess Address Auto Configuration)
      + `ipv6 address autoconfig`
      + [ ] NDP(Neibor Discovery Protocol)
    + [x] auto(only interface ID) by eui-64
      + `ipv6 address <addr>/<prefix_len> eui-64`
    + [x] manually
      + `ipv6 address <addr>/<prefix_len>`
  + show info
    + [x] ipv6
      + `show ipv6 interface <int>`
    + [x] routing table
      + `show ipv6 route`
  + routing
    + [x] enable IPv6 routing
      + `ipv6 unicast-routing`
    + [x] static routing
      + `ipv6 route <prefix>/<len> <dst_ipv6>`
    + [x] default route
      + `ipv6 route ::/0 <dst_ipv6>`
  + migration
    + [ ] dual stack
    + [ ] translator
      + [ ] NAT-PT
        + `ipv6 nat prefix <subnet>/<prefix_len>`
    + tunneling
      + manual
        + [ ] IPv6
          + `tunnel mode ipv6ip`
        + [ ] GRE
          + `tunnel mode gre ip`
      + auto
        + [ ] 6to4
          + `tunnel mode ipv6ip 6to4`
        + [ ] ISATAP
          + `tunnel mode ipv6ip isatap`