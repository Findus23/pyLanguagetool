# -*- coding: utf-8 -*-
from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyLanguagetool',
    version='0.7.0',
    packages=find_packages(),
    url='https://github.com/Findus23/pylanguagetool',
    license='MIT',
    author='Lukas Winkler',
    author_email='python@lw1.at',
    description='A python library and CLI for the LanguageTool JSON API',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Text Processing :: Linguistic'
    ],
    install_requires=['colorama>=0.4.1', 'configargparse>=0.14.0', 'requests>=2.22.0'],
    extras_require={
        'dev': ["pytest", "docutils", "pygments"],
        'optional': ["beautifulsoup4", "markdown2", "docutils"],
    },
    keywords="languagetool spell grammar checker",
    entry_points={
        'console_scripts': [
            'pylanguagetool=pylanguagetool:main',
        ],
    },

)
