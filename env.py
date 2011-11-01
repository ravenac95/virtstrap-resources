"""
env.py allows you to set custom environment variables
"""
from optparse import OptionParser
import imp
import sys

SET_VARIABLE_TEMPLATE = """
{name}="{value}";
export {name};
"""

UNSET_VARIABLE_TEMPLATE = "    unset {name};"

DEACTIVATE_CUSTOM_ENV_TEMPLATE = """
deactivate_custom_env () {{
{unset_area}
}}
"""
parser = OptionParser()
cli_options, cli_args = parser.parse_args()

def build_custom_env(custom_env_path):
    try:
        custom_env = imp.load_source("virtstrap_userdef_customenv",
                custom_env_path)
    except ImportError:
        sys.stderr.write('Custom environment script at "{0}"\n'.format(
            custom_env_path))
        sys.exit(1)
    build_env_dict = getattr(custom_env, "build_env_dict", None)
    if not build_env_dict:
        sys.stderr.write('Custom environment script requires one method '
                '"build_env_dict" that returns a dictionary of environment '
                'values.')
        sys.exit(1)
    return custom_env.build_env_dict()

def process_env_dict(env_dict):
    set_strs = []
    unset_strs = []
    for name, value in env_dict.iteritems():
        variable_context = dict(name=name, value=value)
        set_str = SET_VARIABLE_TEMPLATE.format(**variable_context)
        unset_str = UNSET_VARIABLE_TEMPLATE.format(**variable_context)
        set_strs.append(set_str)
        unset_strs.append(unset_str)
    return set_strs, unset_strs

def main():
    try:
        custom_env_path = cli_args[0]
    except:
        sys.stderr.write("Must define a custom environment script\n")
        sys.exit(1)
    env_dict = build_custom_env(custom_env_path)
    set_strs, unset_strs = process_env_dict(env_dict)
    sys.stdout.write("\n".join(set_strs))
    unset_area = "\n".join(unset_strs)
    deactivate_function = (DEACTIVATE_CUSTOM_ENV_TEMPLATE
            .format(unset_area=unset_area))
    sys.stdout.write(deactivate_function)

if __name__ == "__main__":
    main()
