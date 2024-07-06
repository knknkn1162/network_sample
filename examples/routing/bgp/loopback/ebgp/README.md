# demo

```
iosv_1 -> iosv_0
Border Gateway Protocol - UPDATE Message
    Marker: ffffffffffffffffffffffffffffffff
    Length: 23
    Type: UPDATE Message (2)
    Withdrawn Routes Length: 0
    Total Path Attribute Length: 0
---
iosv_0 -> iosv_1
Border Gateway Protocol - UPDATE Message
    Marker: ffffffffffffffffffffffffffffffff
    Length: 23
    Type: UPDATE Message (2)
    Withdrawn Routes Length: 0
    Total Path Attribute Length: 0
---
iosv_1 -> iosv_0
Path attributes
    Path Attribute - ORIGIN: IGP
    Path Attribute - AS_PATH: 10 
    Path Attribute - NEXT_HOP: 192.168.1.3 
    Path Attribute - MULTI_EXIT_DISC: 0
    Path Attribute - LOCAL_PREF: 100

iosv_1 -> iosv_2
Border Gateway Protocol - UPDATE Message
    Marker: ffffffffffffffffffffffffffffffff
    Length: 23
    Type: UPDATE Message (2)
    Withdrawn Routes Length: 0
    Total Path Attribute Length: 0
---
iosv_2 -> iosv_1
Path attributes
    Path Attribute - ORIGIN: IGP
    Path Attribute - AS_PATH: 10 
    Path Attribute - NEXT_HOP: 192.168.1.3 
    Path Attribute - MULTI_EXIT_DISC: 0

```



## dev


```py
# pyenv in advance
python -m venv venv
pip -r requirements.txt
make all
```