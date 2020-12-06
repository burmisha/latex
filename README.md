This the root of all new writings in LaTeX.

Typical usage:
```
$ brew install imagemagick  # imagemagick is used to convert pdf
$ brew install geckodriver  # selenium requires geckodriver
$ brew install poppler  # split pdf to pdf, pdfseparate and pdfunite are used

$ export PIP_INDEX_URL=https://pypi.org/simple  # to make sure you're using proper repos
$ virtualenv venv --python=python3.8
$ . venv/bin/activate

# see pymaging docs https://pymaging.readthedocs.io/en/latest/usr/installation.html
$ pip3 install -e git+git://github.com/ojii/pymaging.git#egg=pymaging
$ pip3 install -e git+git://github.com/ojii/pymaging-png.git#egg=pymaging-png

$ pip3 install -r requirements.txt

$ . venv/bin/activate
$ ./run.py --help
```

2012–2020 burmisha
