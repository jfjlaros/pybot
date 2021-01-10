import sys
from setuptools import setup

if sys.version_info < (2, 6):
    raise Exception('pybot requires Python 2.6 or higher.')

# Todo: How does this play with pip freeze requirement files?
requires = []

# Python 2.6 does not include the argparse module.
try:
    import argparse
except ImportError:
    requires.append('argparse')

import pybot as distmeta

setup(
    name='pybot',
    version=distmeta.__version__,
    description='FASTA/FASTQ analysis and manipulation toolkit.',
    long_description=distmeta.__doc__,
    author=distmeta.__author__,
    author_email=distmeta.__contact__,
    url=distmeta.__homepage__,
    license='MIT License',
    platforms=['any'],
    packages=['pybot', 'pyPgSQL'],
    install_requires=requires,
    entry_points = {
        'console_scripts': [
            'pybot = pybot.pybot:main'
        ]
    },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    keywords=['bot', 'irc']
)
