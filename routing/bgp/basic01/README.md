# demo

```
@ iosv_0 <-> iosv_1
No.	Time	Source	Destination	Protocol	Length	Info
2	3.787744	192.168.0.2	224.0.0.9	RIPv2	66	Response <- A
4	5.793373	192.168.0.1	224.0.0.9	RIPv2	66	Response <- poison reverse: "16"として192.168.0.2に伝える
7	14.358939	192.168.0.1	224.0.0.9	RIPv2	66	Response 
Routing Information Protocol
    Command: Response (2)
    Version: RIPv2 (2)
    IP Address: 10.0.0.1, Metric: 16 <- split poisoning: 10.0.0.1に関する古い経路情報は転送しない

8	17.351073	192.168.0.2	224.0.0.9	RIPv2	86	Response

@ iosv_1 <-> iosv_2
No.	Time	Source	Destination	Protocol	Length	Info
1	0.000000	192.168.1.3	224.0.0.9	RIPv2	66	Response <- route poisoning
2	2.010058	192.168.1.2	224.0.0.9	RIPv2	66	Response <- A
9	15.267713	192.168.1.2	224.0.0.9	RIPv2	86	Response
Routing Information Protocol
    Command: Response (2)
    Version: RIPv2 (2)
    IP Address: 10.0.0.1, Metric: 16 <- split poisoning: 10.0.0.1に関する古い経路情報は転送しない
    IP Address: 192.168.0.0, Metric: 1
```



## dev


```py
# pyenv in advance
python -m venv venv
pip -r requirements.txt
make all
```