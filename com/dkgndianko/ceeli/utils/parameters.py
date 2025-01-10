import re
from typing import Tuple, List

from com.dkgndianko.ceeli.utils.param_types import SubPathArg, SubPath

PARAM_REGEX = re.compile("{([a-zA-Z_][a-zA-Z0-9_]*)(:[a-zA-Z_][a-zA-Z0-9_]*)?}")


def compile_path(path: str) -> SubPath:

    args: List[SubPathArg] = []
    final_format = ""
    param_names = set()
    duplicates = set()
    idx = 0
    for match in PARAM_REGEX.finditer(path):
        param_name, default_value = match.groups()
        if default_value:
            default_value = default_value.lstrip(":")
        args.append(SubPathArg(name=param_name, default_value=default_value, mandatory=True))
        final_format += path[idx: match.start()]
        final_format += "{%s}" % param_name
        idx = match.end()

        if param_name in param_names:
            duplicates.add(param_name)
        else:
            param_names.add(param_name)

    if len(duplicates) > 0:
        raise ValueError(f"Found duplicate parameter names: {', '.join(duplicates)}")

    final_format += path[idx:]
    return SubPath(format=final_format, args=args)


def test():
    test_cases = [
        "/groups/{group}/{sub_group:main}"
    ]

    for case in test_cases:
        res = compile_path(case)
        print(f"{case}   ==> {res}")


if __name__ == "__main__":
    test()
