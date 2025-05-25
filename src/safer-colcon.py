#!/usr/bin/python3
# EASY-INSTALL-ENTRY-SCRIPT: 'colcon-core==0.19.0','console_scripts','colcon'
import re
import sys
import os

# for compatibility with easy_install; see #2198
__requires__ = 'colcon-core==0.19.0'

source = os.path.exists(os.path.join(os.getcwd(), 'src'))

if source is False:
	if (paths_str := os.getenv('ROSWS')) is not None:
		paths_list = paths_str.split(":")
		index = 0 
		os.chdir(paths_list[index])
		
		# TODO(Add weighted based builds or figure out how to pass CLI after build)
	else:
		print("Are you sure you have any workspaces?")
		sys.exit()
	
try:
    from importlib.metadata import distribution
except ImportError:
    try:
        from importlib_metadata import distribution
    except ImportError:
        from pkg_resources import load_entry_point


def importlib_load_entry_point(spec, group, name):
    dist_name, _, _ = spec.partition('==')
    matches = (
        entry_point
        for entry_point in distribution(dist_name).entry_points
        if entry_point.group == group and entry_point.name == name
    )
    return next(matches).load()


globals().setdefault('load_entry_point', importlib_load_entry_point)


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(load_entry_point('colcon-core==0.19.0', 'console_scripts', 'colcon')())