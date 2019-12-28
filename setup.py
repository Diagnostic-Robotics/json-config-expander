import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
	name="json-config-expander",
	version="0.1",
	author="Diagnostic Robotics",
	author_email="admin@diagnosticrobotics.com",
	description="Expand multi optional configuration to multiple configurations.",
	license="MIT",
	keywords="multiple json config",
	url="https://github.com/DiagnosticRobotics/json-config-expander",
	packages=find_packages(include=['json_config_expander', 'json_config_expander.*']),
	long_description=read('README.md'),
	classifiers=[
		"Development Status :: 1 - Alpha",
	],
)
