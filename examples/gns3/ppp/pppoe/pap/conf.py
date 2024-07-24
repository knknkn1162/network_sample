import os
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()
CONFIG_YAML=os.environ['CONFIG_YAML']