test:
	@tox

format:
	black supa_auth examples
	isort supa_auth examples

pip-tools:
	@pip install pip-tools

pip-install: pip-tools
	@pip install \
	-r requirements/dev.txt

pip-compile: pip-tools
	@rm -f requirements/*.txt
	@pip-compile --config=pyproject.toml --strip-extras --extra database -o requirements/base.txt
	@pip-compile --config=pyproject.toml --strip-extras --allow-unsafe --extra database,dev -o requirements/dev.txt

pip-sync: pip-tools
	@pip-sync requirements/*.txt


.PHONY: test format pip-tools pip-install pip-compile pip-sync
