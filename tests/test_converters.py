from pylanguagetool import converters

markdown = """# Heading
This is *a* Sentence.
"""
html = """<h1>Heading</h1>

<p>This is <em>a</em> Sentence.</p>
"""
plaintext = """Heading
This is a Sentence.
"""

ipython = """{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "# Heading\\n",
        "some *text*"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Other Heading\\n",
        "- text\\n",
        "- more text"
      ]
    }
  ],
  "metadata": {},
  "nbformat": 4,
  "nbformat_minor": 0
}"""

ipython_markdown = """# Heading
some *text*
## Other Heading
- text
- more text
"""

ipython_html = """<h1>Heading</h1>

<p>some <em>text</em></p>

<h2>Other Heading</h2>

<ul>
<li>text</li>
<li>more text</li>
</ul>
"""

ipython_plaintext = """Heading
some text
Other Heading

text
more text

"""


def test_html2text():
    assert converters.html2text(html) == plaintext


def test_markdown2html():
    assert converters.markdown2html(markdown) == html


def test_ipynb2markdown():
    assert converters.ipynb2markdown(ipython) == ipython_markdown


def test_ipython_markdown2html():
    assert converters.markdown2html(ipython_markdown) == ipython_html


def test_ipython_html2text():
    assert converters.html2text(ipython_html) == ipython_plaintext
