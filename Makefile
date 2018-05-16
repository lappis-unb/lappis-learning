.PHONY: clean

###############################################################################
# GLOBALS                                                                     #
###############################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = salic-ml
PYTHON_INTERPRETER = python3
PIP = pip3


###############################################################################
# COMMANDS                                                                    #
###############################################################################

## Delete all compiled Python files
clean:
	rm -f data/raw/*.csv
	rm -f data/processed/*.pickle
	rm -f data/processed/*.xlsx
	rm -f reports/figures/*.png
	rm -f models/*.model
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Install all project dependencies
install:
	$(PIP) install -r requirements.txt


###############################################################################
# NOTEBOOKS                                                                   #
###############################################################################

## Prepare notebook data
notebook_diligencies_metrics: data/raw/area.csv data/raw/projetos.csv data/raw/segmento.csv data/raw/tb_diligencia.csv

## Prepare notebook data
notebook_created_vs_finished_projects_by_year: data/raw/projetos.csv

###############################################################################
# DOWNLOAD DATA                                                               #
###############################################################################

AREAS_URL = "https://www.dropbox.com/s/z4rygyu5cryvvkl/Area.csv?dl=1"
PROJETOS_URL = "https://www.dropbox.com/s/4xboie28xzyln6x/Projetos.csv?dl=1"
SEGMENTOS_URL = "https://www.dropbox.com/s/z4rygyu5cryvvkl/Segmento.csv?dl=1"
DILIGENCIAS_URL = "https://www.dropbox.com/s/3l6ggi9xqmrzpzo/tbDiligencia.csv?dl=1"

data/raw/area.csv:
	$(PYTHON_INTERPRETER) src/data/download.py $(AREAS_URL) $@

data/raw/projetos.csv:
	$(PYTHON_INTERPRETER) src/data/download.py $(PROJETOS_URL) $@

data/raw/segmento.csv:
	$(PYTHON_INTERPRETER) src/data/download.py $(SEGMENTOS_URL) $@

data/raw/tb_diligencia.csv:
	$(PYTHON_INTERPRETER) src/data/download.py $(DILIGENCIAS_URL) $@


###############################################################################
# Self Documenting Commands                                                   #
###############################################################################

.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
