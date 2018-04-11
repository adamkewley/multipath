from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='multipath',
    version=__version__,
    license='Apache License 2.0',

    description='A miniscule python package for joining and resolving paths against multiple possible directories.A python package for resolving relative paths against multiple root directories',
    long_description=long_description,
    keywords='',

    author='Adam Kewley',
    author_email='contact@adamkewley.com',

    url='https://github.com/adamkewley/multipath',
    download_url='https://github.com/adamkewley/multipath/tarball/' + __version__,

    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],

    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
)
