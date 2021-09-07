all: release

galaxy:
	@sed -e 's/__VERSION__/${VERSION}/' galaxy.tmpl > galaxy.yml

release: galaxy
	@ansible-galaxy collection build

clean:
	@rm -f *.tar.gz galaxy.yml
