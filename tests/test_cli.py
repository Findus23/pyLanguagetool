import pylanguagetool


def test_cli(capsys):
    match = {'rule': {'issueType': 'misspelling', 'category': {'name': 'Miscellaneous', 'id': 'MISC'},
                      'description': "Use of 'a' vs. 'an'", 'id': 'EN_A_VS_AN'},
             'message': 'Use "a" instead of \'an\' if the following word doesn\'t start with a vowel sound, e.g. \'a sentence\', \'a university\'',
             'offset': 8, 'replacements': [{'value': 'a'}], 'shortMessage': 'Wrong article',
             'context': {'text': 'This is an test', 'offset': 8, 'length': 2}, 'length': 2}
    should_output = """Use "a" instead of 'an' if the following word doesn't start with a vowel sound, e.g. 'a sentence', 'a university'
  ✗ This is an test
            ^^
  ✓ This is a test

"""
    pylanguagetool.print_errors([match], False)
    out, err = capsys.readouterr()
    assert out == should_output
