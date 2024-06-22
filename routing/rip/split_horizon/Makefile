LOGFILE=out.log

.PHONY: all build create rtest testbed test restart destroy

all: destroy create testbed test
build: destroy create testbed
rtest: restart test

create:
	python create.py
	sleep 10

testbed:
	python gen_testbed.py

test:
	python test.py | tee $(LOGFILE)

restart:
	python restart.py
	sleep 10

destroy:
	python destroy.py