# Code Quality

We used flake8 and black libraries to increase code quality.


flake8 help
```
usage: flake8 [options] file file ...

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  -v, --verbose         Print more information about what is happening in flake8. This option is repeatable and will increase verbosity each time it is        
                        repeated.
  --output-file OUTPUT_FILE
                        Redirect report to a file.
  --append-config APPEND_CONFIG
                        Provide extra config files to parse in addition to the files found by Flake8 by default. These files are the last ones read and so     
                        they take the highest precedence when multiple files provide the same option.
  --config CONFIG       Path to the config file that will be the authoritative config source. This will cause Flake8 to ignore all other configuration files.  
  --isolated            Ignore all configuration files.
  --enable-extensions ENABLE_EXTENSIONS
                        Enable plugins and extensions that are otherwise disabled by default
  --require-plugins REQUIRE_PLUGINS
                        Require specific plugins to be installed before running
  --version             show program's version number and exit
  -q, --quiet           Report only file names, or nothing. This option is repeatable.
  --color {auto,always,never}
                        Whether to use color in output. Defaults to `auto`.
  --count               Print total number of errors to standard output after all other output.
  --exclude patterns    Comma-separated list of files or directories to exclude. (Default: ['.svn', 'CVS', '.bzr', '.hg', '.git', '__pycache__', '.tox',       
                        '.nox', '.eggs', '*.egg'])
  --extend-exclude patterns
                        Comma-separated list of files or directories to add to the list of excluded ones.
  --filename patterns   Only check for filenames matching the patterns in this comma-separated list. (Default: ['*.py'])
  --stdin-display-name STDIN_DISPLAY_NAME
                        The name used when reporting errors from code passed via stdin. This is useful for editors piping the file contents to flake8.
                        (Default: stdin)
  --format format       Format errors according to the chosen formatter (default, pylint, quiet-filename, quiet-nothing) or a format string containing
                        %-style mapping keys (code, col, path, row, text). For example, ``--format=pylint`` or ``--format='%(path)s %(code)s'``. (Default:     
                        default)
  --hang-closing        Hang closing bracket instead of matching indentation of opening bracket's line.
  --ignore errors       Comma-separated list of error codes to ignore (or skip). For example, ``--ignore=E4,E51,W234``. (Default:
                        E121,E123,E126,E226,E24,E704,W503,W504)
  --extend-ignore errors
                        Comma-separated list of error codes to add to the list of ignored ones. For example, ``--extend-ignore=E4,E51,W234``.
  --per-file-ignores PER_FILE_IGNORES
                        A pairing of filenames and violation codes that defines which violations to ignore in a particular file. The filenames can be
                        specified in a manner similar to the ``--exclude`` option and the violations work similarly to the ``--ignore`` and ``--select``       
                        options.
  --max-line-length n   Maximum allowed line length for the entirety of this run. (Default: 79)
  --max-doc-length n    Maximum allowed doc line length for the entirety of this run. (Default: None)
  --indent-size n       Number of spaces used for indentation (Default: 4)
  --select errors       Comma-separated list of error codes to enable. For example, ``--select=E4,E51,W234``. (Default: E,F,W,C90)
  --extend-select errors
                        Comma-separated list of error codes to add to the list of selected ones. For example, ``--extend-select=E4,E51,W234``.
  --disable-noqa        Disable the effect of "# noqa". This will report errors on lines with "# noqa" at the end.
  --show-source         Show the source generate each error or warning.
  --no-show-source      Negate --show-source
  --statistics          Count errors.
  --exit-zero           Exit with status code "0" even if there are errors.
  -j JOBS, --jobs JOBS  Number of subprocesses to use to run checks in parallel. This is ignored on Windows. The default, "auto", will auto-detect the number  
                        of processors available to use. (Default: auto)
  --tee                 Write to stdout and output-file.
  --benchmark           Print benchmark information about this run of Flake8
  --bug-report          Print information necessary when preparing a bug report

mccabe:
  --max-complexity MAX_COMPLEXITY
                        McCabe complexity threshold

pyflakes:
  --builtins BUILTINS   define more built-ins, comma separated
  --doctests            also check syntax of the doctests
  --include-in-doctest INCLUDE_IN_DOCTEST
                        Run doctests only on these files
  --exclude-from-doctest EXCLUDE_FROM_DOCTEST
                        Skip these files when running doctests

Installed plugins: mccabe: 0.7.0, pycodestyle: 2.10.0, pyflakes: 3.0.1
```

Flake8 Rules

https://www.flake8rules.com/

Sample command:

```
flake8 --show-source .\triplea\cli\main.py
```

```
flake8 --show-source .\triplea\cli\aaa.py --ignore F401,W292
```

```
flake8 --show-source .\triplea\cli\ --ignore F401,W292 --max-line-length 150 --output-file cli.flake8
```
```
flake8  .\triplea\cli\ --select  E225,E231 --show-source --output-file cli.txt  --format '%(path)s:%(row)d:'
```

```
flake8  .\triplea\cli\  --output-file cli.txt  --format pylint
```
```
flake8  .\triplea\cli\  --select E251 --output-file cli.txt  --format pylint --show-source
```

```
flake8  .\triplea\cli\analysis.py   --output-file cli2.txt  --format pylint --show-source --max-line-length 150 
```
```
black .\triplea\cli\analysis.py
```
```
flake8  .\triplea\cli\  --output-file cli2.txt  --format pylint --show-source --max-line-length 150 
```

```
black .\triplea\cli\
```

```
flake8  .\triplea\db\  --output-file cli2.txt  --format pylint --show-source --max-line-length 250 
```
```
black .\triplea\db\
```

```
flake8  .\triplea\  --output-file cli2.txt  --format pylint --ignore F401,W503,W504,E203 --show-source --max-line-length 451 
```

```
black .\triplea\
```

```
flake8  .\visualization\  --output-file cli2.txt  --format pylint --ignore F401,W503,W504,E203 --show-source --max-line-length 451 
```

```
black .\visualization\
```

```
flake8 .\triplea\ --count --exit-zero --max-complexity=10 --format pylint --ignore F401,W503,W504,E203 --max-line-length=451 --statistics
```