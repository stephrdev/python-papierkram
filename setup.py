import os
from codecs import open

from setuptools import setup, find_packages


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION = __import__('papierkram').__version__


with open(os.path.join(BASE_DIR, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='python-papierkram',
    version=VERSION,
    description='A thin API wrapper around Papierkram.de until a real API exists.',
    long_description=long_description,
    url='https://github.com/stephrdev/python-papierkram',
    project_urls={
        'Bug Reports': 'https://github.com/stephrdev/python-papierkram/issues',
        'Source': 'https://github.com/stephrdev/python-papierkram',
    },
    author='Stephan Jaekel',
    author_email='steph@rdev.info',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[],
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
