PYTHON ?= python3
.PHONY: initial all audit pdf
initial:
	$(PYTHON) scripts/build_all.py --phase initial
audit:
	$(PYTHON) scripts/audit_completeness.py
pdf:
	latexmk -lualatex -outdir=build main.tex
all:
	$(PYTHON) scripts/build_all.py --phase final
