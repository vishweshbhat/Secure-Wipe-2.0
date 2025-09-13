from src.wipe_utils import wipe_file as wipe_utils_file
from src.wipe_utils import wipe_partition as wipe_utils_partition
from src.wipe_utils import wipe_os as wipe_utils_os

def wipe_file(file_path):
    return wipe_utils_file(file_path)

def wipe_partition(partition_path):
    return wipe_utils_partition(partition_path)

def wipe_os():
    return wipe_utils_os()
