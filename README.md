# master-ansible-deployment
A collection  of common Ansible roles.

To install:

`ansible-galaxy collection install <url to release tar ball>`

To build locally for test development (from `epimorphics/deployment`):

    VERSION=2.x.y make clean install

To release CI/CD is triggered from tag so:

    git tag $VERSION
    git push
    git push --tags

Typically use odd number `y` for local test, even for releases
