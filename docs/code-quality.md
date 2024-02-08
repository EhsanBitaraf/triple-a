# Code Quality

We used flake8 and black libraries to increase code quality.


# Flake8 help
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

## Flake8 Rules

https://www.flake8rules.com/

## Flake Tips

In-line Ignoring Errors:
```python
example = lambda: 'example'  # noqa: E731
```
Ignoring Entire Files:
```python
# flake8: noqa
```
## Sample command

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


```
flake8 --config=.flake8 --output-file out-flake8.txt .\triplea\cli\
```

```
black .\triplea\cli\
```
## Flake8 Tips

Per ine:
```python
# noqa: E501
```

Per page:
```python
# flake8: noqa
```

# History

### All

```sh
flake8 --config=.flake8 --count --output-file out-flake8.txt .\triplea\ --no-show-source  --statistics
```

2023-10-15
```
4     C901 'export_rayyan_csv' is too complex (21)
24    E116 unexpected indentation (comment)
6     E117 over-indented
3     E122 continuation line missing indentation or outdented
3     E125 continuation line with same indent as next logical line
14    E127 continuation line over-indented for visual indent
8     E128 continuation line under-indented for visual indent
1     E131 continuation line unaligned for hanging indent
17    E201 whitespace after '('
14    E202 whitespace before ')'
38    E203 whitespace before ':'
1     E211 whitespace before '('
6     E221 multiple spaces before operator
7     E222 multiple spaces after operator
24    E225 missing whitespace around operator
43    E231 missing whitespace after ','
4     E251 unexpected spaces around keyword / parameter equals
4     E252 missing whitespace around parameter equals
15    E261 at least two spaces before inline comment
5     E262 inline comment should start with '# '
24    E265 block comment should start with '# '
1     E271 multiple spaces after keyword
1     E301 expected 1 blank line, found 0
32    E302 expected 2 blank lines, found 1
84    E303 too many blank lines (3)
1     E402 module level import not at top of file
143   E501 line too long (112 > 90 characters)
1     E711 comparison to None should be 'if cond is None:'
4     E712 comparison to False should be 'if cond is False:' or 'if not cond:'
11    E722 do not use bare 'except'
1     E741 ambiguous variable name 'l'
78    F401 'json' imported but unused
1     F821 undefined name 'topics'
29    F841 local variable 'output_data' is assigned to but never used
63    W291 trailing whitespace
13    W292 no newline at end of file
84    W293 blank line contains whitespace
11    W391 blank line at end of file
```

select
```sh
flake8 --config=.flake8 --count --output-file out-flake8.txt .\triplea\ --no-show-source  --statistics --select E501
```

ignore
```sh
flake8 --config=.flake8 --count --output-file out-flake8.txt .\triplea\ --no-show-source  --statistics --ignore E501,W503,E722
```


```sh
black .\triplea\the_private_backyard.py

black .\triplea\the_private_backyard1.py

black .\triplea\the_private_backyard2.py

black .\triplea\the_private_backyard3.py

black .\triplea\the_private_backyard3.py

black .\triplea\the_private_backyard_mongodb.py

```

2023-10-16
```
4     C901 'export_rayyan_csv' is too complex (21)
1     E303 too many blank lines (3)
82    E501 line too long (110 > 90 characters)
10    E722 do not use bare 'except'
1     E741 ambiguous variable name 'l'
1     F821 undefined name 'topics'
5     F841 local variable 'city' is assigned to but never used
104
```
104
353
61

### cli

```sh
black .\triplea\cli\
```

```sh
flake8 --config=.flake8 --output-file out-flake8.txt .\triplea\cli\ --no-show-source  --statistics
```

0

### client

```sh
black .\triplea\client\
```

```sh
flake8 --config=.flake8 --output-file out-flake8.txt .\triplea\client\ --no-show-source  --statistics
```

0

### config


```sh
black .\triplea\config\
```

```sh
flake8 --config=.flake8 --output-file out-flake8.txt .\triplea\config\ --no-show-source  --statistics
```

0

### db

```sh
black .\triplea\db\
```

```sh
flake8 --config=.flake8 --output-file out-flake8.txt .\triplea\db\ --no-show-source  --statistics
```
0


### schemas


```sh
black .\triplea\schemas\
```

```sh
flake8 --config=.flake8 --output-file out-flake8.txt .\triplea\schemas\ --no-show-source  --statistics
```

0

### service

```sh
black .\triplea\service\
```

```sh
flake8 --config=.flake8 --count --output-file out-flake8.txt .\triplea\service\ --no-show-source  --statistics --select W291

flake8 --config=.flake8 --count --output-file out-flake8.txt .\triplea\service\ --no-show-source  --statistics --ignore E501,W503,E722

flake8 --config=.flake8 --count --output-file out-flake8.txt .\triplea\service\ --no-show-source  --statistics

```



```
4     C901 'export_rayyan_csv' is too complex (21)
1     E303 too many blank lines (3)
1     E402 module level import not at top of file
82    E501 line too long (110 > 90 characters)
2     E712 comparison to False should be 'if cond is False:' or 'if not cond:'
10    E722 do not use bare 'except'
1     E741 ambiguous variable name 'l'
5     F401 'networkx.classes.function.is_directed' imported but unused
1     F821 undefined name 'topics'
6     F841 local variable 'elapsed' is assigned to but never used
```

510
137
113
0

Don't forget `# noqa: C901`

### utils


```sh
black .\triplea\utils\
```

```sh
flake8 --config=.flake8 --output-file out-flake8.txt .\triplea\utils\ --no-show-source  --statistics
```

0

black .\triplea\

flake8 --config=.flake8 --count --output-file out-flake8.txt .\triplea\ --no-show-source  --statistics --ignore E721,W503