import argparse    # 1. argparseをインポート
from cmlmag.cml import Cml
lab = Cml().lab
import create, test
from logging import getLogger, StreamHandler, DEBUG
import sys

def start_log(lib: str, level=DEBUG):
  logger = getLogger(lib)
  logger.addHandler(StreamHandler(stream=sys.stdout))
  logger.setLevel(level=level)
  return logger

start_log("lib")

parser = argparse.ArgumentParser()    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('--testbed', action='store_true')
parser.add_argument('--restart', action='store_true')
parser.add_argument('--destroy', action='store_true')
parser.add_argument('--create', action='store_true')
parser.add_argument('--test', action='store_true')

args = parser.parse_args()

if args.testbed:
	lab.gen_testbed()
elif args.restart:
	lab.restart()
elif args.destroy:
	lab.delete_all()
elif args.create:
	create.main()
elif args.test:
	test.main()