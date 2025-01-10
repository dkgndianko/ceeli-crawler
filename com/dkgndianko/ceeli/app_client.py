from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Dict, Optional

from com.dkgndianko.ceeli.base_client import BaseClient


DEFAULT_HOME_PATH = "/"
HOME_NAME = "home"
@dataclass
class SubPathArg:
    name: str
    default_value: Any
    mandatory: bool
@dataclass
class SubPath:
    format: str
    args: List[SubPathArg]


def parse_path(input_format: str) -> SubPath:
    without_leading_slash = input_format[1:] if input_format.startswith("/") else input_format
    return SubPath(format=without_leading_slash, args=[])


class AppClient(BaseClient):
    def __init__(self, base_url: str, user_data_dir: Path, silent: Optional[bool] = False,
                 headless: Optional[bool] = False, detached: Optional[bool] = False):
        super().__init__(user_data_dir, silent, headless, detached)
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.sub_paths: Dict[str, SubPath] = {}
        self.register_sub_path(HOME_NAME, DEFAULT_HOME_PATH)

    def register_sub_path(self, name: str, sub_path: str) -> None:
        """

        :param name: The name of the sub path to use after when calling :func: `go_to_path`
        :param sub_path: The formatting of the sub path \
        e.g "/clients/{clientId}
        /export/{format:pdf} -> here 'pdf' is the default value of format that will be used if not given
        :return:
        """
        sub_path = parse_path(sub_path)
        self.sub_paths[name] = sub_path

    def _get_url(self, name, **kwargs) -> str:
        try:
            sub_path = self.sub_paths[name]
        except KeyError:
            raise ValueError(f"no sub path with name ${name} registered. User the {self.register_sub_path.__name__} method to register")
        arg_val = {}
        for arg_def in sub_path.args:
            val = kwargs.get(arg_def.name) or arg_def.default_value
            if not val and arg_def.mandatory:
                raise ValueError(f"Argument {arg_def.name} is mandatory and not given")
            arg_val[arg_def.name] = val
        path = sub_path.format.format(**arg_val)
        return f"{self.base_url}/{path}"

    def home(self):
        self.go_to_path(HOME_NAME)

    def go_to_path(self, name, **kwargs):
        url = self._get_url(name, **kwargs)
        self.go_to(url)
