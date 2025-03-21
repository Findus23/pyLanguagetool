#compdef pylanguagetool

# ZSH completion script for pylanguagetool
# Generated by pycomplete 0.4.0

_pylanguagetool_99ddd2e4751833f8_complete()
{
    local state com cur opts

    cur=${words[${#words[@]}]}

    # lookup for command
    for word in ${words[@]:1}; do
        if [[ $word != -* ]]; then
            com=$word
            break
        fi
    done

    if [[ ${cur} == --* ]]; then
        state="option"
        opts=("--api-key:For languagetool.org Premium API." "--api-url:the URL of the v2 languagetool API, should end with \'/v2/\'" "--clipboard:get text from system clipboard" "--disabled-categories:IDs of categories to be disabled, comma-separated" "--disabled-rules:IDs of rules to be disabled, comma-separated" "--enabled-categories:IDs of categories to be enabled, comma-separated" "--enabled-only:enable only the rules and categories whose IDs are specified with --enabled-rules or --enabled-categories" "--enabled-rules:IDs of rules to be enabled, comma-separated" "--explain-rule:print URLs with more information about rules" "--help:show this help message and exit" "--input-type:if not plaintext" "--lang:A language code like en or en-US, or auto to guess the language automatically \(see preferredVariants below\). For languages with variants \(English, German, Portuguese\) spell checking will only be activated when you specify the variant, e.g. en-GB instead of just en." "--mother-tongue:A language code of the user\'s native language, enabling false friends checks for some language pairs." "--no-color:don\'t color output" "--personal-word-list:File name of personal dictionary. A private dictionary can be used to add special words that would otherwise be marked as spelling errors." "--picky:if enabled, additional rules will be activated" "--preferred-variants:Comma-separated list of preferred language variants. The language detector used with language=auto can detect e.g. English, but it cannot decide whether British English or American English is used. Thus this parameter can be used to specify the preferred variants like en-GB and de-AT. Only available with language=auto." "--rule-categories:show the the categories of the matching rules" "--rules:show the matching rules" "--single-line:check every line on its own" "--username:For languagetool.org Premium API. Your username/email as used to log in at languagetool.org" "--verbose:verbose output" "--version:print version and exit")
    elif [[ $cur == $com ]]; then
        state="command"
        coms=()
    fi

    case $state in
        (command)
            _describe 'command' coms
        ;;
        (option)
            case "$com" in



            esac

            _describe 'option' opts
        ;;
        *)
            # fallback to file completion
            _arguments '*:file:_files'
    esac
}

_pylanguagetool_99ddd2e4751833f8_complete "$@"

