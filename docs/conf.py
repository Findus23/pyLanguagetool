"""Sphinx configuration file."""

from pkg_resources import get_distribution

project = "pyLanguagetool"
copyright = "2017, Lukas Winkler"
release = get_distribution('pylanguagetool').version
version = '.'.join(release.split('.')[:2])

master_doc = 'index'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
