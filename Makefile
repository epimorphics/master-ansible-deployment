.PHONY: install release version

all: release

ARCHIVE=epimorphics-deployment-${VERSION}.tar.gz
GALAXY=galaxy.yml

${ARCHIVE}: version ${GALAXY}
	@ansible-galaxy collection build

version:
	@if [ -z "${VERSION}" ]; then echo VERSION not set; exit 1; else : ; fi

${GALAXY}: version galaxy.tmpl
	@sed -e 's/__VERSION__/${VERSION}/' galaxy.tmpl > galaxy.yml

install: ${ARCHIVE}
	@ansible-galaxy collection install --force ${ARCHIVE}

release: ${ARCHIVE}

clean:
	@rm -f *.tar.gz galaxy.yml
