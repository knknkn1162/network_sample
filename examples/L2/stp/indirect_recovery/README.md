# demo

```
#### device iosvl2_0 ####

2024-07-13 12:37:54,977: %UNICON-INFO: +++ iosvl2_0 with via 'a': executing command 'show spanning-tree vlan 10' +++
show spanning-tree vlan 10

VLAN0010
  Spanning tree enabled protocol ieee
  Root ID    Priority    4106
             Address     5254.0006.e77b
             This bridge is the root
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    4106   (priority 4096 sys-id-ext 10)
             Address     5254.0006.e77b
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Desg FWD 4         128.1    P2p 
Gi0/1               Desg FWD 4         128.2    P2p 
Gi0/2               Desg FWD 4         128.3    P2p 


iosvl2_0#
#### device iosvl2_1 ####

2024-07-13 12:37:56,524: %UNICON-INFO: +++ iosvl2_1 with via 'a': executing command 'show spanning-tree vlan 10' +++
show spanning-tree vlan 10

VLAN0010
  Spanning tree enabled protocol ieee
  Root ID    Priority    4106
             Address     5254.0006.e77b
             Cost        4
             Port        1 (GigabitEthernet0/0)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    8202   (priority 8192 sys-id-ext 10)
             Address     5254.000c.ad71
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Root FWD 4         128.1    P2p 
Gi0/1               Desg FWD 4         128.2    P2p 


iosvl2_1#
#### device iosvl2_2 ####

2024-07-13 12:37:58,209: %UNICON-INFO: +++ iosvl2_2 with via 'a': executing command 'show spanning-tree vlan 10' +++
show spanning-tree vlan 10

VLAN0010
  Spanning tree enabled protocol ieee
  Root ID    Priority    4106
             Address     5254.0006.e77b
             Cost        4
             Port        2 (GigabitEthernet0/1)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    12298  (priority 12288 sys-id-ext 10)
             Address     5254.0011.9239
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Desg FWD 4         128.1    P2p 
Gi0/1               Root FWD 4         128.2    P2p 


iosvl2_2#
#### device iosvl2_3 ####

2024-07-13 12:37:59,856: %UNICON-INFO: +++ iosvl2_3 with via 'a': executing command 'show spanning-tree vlan 10' +++
show spanning-tree vlan 10

VLAN0010
  Spanning tree enabled protocol ieee
  Root ID    Priority    4106
             Address     5254.0006.e77b
             Cost        8
             Port        2 (GigabitEthernet0/1)
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    12298  (priority 12288 sys-id-ext 10)
             Address     5254.001f.5e45
             Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  300 sec

Interface           Role Sts Cost      Prio.Nbr Type
------------------- ---- --- --------- -------- --------------------------------
Gi0/0               Altn BLK 4         128.1    P2p 
Gi0/1               Root FWD 4         128.2    P2p 
Gi0/2               Desg FWD 4         128.3    P2p 


iosvl2_3#
```