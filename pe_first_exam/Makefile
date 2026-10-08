PYTHON ?= python3
.PHONY: initial reviewed audit test stats draft pdf all
initial:
	$(PYTHON) -B scripts/build_all.py --phase initial
reviewed:
	$(PYTHON) -B scripts/build_all.py --phase reviewed --apply
audit:
	$(PYTHON) -B scripts/audit_completeness.py
test:
	$(PYTHON) -B -m unittest discover -s tests -v
stats:
	$(PYTHON) -B scripts/generate_statistics.py
	$(PYTHON) -B scripts/find_similar_questions.py
draft:
	$(PYTHON) -B scripts/build_all.py --phase draft
pdf:
	latexmk -lualatex -outdir=build main.tex
all:
	$(PYTHON) -B scripts/build_all.py --phase final
