Changelog
=========

'0.11.0` (2025-03-15)

* add support for Python 3.13
* drop support for Python 3.8
* fix build

  * sorry for leaving the broken 0.10.1 version unfixed for so long
* some code cleanup
* support multiple input files

  * thanks to `@Roald87`_ for the suggestion and initial implementation (`#52`_, `#49`_)

.. _@Roald87: https://github.com/Roald87
.. _#52: https://github.com/Findus23/pyLanguagetool/pull/52
.. _#49: https://github.com/Findus23/pyLanguagetool/pull/49


`0.10.1` (2024-07-20)
---------------------

* add shell completion config files
* don't use deprecated pkg_resources
* only read from stdin if no input file has been specified

`0.10.0` (2023-09-27)
---------------------

* no real code changes
* update packaging to use pyproject.toml
* update CI to test on Python 3.11

`0.9.2` (2021-10-05)
--------------------
* support Python 3.9 and 3.10
* update dev-dependencies

`0.9.1` (2020-10-01)
--------------------
* fixed value of POST parameter enabledOnly (`#42`_ by `@matze-dd`_)
* fix link for self-hosting Languagetool (`#44`_ by `@fkarg`_)


.. _#42: https://github.com/Findus23/pyLanguagetool/pull/42
.. _@matze-dd: https://github.com/matze-dd
.. _#44: https://github.com/Findus23/pyLanguagetool/pull/44
.. _@fkarg: https://github.com/fkarg

`0.9.0` (2020-01-23)
--------------------
* drop support for Python 2
* use `poetry` for development (no change for users)


`0.8.4` (2019-11-15)
--------------------
* support Python 3.8
* remove leftover `print()`
* add new option `--explain-rule` that prints URLs with more information about affected rules

`0.8.3` (2019-09-20)
--------------------
* allow overriding file extension
* improve XLIFF handling

`0.8.2` (2019-09-19)
--------------------
* output version with `-V`/`--version`
* better message when running without input

`0.8.1` (2019-09-19)
--------------------
* fix supported file formats when manually specifying `--input-type`


`0.8.0` (2019-07-19)
--------------------
* don't use goo.gl in the help text
* add new option `-r`/`--rules` to show details for matching rules
* add new option `--rule-categories` to show categories of matching rules
* print autodetected language


`0.7.1` (2019-06-14)
--------------------

* show help when trying to spellcheck LaTeX files
* extend documentation
* add Matomo to https://pylanguagetool.lw1.at/

`0.7.0` (2019-05-17)
--------------------

* add great documentation (`#40`_ by `@codingjoe`_)
* fix ``disabledCategories`` parameter (`#37`_ by `@scheijan`_)
* improve help of ``--api-url`` parameter (`#38`_)
* update dependencies
* drop support for Python 3.4

.. _#38: https://github.com/Findus23/pyLanguagetool/pull/38
.. _#40: https://github.com/Findus23/pyLanguagetool/pull/40
.. _#37: https://github.com/Findus23/pyLanguagetool/pull/37
.. _@scheijan: https://github.com/scheijan
.. _@codingjoe: https://github.com/codingjoe

`0.6.3` (2019-01-19)
--------------------

* officially support Python 3.7

`0.6.2` (2019-01-18)
--------------------

* only check markdown cells in ipython notebooks

`0.6.1` (2018-02-28)
--------------------

* fix import error messages

`0.6.0` (2017-12-29)
--------------------

* support checking single lines

`0.5.1` (2017-10-27)
--------------------

* don't spellcheck code blocks

`0.5.0` (2017-09-06)
--------------------

* support Transifex JSON

`0.4.3` (2017-05-24)
--------------------

* fix tests

`0.4.2` (2017-05-24)
--------------------

* add LanguageTool version to output

`0.4.1` (2017-01-28)
--------------------

* fix beautifulsoup

`0.4.0` (2017-01-28)
--------------------

* converters

`0.3.1` (2017-01-25)
--------------------

* strip newlines from stdin

`0.3.0` (2017-01-25)
--------------------

* max 5 replacements and "text checked by"

`0.2.1` (2017-01-24)
--------------------

* define minium dependency versions

`0.2.0` (2017-01-23)
--------------------

* add parameter to get text from system clipboard

`0.1.1` (2017-01-23)
--------------------

* parameter to disable color

`0.0.5` (2017-01-21)
--------------------

* description and tests

`0.0.4` (2017-01-20)
--------------------

* better README

`0.0.3` (2017-01-20)
--------------------

* Python 2 support


`0.0.2` (2017-01-19)
--------------------

* first working version
