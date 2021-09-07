TAG?=$(shell if git describe > /dev/null 2>&1 ; then   git describe; else   git rev-parse --short HEAD; fi)

all: release move

galaxy:
	@sed -e 's/__RELEASE__/${TAG}/' galaxy.tmpl > galaxy.yml

release: galaxy
	@ansible-galaxy collection build

move:
	@mv epimorphics-deployment*.tar.gz ..

clean:
	@rm -f *.tar.gz galaxy.yml

tag:
	@echo ${TAG}
