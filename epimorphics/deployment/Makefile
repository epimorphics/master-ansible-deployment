all: release

galaxy:
	@sed -e 's/__VERSION__/${VERSION}/' galaxy.tmpl > galaxy.yml

release: galaxy
	@ansible-galaxy collection build epimorphics-deployment-${VERSION}.tar.gz

clean:
	@rm -f *.tar.gz galaxy.yml
