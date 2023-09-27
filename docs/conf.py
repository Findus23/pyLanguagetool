"""Sphinx configuration file."""
import sys

from pkg_resources import get_distribution

project = "pyLanguagetool"
copyright = "2023, Lukas Winkler"
release = get_distribution('pylanguagetool').version
version = '.'.join(release.split('.')[:2])

master_doc = 'index'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
    'sphinx.ext.linkcode'
]

html_theme = 'alabaster'
html_theme_options = {
    'description': 'A python library and CLI for the LanguageTool JSON API.',
}

templates_path = ['_templates']

latex_engine = 'xelatex'
latex_elements = {
    'papersize': 'a4paper',
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    "requests": ("https://docs.python-requests.org/en/latest/", None),
}


def linkcode_resolve(domain, info):
    def find_source():
        # try to find the file and line number, based on code from numpy:
        # https://github.com/numpy/numpy/blob/master/doc/source/conf.py#L286
        obj = sys.modules[info['module']]
        for part in info['fullname'].split('.'):
            obj = getattr(obj, part)
        import inspect
        mod = info['module'].replace('.', '/')
        if mod == "pylanguagetool":
            mod += "/__init__"
        fn = mod + ".py"
        source, lineno = inspect.getsourcelines(obj)
        return fn, lineno, lineno + len(source) - 1

    if domain != 'py' or not info['module']:
        return None
    try:
        filename = '{}#L{:d}-L{:d}'.format(*find_source())
    except Exception:
        filename = info['module'].replace('.', '/') + '.py'
    return "https://github.com/Findus23/pyLanguagetool/blob/master/{}".format(filename)
