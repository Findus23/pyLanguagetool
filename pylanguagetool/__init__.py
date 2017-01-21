# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
from pprint import pprint
import configargparse
from colorama import Fore

from . import api

indention = " " * 4


def init_config():
    p = configargparse.ArgParser(default_config_files=["~/.config/pyLanguagetool.conf"])
    p.add_argument("-v", "--verbose", env_var="VERBOSE", default=False, action='store_true')
    p.add_argument("-a", "--api-url", env_var="API_URL", default="https://languagetool.org/api/v2/")
    p.add_argument('input file', help='input file', nargs='?')

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

    c = vars(p.parse_args())
    if c["enabled_only"] and (c["disabled_categories"] or c["disabled_rules"]):
        print("disabled not allowed")  # TODO: ?
    if c["preferred_variants"] and c["lang"] != "auto":
        # print("You specified --preferred_variants but you didn't specify --language=auto")
        # sys.exit(2)
        print('ignoring --preferred-variants as --lang is not set to "auto"')
        c["preferred_variants"] = None
    if c["verbose"]:
        pprint(c)
    return c


def get_input_text(config):
    if sys.stdin.isatty():
        if config["input file"]:
            with open(config["input file"], 'r') as myfile:
                return myfile.read()
        else:
            print("input file required")
            sys.exit(2)
    else:
        return "\n".join(sys.stdin.readlines())


def print_errors(matches, print_color=True):
    def colored(text, color):
        if print_color:
            return color + text + Fore.RESET
        else:
            return text

    tick = colored(u"\u2713", Fore.LIGHTGREEN_EX) + " "
    cross = colored(u"\u2717", Fore.LIGHTRED_EX) + " "

    for error in matches:
        context_object = error["context"]
        context = context_object["text"]
        length = context_object["length"]
        offset = context_object["offset"]

        endpostion = offset + length
        print(error["message"])

        print(
            indention[:2] +
            cross +
            colored(context[:offset], Fore.LIGHTBLACK_EX) +
            colored(context[offset:endpostion], Fore.LIGHTRED_EX) +
            colored(context[endpostion:], Fore.LIGHTBLACK_EX)
        )
        print(
            indention +
            offset * " " +
            colored(length * "^", Fore.LIGHTRED_EX)
        )

        if error["replacements"]:
            for replacement in error["replacements"]:
                print(
                    indention[:2] +
                    tick +
                    colored(context[:offset], Fore.LIGHTBLACK_EX) +
                    colored(replacement["value"], Fore.LIGHTGREEN_EX) +
                    colored(context[endpostion:], Fore.LIGHTBLACK_EX)
                )
            print()


def main():
    config = init_config()

    if config["verbose"]:
        print(sys.version)

    text = get_input_text(config)
    response = api.check(text, **config)

    print_errors(response["matches"])

    if len(response["matches"]) > 0:
        sys.exit(1)
