import requests


def get_languages(api_url):
    r = requests.get(api_url + "languages")
    return r.json()


def check(input_text,api_url, lang, mother_tongue=None, preferred_variants=None,
          enabled_rules=None, disabled_rules=None,
          enabled_categories=None, disabled_categories=None,
          enabled_only=False,
          **kwargs):
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
        post_parameters["enabledCategories"] = disabled_categories
    if enabled_only:
        post_parameters["enabledOnly"] = True
    r = requests.post(api_url + "check", data=post_parameters)
    if r.status_code != 200:
        raise ValueError(r.text)
    return r.json()
