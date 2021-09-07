.PHONY:	tag

TAG?=$(shell if git describe > /dev/null 2>&1 ; then   git describe; else   git rev-parse --short HEAD; fi)

tag:
	@echo ${TAG}
