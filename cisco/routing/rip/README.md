## tips

+ RIPv2の場合はクラスフル境界の左側に向けたCIDRの集約をサポートしていないので、手動経路集約はエラーになる

```
R     192.168.0.0/24 [120/1] via 10.0.0.2, 00:00:12, GigabitEthernet0/0
R     192.168.1.0/24 [120/1] via 10.0.0.2, 00:00:12, GigabitEthernet0/0
iosv_0(config-if)#ip summary-address rip 192.168.0.0 255.255.254.0
 Summary mask must be greater or equal to major net
```