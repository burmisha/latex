vendor:
	pip install -r requirements.txt

fmt:
	git restore generators
	black --skip-string-normalization --line-length 200 generators
	# yapf --in-place --recursive generators

reset-yapf-style:
	yapf --no-local-style --style-help > .style.yapf.tmp && mv .style.yapf.tmp .style.yapf

showcase:
	python -m streamlit run bin/showcase.py
