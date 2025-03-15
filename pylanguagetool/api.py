r"""
Python API wrapper for the languagetool REST API.

Simple usage::

    >>> from pylanguagetool import api
    >>> api.check(
    ...     'This is a example',
    ...     api_url='https://languagetool.org/api/v2/',
    ...     lang='en-US',
    ... )
"""
from typing import Optional

import requests


def get_languages(api_url: str) -> list[dict[str, str]]:
    """
    Return supported languages as a list of dictionaries.

    Args:
        api_url (str): API base url.

    Returns:
        list[dict]:
            Supported languages as a list of dictionaries.

            Each dictionary contains three keys, ``name``, ``code`` and
            ``longCode``::

                {
                    "name":"English (GB)",
                    "code":"en",
                    "longCode":"en-GB"
                }

    """
    r = requests.get(api_url + "languages")
    return r.json()


def _is_in_pwl(match, pwl):
    start = match['context']['offset']
    end = start + match['context']['length']
    word = match['context']['text'][start:end]
    return word in pwl


def check(
        input_text: str, api_url: str,
        lang: str, pwl: list[str],
        mother_tongue: Optional[str] = None,
        preferred_variants: Optional[str] = None,
        enabled_rules: Optional[str] = None, disabled_rules: Optional[str] = None,
        enabled_categories: Optional[str] = None, disabled_categories: Optional[str] = None,
        enabled_only: bool = False, picky: bool = False, verbose: bool = False,
        username: Optional[str] = None, api_key: Optional[str] = None):
    """
    Check given text and return API response as a dictionary.

    Args:
        input_text (str):
            Plain text that will be checked for spelling mistakes.

        api_url (str):
            API base url, e.g. ``https://languagetool.org/api/v2/``

        lang: Language of the given text as `RFC 3066`__ language code.
            For example ``en-GB`` or ``de-AT``. ``auto`` is a valid value too
            and will cause the language to be detected automatically.

            __ https://www.ietf.org/rfc/rfc3066.txt

        mother_tongue: Native language of the author as `RFC 3066`__ language
            code.

            __ https://www.ietf.org/rfc/rfc3066.txt

        preferred_variants (str):
            Comma-separated list of preferred language variants. The language
            detector used with ``language=auto`` can detect e.g. English, but
            it cannot decide whether British English or American English is
            used. Therefore, this parameter can be used to specify the
            preferred variants like ``en-GB`` and ``de-AT``. Only available
            with ``language=auto``.

        enabled_rules (str):
            Comma-separated list of IDs of rules to be enabled

        disabled_rules (str):
            Comma-separated list of IDs of rules to be disabled.

        enabled_categories (str):
            Comma-separated list of IDs of categories to be enabled.

        disabled_categories (str):
            Comma-separated list of IDs of categories to be disabled.

        enabled_only (bool):
            If ``True``, only the rules and categories whose IDs are specified
            with ``enabledRules`` or ``enabledCategories`` are enabled.
            Defaults to ``False``.

        picky (bool):
            If enabled, addition rules are activated.

        verbose (bool):
            If ``True``, a more verbose output will be printed. Defaults to
            ``False``.

        pwl (list[str]):
            Personal world list. A custom dictionary of words that should be
            excluded from spell checking errors.

        username (str):
            For Premium API

        api_key (str):
            For Premium API

    Returns:
        dict:
            A dictionary representation of the JSON API response.
            The most notable key is ``matches``, which contains a list of all
            spelling mistakes that have been found.

            E.g.::

                {
                    "language": {
                        "name": "English (GB)",
                        "code": "en-GB",
                        "detectedLanguage": {
                            "name": "English (GB)",
                            "code": "en-GB",
                            "confidence": 0.561,
                            "source": "fasttext",
                        },
                    },
                    "sentenceRanges": [[0, 17]],
                    "extendedSentenceRanges": [
                        {"from": 0, "to": 17, "detectedLanguages": [{"language": "en", "rate": 1.0}]}
                    ],
                    "matches": [
                        {
                            "context": {"text": "This is a example", "offset": 8, "length": 1},
                            "contextForSureMatch": 1,
                            "ignoreForIncompleteSentence": False,
                            "length": 1,
                            "message": "Use “an” instead of ‘a’ if the following word starts with a vowel sound, e.g.\xa0‘an article’, ‘an hour’.",
                            "offset": 8,
                            "replacements": [{"value": "an"}],
                            "rule": {
                                "category": {"id": "MISC", "name": "Miscellaneous"},
                                "description": "Use of 'a' vs. 'an'",
                                "id": "EN_A_VS_AN",
                                "issueType": "misspelling",
                                "urls": [
                                    {
                                        "value": "https://languagetool.org/insights/post/indefinite-articles/"
                                    }
                                ],
                            },
                            "sentence": "This is a example",
                            "shortMessage": "Wrong article",
                            "type": {"typeName": "Other"},
                        }
                    ],
                    "software": {
                        "apiVersion": 1,
                        "buildDate": "2024-09-27 11:27:57 +0200",
                        "version": "6.5",  
                        "name": "LanguageTool",
                        "premium": False,
                        "premiumHint": "You might be missing errors only the Premium version can find. Contact us at support<at>languagetoolplus.com.",
                        "status": "",
                    },
                    "warnings": {"incompleteResults": False},
                }


    """
    post_parameters = {
        "text": input_text,
        "language": lang,
    }
    if mother_tongue:
        post_parameters["motherTongue"] = mother_tongue
    if preferred_variants:
        post_parameters["preferredVariants"] = preferred_variants
    if enabled_rules:
        post_parameters["enabledRules"] = enabled_rules
    if disabled_rules:
        post_parameters["disabledRules"] = disabled_rules
    if enabled_categories:
        post_parameters["enabledCategories"] = enabled_categories
    if disabled_categories:
        post_parameters["disabledCategories"] = disabled_categories
    if enabled_only:
        post_parameters["enabledOnly"] = 'true'
    if picky:
        post_parameters["level"] = 'picky'
    if username or api_key:
        if not username or not api_key:
            raise ValueError("When specifying username or apikey, you must specify both")
        if api_url != "https://languagetool.org/api/v2/":
            raise ValueError("Premium API only works when using languagetool.org")
        post_parameters["username"] = username
        post_parameters["apiKey"] = api_key

    r = requests.post(api_url + "check", data=post_parameters)
    if r.status_code != 200:
        raise ValueError(r.text)
    if verbose:
        print(post_parameters)
        print(r.json())
    data = r.json()
    if pwl:
        matches = data.pop('matches', [])
        data['matches'] = [
            match for match in matches
            if not _is_in_pwl(match, pwl)
        ]
    return data
