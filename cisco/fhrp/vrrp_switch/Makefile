LOGFILE=out.log

.PHONY: all build create rtest testbed test restart destroy

all: destroy create testbed test
build: destroy create testbed
rtest: restart test

create:
	python main.py --create

testbed:
	python main.py --testbed

test:
	python main.py --test | tee $(LOGFILE)

restart:
	python main.py --restart

destroy:
	python main.py --destroy
