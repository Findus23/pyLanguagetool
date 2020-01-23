import os

from pylanguagetool import api

API_BASE_URL = os.environ["API_URL"]


def test_languages_request():
    langs = api.get_languages(API_BASE_URL)
    assert isinstance(langs, list)
    assert len(langs) > 2
    found_german = False
    for i, dic in enumerate(langs):
        if dic["code"] == "de":
            found_german = True
    assert found_german


def test_request():
    response = api.check("This is an test", API_BASE_URL, "auto")
    assert "software" in response
    match = response["matches"][0]
    assert isinstance(match, dict)
