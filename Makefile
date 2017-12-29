VERSION=$(shell git rev-list --count HEAD)-$(shell git describe --always --long)

.PHONY: build
build:
	docker build -t justinbarrick/img-processor:$(VERSION) .

.PHONY: push
push:
	docker push justinbarrick/img-processor:$(VERSION)

.PHONY: test
test:
	docker run -v $(shell pwd):/app --entrypoint /usr/bin/make justinbarrick/img-processor:$(VERSION) run-test

.PHONY: run-test
run-test:
	nosetests -v -s --with-coverage --cover-xml-file=coverage.xml --cover-xml  
	cd docs && make html

.PHONY: deploy
deploy:
	cd helm; helm --debug upgrade --set image.tag=$(VERSION) elder-bumblebee .
