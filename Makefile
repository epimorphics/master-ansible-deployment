all: release

release tag:
	@cd epimorphics; make -s${MAKEFLAGS} --no-print-directory $@

clean:
	@rm -f *.tar.gz
