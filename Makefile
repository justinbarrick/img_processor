.PHONY: build
build:
	docker build -t img_processor .

.PHONY: test
test:
	docker run -v $(shell pwd):/app --entrypoint /usr/bin/make img_processor run-test

.PHONY: run-test
run-test:
	nosetests -v -s --with-coverage --cover-xml-file=coverage.xml --cover-xml  
	cd docs && make html
