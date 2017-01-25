# -*- coding: utf-8 -*-
import pylanguagetool


def test_cli(capsys):
    response = {
        'software': {
            'buildDate': '2016-12-28 15:25',
            'apiVersion': '1',
            'version': '3.6',
            'status': '',
            'name': 'LanguageTool'
        },
        'matches': [
            {
                'length': 3,
                'shortMessage': '',
                'context': {
                    'length': 3,
                    'text': 'das ist ein est ',
                    'offset': 0
                },
                'replacements':
                    [{'value': 'Das'}],
                'rule': {
                    'category': {
                        'name': 'Groß-/Kleinschreibung',
                        'id': 'CASING'
                    },
                    'issueType': 'typographical',
                    'description': 'Großschreibung am Satzanfang',
                    'id': 'UPPERCASE_SENTENCE_START'
                },
                'message': 'Dieser Satz fängt nicht mit einem großgeschriebenen Wort an',
                'offset': 0
            },
            {'length': 3,
             'shortMessage': 'Rechtschreibfehler',
             'context':
                 {'length': 3,
                  'text': 'das ist ein est ',
                  'offset': 12
                  },
             'replacements':
                 [
                     {'value': 'esst'}, {'value': 'ist'}, {'value': 'es'}, {'value': 'erst'}, {'value': 'fest'},
                     {'value': 'Rest'}, {'value': 'Test'}, {'value': 'Fest'}, {'value': 'West'}, {'value': 'Nest'},
                     {'value': 'Ost'}, {'value': 'Ast'}, {'value': 'Gst'}, {'value': 'Pest'}, {'value': 'et'},
                     {'value': 'lest'}, {'value': 'äst'}, {'value': 'des'}, {'value': 'mit'}, {'value': 'ein'}
                 ],
             'rule': {
                 'category': {
                     'name': 'Mögliche Tippfehler',
                     'id': 'TYPOS'
                 },
                 'issueType': 'misspelling',
                 'description': 'Möglicher Rechtschreibfehler',
                 'id': 'GERMAN_SPELLER_RULE'
             },
             'message': 'Möglicher Rechtschreibfehler gefunden',
             'offset': 12
             }
        ],
        'language': {
            'code': 'de-AT',
            'name': 'German (Austria)'
        }
    }

    should_output = u"""Dieser Satz fängt nicht mit einem großgeschriebenen Wort an
  ✗ das ist ein est\u0020
    ^^^
  ✓ Das ist ein est\u0020

Möglicher Rechtschreibfehler gefunden
  ✗ das ist ein est\u0020
                ^^^
  ✓ das ist ein esst\u0020
  ✓ das ist ein ist\u0020
  ✓ das ist ein es\u0020
  ✓ das ist ein erst\u0020
  ✓ das ist ein fest\u0020

Text checked by https://example.com/v2/
"""
    pylanguagetool.print_errors(response["matches"], "https://example.com/v2/", False)
    out, err = capsys.readouterr()
    assert out == should_output
