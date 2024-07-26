from dataclasses import dataclass
from enum import StrEnum, auto

@dataclass
class NodeType:
  iosv = auto()
  iosvl2 = auto()
  unmanaged_switch = auto()
  server = auto()
  ubuntu = auto()
  vyos = auto()