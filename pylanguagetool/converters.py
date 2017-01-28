import json
import sys


def convert(source, texttype):
    if texttype == "html":
        return html2text(source)
    if texttype in ["md", "markdown"]:
        return html2text(markdown2html(source))
    if texttype in ["rst"]:
        return html2text(rst2html(source))
    if texttype == "ipynb":
        return html2text(markdown2html(ipynb2markdown(source)))
    if texttype != "txt":
        print("filetype not detected, assuming plaintext")
    return source


def html2text(html):
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        notinstalled("beautifulsoup", "HTML", "text")
        sys.exit(4)
    soup = BeautifulSoup(html, "html.parser")
    # remove scripts from html
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text()


def markdown2html(markdown):
    try:
        import markdown2
    except ImportError:
        notinstalled("markdown2", "markdown", "HTML")
        sys.exit(4)

    return markdown2.markdown(markdown)


def ipynb2markdown(ipynb):
    j = json.loads(ipynb)
    markdown = ""
    for cell in j["cells"]:
        markdown += "".join(cell["source"]) + "\n"
    return markdown


def rst2html(rst):
    try:
        from docutils.core import publish_string
    except ImportError:
        notinstalled("markdown2", "markdown", "HTML")
        sys.exit(4)
    return publish_string(rst, writer_name="html5")


def notinstalled(package, convert_from, convert_to):
    print(
        """{package} is needed to convert {source} to {target}
you can install it with pip:
pip install {package}""".format(package=package, source=convert_from, target=convert_to)
    )
