from __future__ import print_function
from setuptools import setuptools, find_packages

import rcon

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='starbound-rcon',
    version='0.0.1',
    description='An RCON client that is compatible with Starbound servers',
    long_description=readme,
    author='Justin Gorinsky',
    author_email='gorinsky@gmail.com',
    url='https://github.com/jgorinsky/starbound-rcon',
    license=license,
    packages=find_packages(exclude=('tests','docs'))
)