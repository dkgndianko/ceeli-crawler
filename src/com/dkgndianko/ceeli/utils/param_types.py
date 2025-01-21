from dataclasses import dataclass
from typing import Any, List


@dataclass
class TemplateArg:
    name: str
    default_value: Any
    mandatory: bool


@dataclass
class Template:
    format: str
    args: List[TemplateArg]
