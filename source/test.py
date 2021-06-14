import hashlib
from utils import file_to_byte_arr, get_hex_bytes_str
import md5
import time


def test_custom_md5_hash_function(message_file_path: str):
    file_to_byte_arr(message_file_path)
    bytes_obj = file_to_byte_arr(message_file_path).read()

    start_time = time.time()
    hashed_message = md5.hash(bytes_obj)
    custom_md5_time = time.time() - start_time

    hashed_message_string = get_hex_bytes_str(hashed_message)

    start_time_2 = time.time()
    hashed_message_by_hashlib = hashlib.md5(bytes_obj).hexdigest()
    hashlib_md5_time = time.time() - start_time_2

    print(
        f'Custom computed md5 hash for "{message_file_path}" (length in bytes: {len(bytes_obj)}): ', hashed_message_string)
    print(f'Hash computed in: {custom_md5_time}s')
    print(
        f'Md5 hash computed by hashlib for "{message_file_path}": ', hashed_message_by_hashlib)
    print(f'Hash computed in: {hashlib_md5_time}s')
    print('Are hashes identical: ',
          'YES!' if hashed_message_by_hashlib == hashed_message_string else 'No - something does not work.')
