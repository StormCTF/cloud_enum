import setuptools
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

setup(
	name='cloud_enum',
	version='1.0',
	description='Cloud Enum Project',
	long_description=long_description,
	url='https://github.com/StormCTF/cloud_enum',
	packages=setuptools.find_packages(),
	python_requires='>=3.4'
)