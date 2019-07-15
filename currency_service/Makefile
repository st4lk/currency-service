.PHONY: runserver, command, test

ENV ?= venv
LEVEL ?= development

install: .install
.install: requirements/main.txt
	$(ENV)/bin/pip install -r requirements/main.txt
	touch $@


install-test: .install-test
.install-test: requirements/tests.txt
	$(ENV)/bin/pip install -r requirements/tests.txt
	touch $@

runserver: install
	LEVEL=$(LEVEL) $(ENV)/bin/python app/server.py

command: install
	PYTHONPATH=app/ $(ENV)/bin/python app/commands/$(COMMAND).py $(ARGS)

test: install install-test
	LEVEL=test COMMAND=migrate $(MAKE) command
	LEVEL=test PYTHONPATH=app/ $(ENV)/bin/python -m pytest $(TEST_ARGS)
