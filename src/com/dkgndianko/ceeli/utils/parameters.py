import re
from typing import List

from com.dkgndianko.ceeli.utils.param_types import TemplateArg, Template

PARAM_REGEX = re.compile("{([a-zA-Z_][a-zA-Z0-9_]*)(:[a-zA-Z_][a-zA-Z0-9_]*)?}")


def compile_template(template: str) -> Template:

    args: List[TemplateArg] = []
    final_format = ""
    param_names = set()
    duplicates = set()
    idx = 0
    for match in PARAM_REGEX.finditer(template):
        param_name, default_value = match.groups()
        if default_value:
            default_value = default_value.lstrip(":")
        args.append(TemplateArg(name=param_name, default_value=default_value, mandatory=True))
        final_format += template[idx: match.start()]
        final_format += "{%s}" % param_name
        idx = match.end()

        if param_name in param_names:
            duplicates.add(param_name)
        else:
            param_names.add(param_name)

    if len(duplicates) > 0:
        raise ValueError(f"Found duplicate parameter names: {', '.join(duplicates)}")

    final_format += template[idx:]
    return Template(format=final_format, args=args)


def format_template(template: Template, **kwargs) -> str:
    """
    Format a template by filling in the parameters. It uses either the given parameter or the default values if \
    available. It can raise an exception if a mandatory parameter or not given and doesn't have a default value
    :param template: the sub path definition with the template and the list of parameters to provide
    :param kwargs: the parameters as key-word arguments
    :return: str, the formatted value
    :except: ValueError
    """
    arg_val = {}
    for arg_def in template.args:
        val = kwargs.get(arg_def.name) or arg_def.default_value
        if val is None and arg_def.mandatory:
            raise ValueError(f"Argument {arg_def.name} is mandatory and not given")
        arg_val[arg_def.name] = val
    return template.format.format(**arg_val)


def test():
    test_cases = [
        "/groups/{group}/{sub_group:main}"
    ]

    for case in test_cases:
        res = compile_template(case)
        print(f"{case}   ==> {res}")


if __name__ == "__main__":
    test()
