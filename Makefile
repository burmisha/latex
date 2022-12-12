vendor:
	pip install -r requirements.txt

upgrade:
	python -m pip install --upgrade pip
	pip list --outdated > a
	cat a | awk '(NR >= 2) && ($$2 != $$3) && ($$1 != "py"){print "s/"$$1".*/"$$1"=="$$3"/g;"}' > sed.txt
	sed -i '' -f sed.txt requirements.txt

fmt:
	git restore generators
	black --skip-string-normalization --line-length 200 generators
	# yapf --in-place --recursive generators

reset-yapf-style:
	yapf --no-local-style --style-help > .style.yapf.tmp && mv .style.yapf.tmp .style.yapf

showcase:
	python -m streamlit run bin/showcase.py
