.PHONY:	rpm clean

VERSION ?= 1.1.1
BUILD_NUMBER ?= 1
SOURCE = apache-storm-$(VERSION).tar.gz
TOPDIR = /tmp/storm-rpm
PWD = $(shell pwd)
URL = $(shell curl -s https://www.apache.org/dyn/closer.cgi/storm/apache-storm-$(VERSION)/apache-storm-$(VERSION).tar.gz?asjson=1 | python -c 'import sys,json; data=json.load(sys.stdin); print data["preferred"] + data["path_info"]')

rpm: $(SOURCE)
	@rpmbuild -v -bb \
			--define "_sourcedir $(PWD)" \
			--define "_rpmdir $(PWD)" \
			--define "_topdir $(TOPDIR)" \
			--define "version $(VERSION)" \
			--define "build_number $(BUILD_NUMBER)" \
			storm.spec

source: $(SOURCE)

$(SOURCE): KEYS $(SOURCE).asc
	@wget -q $(URL)
	gpg --verify $(SOURCE).asc $(SOURCE)

clean:
	@rm -rf $(TOPDIR) x86_64
	@rm -f $(SOURCE)

$(SOURCE).asc:
	@wget -q https://dist.apache.org/repos/dist/release/storm/apache-storm-$(VERSION)/$(SOURCE).asc

KEYS:
	@wget -q https://dist.apache.org/repos/dist/release/storm/KEYS
	gpg --import KEYS
