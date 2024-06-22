LOGFILE=out.log

.PHONY: all build create rtest testbed test restart destroy

all: create testbed test
build: create testbed
rtest: restart test

create:
	python create.py

testbed:
	python gen_testbed.py

test:
	python test.py | tee $(LOGFILE)

restart:
	python restart.py

destroy:
	python destroy.py