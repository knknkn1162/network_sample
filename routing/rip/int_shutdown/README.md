# demo

+ before

```
      10.0.0.0/32 is subnetted, 1 subnets
R        10.0.0.1 [120/1] via 192.168.2.3, 00:01:23, GigabitEthernet0/0
R     192.168.1.0/24 [120/1] via 192.168.2.3, 00:01:23, GigabitEthernet0/0
                     [120/1] via 192.168.0.2, 00:00:08, GigabitEthernet0/1
```

+ after

```
Gateway of last resort is not set

      10.0.0.0/32 is subnetted, 1 subnets
R        10.0.0.1 [120/2] via 192.168.0.2, 00:00:19, GigabitEthernet0/1
R     192.168.1.0/24 [120/1] via 192.168.0.2, 00:00:19, GigabitEthernet0/1
```

## dev


```py
# pyenv in advance
python -m venv venv
pip -r requirements.txt
make all
```