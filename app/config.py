# LOG_ROOT_DIR = HOME_DIR + "../unix_home/var/log/"

LOG_ROOT_DIR = "/var/log/"

METADATA_DIR = "../metadata/"

# Line size < chunk size
CHUNK_SIZE=1024 * 1024 * 5 # 5 MB chunk size
LINE_SIZE = 1024 * 1024 * 4 # 4 MB line size
PAGE_SIZE = 50