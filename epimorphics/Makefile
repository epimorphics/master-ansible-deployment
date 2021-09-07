all: release move

release tag:
	@cd deployment; make -s${MAKEFLAGS} --no-print-directory $@

move:
	@mv epimorphics-deployment*.tar.gz ..
