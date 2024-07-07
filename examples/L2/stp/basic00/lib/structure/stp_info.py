from dataclasses import dataclass
from enum import StrEnum, auto

class Role(StrEnum):
    designated = auto()
    root = auto()
    alternate = auto()

class StpType(StrEnum):
    p2p = 'P2p'

class State(StrEnum):
    forwarding = auto()
    blocking = auto()


# #{'cost': 4, 'port_priority': 128, 'port_num': 1, 'role': 'designated', 'port_state': 'forwarding', 'type': 'P2p'}
@dataclass
class StpInfo:
    cost: int
    port_priority: int
    port_num: int
    role: Role
    port_state: State
    type: StpType