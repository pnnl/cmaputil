from setuptools import setup, find_packages

import cmaputil


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

pkgs = find_packages(exclude=('examples'))

setup(
    name='cmaputil',
    version=cmaputil.__version__,
    description='Colormap analysis module.',
    long_description=readme,
    author=cmaputil.__author__,
    author_email='jamie.nunez@pnnl.gov',
    url='https://github.com/smcolby/cmaputil',
    license=license,
    packages=pkgs,
    install_requires=required
)
