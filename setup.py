import io
from os.path import dirname, join
from setuptools import setup, find_packages


def get_version(relpath):
  """Read version info from a file without importing it"""
  for line in io.open(join(dirname(__file__), relpath), encoding="cp437"):
    if "__version__" in line:
      if '"' in line:
        # __version__ = "0.9"
        return line.split('"')[1]
      elif "'" in line:
        return line.split("'")[1]


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

pkgs = find_packages(exclude=('examples'))

setup(
    name='cmaputil',
    version=get_version("cmaputil/__init__.py"),
    description='Colormap analysis module.',
    long_description=readme,
    author='Jamie R. Nunez',
    author_email='jamie.nunez@pnnl.gov',
    url='https://github.com/pnnl/cmaputil',
    license=license,
    packages=pkgs,
    install_requires=required
)
