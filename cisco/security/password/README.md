# demo

+ https://gist.github.com/knknkn1162/9648abc873d294afa4f23005b3a93723

+ @iosv_0:
  + `10.0.0.1`のmetricsの遷移
    + metrics: 1
    + 上の経路が切れる
    + 10.0.0.1のテーブルがずっと更新されない
    + `10.0.0.1, Metric: 16`を送る(経路取り消し情報の送信)
    + possibly down -> ルートテーブルから消える
    + @iosv_1から10.0.0.1, Metric: 2の情報がくる
    + metrics: 2(10.0.0.1 [120/2]) が反映される
      + metrics: 2に変更される


```
---
@iosv_0
#0: 12:19:27 -> start
---
#1: 12:22:11(164[s])
      10.0.0.0/32 is subnetted, 1 subnets
R        10.0.0.1 [120/1] via 192.168.2.3, 00:02:55, GigabitEthernet0/0
R     192.168.1.0/24 [120/1] via 192.168.2.3, 00:02:55, GigabitEthernet0/0
                     [120/1] via 192.168.0.2, 00:00:08, GigabitEthernet0/1
---
@iosv_0 -> iosv_1
169[s]
Routing Information Protocol
    Command: Response (2)
    Version: RIPv2 (2)
    IP Address: 10.0.0.1, Metric: 16
---
#2: 12:22:29(182[s])
      10.0.0.0/32 is subnetted, 1 subnets
R        10.0.0.1/32 is possibly down,
          routing via 192.168.2.3, Gigabi
R     192.168.1.0/24 [120/1] via 192.168.0.2, 00:00:26, GigabitEthernet0/1
---
@iosv_0 <- iosv_1
207[s]
Routing Information Protocol
    Command: Response (2)
    Version: RIPv2 (2)
    IP Address: 10.0.0.1, Metric: 2
    IP Address: 192.168.1.0, Metric: 1
---
@iosv_0 -> iosv_1
229[s]
Routing Information Protocol
    Command: Response (2)
    Version: RIPv2 (2)
    IP Address: 192.168.2.0, Metric: 1
---
#3: 12:23:33(244[s])
      10.0.0.0/32 is subnetted, 1 subnets
R        10.0.0.1 [120/2] via 192.168.0.2, 00:00:06, GigabitEthernet0/1
R     192.168.1.0/24 [120/1] via 192.168.0.2, 00:00:06, GigabitEthernet0/1
```

## dev


```py
# pyenv in advance
python -m venv venv
pip -r requirements.txt
make all
```