from dataclasses import dataclass
from typing import Any, List


@dataclass
class SubPathArg:
    name: str
    default_value: Any
    mandatory: bool


@dataclass
class SubPath:
    format: str
    args: List[SubPathArg]
