"""
Support spellchecking various file formats by converting them to plain text

"""
import json
import sys
import xml.etree.ElementTree
from typing import Optional

supported_extensions = ["txt", "html", "md", "markdown", "rst", "ipynb", "json", "xliff"]


def convert(source: str, texttype: Optional[str]) -> str:
    """
    Convert files of various types to plaintext

    Args:
        texttype (str):
            file extension of the input file
        source (str):
            content of the input file

    Returns:
        str:
            plaintext output
    """
    if texttype == "html":
        return html2text(source)
    if texttype in ["md", "markdown"]:
        return html2text(markdown2html(source))
    if texttype in ["rst"]:
        return html2text(rst2html(source))
    if texttype == "ipynb":
        return html2text(markdown2html(ipynb2markdown(source)))
    if texttype == "json":
        return transifexjson2txt(source)
    if texttype == "xliff":
        return xliff2txt(source)
    if texttype != "txt":
        print("filetype not detected, assuming plaintext")
    return source


def html2text(html: str) -> str:
    """
    convert HTML to plaintext by parsing it with BeautifulSoup and removing code

    Args:
        html (str):
            HTML string

    Returns:
        str: plaintext
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        notinstalled("beautifulsoup4", "HTML", "text")
        sys.exit(4)
    soup = BeautifulSoup(html, "html.parser")
    # remove scripts from html
    for script in soup(["script", "style", "code", "pre"]) + soup("span", {"class": "literal"}):
        script.extract()
    return soup.get_text()


def markdown2html(markdown: str) -> str:
    """
    convert Markdown to HTML via ``markdown2``

    Args:
        markdown (str):
            Markdown text

    Returns:
        str: HTML
    """
    try:
        import markdown2
    except ImportError:
        notinstalled("markdown2", "markdown", "HTML")
        sys.exit(4)

    return markdown2.markdown(markdown)


def ipynb2markdown(ipynb: str) -> str:
    """
    Extract Markdown cells from iPython Notebook

    Args:
        ipynb (str):
            iPython notebook JSON file

    Returns:
        str: Markdown
    """
    j = json.loads(ipynb)
    markdown = ""
    for cell in j["cells"]:
        if cell["cell_type"] == "markdown":
            markdown += "".join(cell["source"]) + "\n"
    return markdown


def rst2html(rst: str) -> str:
    """
    convert reStructuredText to HTML with ``docutils``

    Args:
        rst (str):
             reStructuredText

    Returns:
        str: HTML
    """
    try:
        from docutils.core import publish_string
    except ImportError:
        notinstalled("docutils", "ReStructuredText", "HTML")
        sys.exit(4)
    return publish_string(rst, writer_name="html5")


def transifexjson2txt(jsondata: str) -> str:
    """
    extract translations from Transifex JSON file

    Args:
        jsondata (str):
            Transifex export file

    Returns:
        str: Plaintext translations

    """
    data = json.loads(jsondata)
    text = ""
    for _category, content in data.items():
        for _key, value in content.items():
            text += value + "\n"
    return text


def xliff2txt(source: str) -> str:
    """
    extract translations from ``XLIFF`` file

    Args:
        source (str):
            XLIFF XML string

    Returns:
        str: Plaintext translations

    """
    root = xml.etree.ElementTree.fromstring(source)
    text = ""
    for file in root:
        for body in file:
            for trans_unit in body:
                value = trans_unit.find("{urn:oasis:names:tc:xliff:document:1.1}target").text
                if value:
                    text += value + "\n\n"
    return text


def notinstalled(package: str, convert_from: str, convert_to: str) -> None:
    print(
        f"""{package} is needed to convert {convert_from} to {convert_to}
you can install it with pip:
pip install {package}"""
    )
