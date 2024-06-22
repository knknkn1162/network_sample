LOGFILE=out.log

.PHONY: all build create rtest testbed test restart destroy

all: destroy create testbed test
build: destroy create testbed
rtest: restart test

create:
	python create.py

testbed:
	python gen_testbed.py

test:
	python test0.py | tee $(LOGFILE)
	python test1.py | tee --append $(LOGFILE)
	python test2.py | tee --append $(LOGFILE)

restart:
	python restart.py

destroy:
	python destroy.py