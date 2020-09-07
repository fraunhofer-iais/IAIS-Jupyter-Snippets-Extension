all: wheel

install: wheel

	pip uninstall -y snippetlib || true
	pip install dist/snippetlib-*.whl

Base: 
	git clone https://jira.iais.fraunhofer.de/stash/scm/kdpyt/snippetsbase.git
	cp -r snippetsbase/Base-Snippets/* snippetlib/menu/KD-Snippets/
	

Special: 
	git clone https://jira.iais.fraunhofer.de/stash/scm/kdpyt/snippetsspecial.git
	cp -r snippetsspecial/Special-Snippets/* snippetlib/menu/KD-Snippets/

install_develop:
	pip uninstall -y snippetlib || true
	pip install -e .

wheel:
	rm -rf build dist
	python setup.py bdist_wheel

.PHONY: all wheel install
