This the root of all new writings in LaTeX.

Typical usage:
```
$ export PIP_INDEX_URL=https://pypi.org/simple  # to make sure you're using proper repos
$ virtualenv venv --python=python2.7

$ # see pymaging docs https://pymaging.readthedocs.io/en/latest/usr/installation.html
$ pip install -e git+git://github.com/ojii/pymaging.git#egg=pymaging
$ pip install -e git+git://github.com/ojii/pymaging-png.git#egg=pymaging-png

$ pip install -r requirements.txt

$ . venv/bin/activate
$ ./generate.py --help
```

2012–2020 burmisha
