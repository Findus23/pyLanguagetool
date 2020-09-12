"""
A python library and CLI tool for the LanguageTool JSON API.
"""
import os
import sys
from pprint import pprint

import configargparse
import pkg_resources
from colorama import Fore, init as init_colors

from . import CustomConfigFileParser
from . import api
from . import converters

indention = " " * 4


def init_config():
    p = configargparse.ArgParser(default_config_files=["~/.config/pyLanguagetool.conf"],
                                 config_file_parser_class=CustomConfigFileParser.CustomConfigFileParser)
    p.add_argument("-V", "--version", default=False, action='store_true')
    p.add_argument("-v", "--verbose", env_var="VERBOSE", default=False, action='store_true')
    p.add_argument("-a", "--api-url", env_var="API_URL", default="https://languagetool.org/api/v2/",
                   help="the URL of the v2 languagetool API, should end with '/v2/'")
    p.add_argument("--no-color", env_var="NO_COLOR", action='store_true', default=False, help="don't color output")
    p.add_argument("-c", "--clipboard", env_var="CLIPBOARD", action='store_true', default=False,
                   help="get text from system clipboard")
    p.add_argument("-s", "--single-line", env_var="SINGLE_LINE", action='store_true', default=False,
                   help="check every line on its own")
    p.add_argument("-t", "--input-type", env_var="INPUT_TYPE",
                   choices=converters.supported_extensions,
                   help="if not plaintext")
    p.add_argument("-u", "--explain-rule", env_var="EXPLAIN_RULE", action="store_true", default=False,
                   help="print URLs with more information about rules")
    p.add_argument('input file', help='input file', nargs='?')
    p.add_argument("-r", "--rules", env_var="RULES", action='store_true', default=False,
                   help="show the matching rules")
    p.add_argument("--rule-categories", env_var="RULE_CATEGORIES", action='store_true', default=False,
                   help="show the the categories of the matching rules")
    p.add_argument('-l', '--lang', env_var='TEXTLANG', default="auto",
                   help="A language code like en or en-US, or auto to guess the language automatically (see preferredVariants below). For languages with variants (English, German, Portuguese) spell checking will only be activated when you specify the variant, e.g. en-GB instead of just en."
                   )
    p.add_argument("-m", "--mother-tongue", env_var="MOTHER__TONGUE",
                   help="A language code of the user's native language, enabling false friends checks for some language pairs."
                   )
    p.add_argument("-p", "--preferred-variants", env_var="PREFERRED_VARIANTS",
                   help="Comma-separated list of preferred language variants. The language detector used with language=auto can detect e.g. English, but it cannot decide whether British English or American English is used. Thus this parameter can be used to specify the preferred variants like en-GB and de-AT. Only available with language=auto."
                   )
    p.add_argument('-e', '--enabled-rules', env_var='ENABLED_RULES', help='IDs of rules to be enabled, comma-separated')
    p.add_argument('-d', '--disabled-rules', env_var='DISABLED_RULES',
                   help='IDs of rules to be disabled, comma-separated')
    p.add_argument('--enabled-categories', env_var='ENABLED_CATEGORIES',
                   help='IDs of categories to be enabled, comma-separated')
    p.add_argument('--disabled-categories', env_var='DISABLED_CATEGORIES',
                   help='IDs of categories to be disabled, comma-separated')
    p.add_argument("--enabled-only", action='store_true', default=False,
                   help="enable only the rules and categories whose IDs are specified with --enabled-rules or --enabled-categories"
                   )
    p.add_argument(
        '--pwl', '--personal-word-list',
        env_var='PERSONAL_WORD_LIST', help=(
            'File name of personal dictionary. A private dictionary'
            ' can be used to add special words that would otherwise'
            ' be marked as spelling errors.'
        ))

    c = vars(p.parse_args())
    if c["version"]:
        print(pkg_resources.get_distribution('pylanguagetool').version)
        exit()
    if c["enabled_only"] and (c["disabled_categories"] or c["disabled_rules"]):
        print("disabled not allowed")  # TODO: ?
    if c["preferred_variants"] and c["lang"] != "auto":
        # print("You specified --preferred_variants but you didn't specify --language=auto")
        # sys.exit(2)
        print('ignoring --preferred-variants as --lang is not set to "auto"')
        c["preferred_variants"] = None
    if c["verbose"]:
        pprint(c)
    return c, p


def get_clipboard():
    """
    Return text stored in the operating system's clipboard.

    Returns:
        str: Text stored in the operating system's clipboard.

    """
    # See also: http://stackoverflow.com/a/16189232
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()  # keep the window from showing
    clipboard = root.clipboard_get()  # read the clipboard
    root.destroy()
    return clipboard


def get_input_text(config):
    """
    Return text from stdin, clipboard or file.

    Returns:
        Tuple[str, str]:
            A tuple contain of the text and an optional file extension.
            If the text does not come from a file, the extension part of the
            tuple will be none.

    """
    if not sys.stdin.isatty():  # if piped into script
        lines = [line.rstrip() for line in sys.stdin.readlines() if line.rstrip()]
        return "\n".join(lines), None  # read text from pipe and remove empty lines
    elif config["clipboard"]:
        return get_clipboard(), None
    else:
        if config["input file"]:
            extension = os.path.splitext(config["input file"])[1][1:]  # get file extention without .
            try:
                with open(config["input file"], 'r') as myfile:
                    return myfile.read(), extension
            except UnicodeDecodeError:
                print("can't read text")
                sys.exit(1)
        return None, None


def print_errors(response, api_url, print_color=True, rules=False, rule_categories=False, explain_rule=False):
    matches = response["matches"]
    language = response["language"]
    version = response["software"]["name"] + " " + response["software"]["version"]

    def colored(text, color):
        if print_color:
            init_colors()
            return color + text + Fore.RESET
        else:
            return text

    print(colored(
        "{} detected ({:.0f}% confidence)".format(language["detectedLanguage"]["name"],
                                                  language["detectedLanguage"]["confidence"] * 100)
        , Fore.LIGHTBLACK_EX))
    if language["detectedLanguage"]["code"] != language["code"]:
        print(colored(
            "checking as {} text because of setting".format(language["name"])
            , Fore.LIGHTBLACK_EX))
    print()

    tick = colored(u"\u2713", Fore.LIGHTGREEN_EX) + " "
    cross = colored(u"\u2717", Fore.LIGHTRED_EX) + " "

    rule_explanations = []

    for error in matches:
        context_object = error["context"]
        context = context_object["text"]
        length = context_object["length"]
        offset = context_object["offset"]

        endposition = offset + length
        print(error["message"])

        print(
            indention[:2] +
            cross +
            colored(context[:offset], Fore.LIGHTBLACK_EX) +
            colored(context[offset:endposition], Fore.LIGHTRED_EX) +
            colored(context[endposition:], Fore.LIGHTBLACK_EX)
        )
        print(
            indention +
            offset * " " +
            colored(length * "^", Fore.LIGHTRED_EX)
        )

        if error["replacements"]:
            # only print first 5 replacements
            for replacement in error["replacements"][:5]:
                print(
                    indention[:2] +
                    tick +
                    colored(context[:offset], Fore.LIGHTBLACK_EX) +
                    colored(replacement["value"], Fore.LIGHTGREEN_EX) +
                    colored(context[endposition:], Fore.LIGHTBLACK_EX)
                )
        rule = error["rule"]
        if rules:
            print(
                indention[:2] + colored(rule["id"] + ": ", Fore.LIGHTBLACK_EX) + rule["description"]
            )
        if rule_categories:
            category = rule["category"]
            print(
                indention[:2] + colored(category["id"] + ": ", Fore.LIGHTBLACK_EX) + category["name"]
            )
        if explain_rule:
            rule = error["rule"]
            if "description" in rule and "urls" in rule and len(rule["urls"]) > 0:
                rule_explanations.append((rule["description"], rule["urls"][0]["value"]))
        print()

    if explain_rule:
        col_len = max(len(d) for d,u in rule_explanations) + 1
        for descr, url in rule_explanations:
            print(descr + ":" + " " * (col_len - len(descr)) + url)
        print()

    print(colored("Text checked by {url} ({version})".format(url=api_url, version=version), Fore.LIGHTBLACK_EX))


def main():
    config, argparser = init_config()

    if config["verbose"]:
        print(sys.version)

    if config['pwl']:
        with open(config['pwl'], 'r') as fs:
            config['pwl'] = [w.strip() for w in fs.readlines()]

    input_text, inputtype = get_input_text(config)
    if not input_text:
        argparser.print_usage()
        print("input file is required")
        sys.exit(2)
    if config["input_type"]:
        inputtype = config["input_type"]
    if inputtype == "tex":
        print("pyLanguagetool doesn't support LaTeX out of the box.")
        print("But it doesn't have to:")
        print("You can simply use the output of detex")
        if config["input file"]:
            print("    $ detex {} | pylanguagetool".format(config["input file"]))
        print("or use the languagetool integration in TeXstudio.")
        sys.exit(3)
    check_text = converters.convert(input_text, inputtype)
    if config["single_line"]:
        found = False
        for line in check_text.splitlines():
            response = api.check(line, **config)
            print_errors(response,
                         config["api_url"],
                         not config["no_color"],
                         config["rules"],
                         config["rule_categories"]
                         )
            if len(response["matches"]) > 0:
                found = True
        if found:
            sys.exit(1)

    else:
        response = api.check(check_text, **config)
        print_errors(response,
                     config["api_url"],
                     not config["no_color"],
                     config["rules"],
                     config["rule_categories"],
                     config["explain_rule"]
                     )

        if len(response["matches"]) > 0:
            sys.exit(1)
