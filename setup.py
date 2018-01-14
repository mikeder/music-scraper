import re
from setuptools import setup, find_packages
from os import path

VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+((dev|rc|b)[0-9]+)?)['"]''')
here = path.abspath(path.dirname(__file__))


def get_version():
    init = open(path.join(here, 'rsdc', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)

setup(
    name='rsdc',
    version=get_version(),
    packages=find_packages(),
    url='https://github.com/mikeder/music-scraper',
    license='MIT',
    author='mike.eder',
    author_email='mikedernet@gmail.com',
    description='Reddit Music Scraper',
    install_requires=[
        'configparser==3.5.0',
        'pafy==0.5.3.1',
        'pydub==0.20.0',
        'requests==2.18.4',
        'youtube-dl==2017.12.31'
    ],
    entry_points={
        'console_scripts': [
            'rsdc=rsdc.rsdc:main'
        ]
    }
)
