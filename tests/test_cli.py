import pylanguagetool


def test_cli(capsys):
    response = {
        "software": {
            "name": "LanguageTool",
            "version": "4.6",
            "buildDate": "2019-06-26 07:28",
            "apiVersion": 1,
            "premium": False,
            "premiumHint": "You might be missing errors only the Premium version can find. Contact us at support<at>languagetoolplus.com.",
            "status": "",
        },
        "warnings": {"incompleteResults": False},
        "language": {
            "name": "German (Austria)",
            "code": "de-AT",
            "detectedLanguage": {
                "name": "German (Austria)",
                "code": "de-AT",
                "confidence": 0.99999136,
            },
        },
        "matches": [
            {
                "message": "Dieser Satz fängt nicht mit einem großgeschriebenen Wort an",
                "shortMessage": "",
                "replacements": [{"value": "Das"}],
                "offset": 0,
                "length": 3,
                "context": {"text": "das ist ein est", "offset": 0, "length": 3},
                "sentence": "das ist ein est",
                "type": {"typeName": "Other"},
                "rule": {
                    "id": "UPPERCASE_SENTENCE_START",
                    "description": "Großschreibung am Satzanfang",
                    "issueType": "typographical",
                    "category": {"id": "CASING", "name": "Groß-/Kleinschreibung"},
                },
                "ignoreForIncompleteSentence": True,
                "contextForSureMatch": -1,
            },
            {
                "message": "Möglicher Rechtschreibfehler gefunden",
                "shortMessage": "Rechtschreibfehler",
                "replacements": [
                    {"value": "ist"},
                    {"value": "es"},
                    {"value": "erst"},
                    {"value": "fest"},
                    {"value": "West"},
                    {"value": "Ost"},
                    {"value": "Rest"},
                    {"value": "Nest"},
                    {"value": "Pest"},
                    {"value": "lest"},
                    {"value": "Ast"},
                    {"value": "Fest"},
                    {"value": "Gst"},
                    {"value": "Test"},
                    {"value": "best"},
                    {"value": "esst"},
                    {"value": "et"},
                    {"value": "äst"},
                    {"value": "des"},
                    {"value": "mit"},
                ],
                "offset": 12,
                "length": 3,
                "context": {"text": "das ist ein est", "offset": 12, "length": 3},
                "sentence": "das ist ein est",
                "type": {"typeName": "UnknownWord"},
                "rule": {
                    "id": "AUSTRIAN_GERMAN_SPELLER_RULE",
                    "description": "Möglicher Rechtschreibfehler",
                    "issueType": "misspelling",
                    "category": {"id": "TYPOS", "name": "Mögliche Tippfehler"},
                },
                "ignoreForIncompleteSentence": False,
                "contextForSureMatch": 0,
            },
        ],
    }

    should_output = """German (Austria) detected (100% confidence)

Dieser Satz fängt nicht mit einem großgeschriebenen Wort an
  ✗ das ist ein est
    ^^^
  ✓ Das ist ein est

Möglicher Rechtschreibfehler gefunden
  ✗ das ist ein est
                ^^^
  ✓ das ist ein ist
  ✓ das ist ein es
  ✓ das ist ein erst
  ✓ das ist ein fest
  ✓ das ist ein West

Text checked by https://example.com/v2/ (LanguageTool 4.6)
"""
    pylanguagetool.print_errors(response, "https://example.com/v2/", False)
    out, err = capsys.readouterr()
    assert out == should_output
