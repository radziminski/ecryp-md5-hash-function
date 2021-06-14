def file_to_byte_arr(filename: str):
    file = open(filename, "rb")

    return file


def len_in_bits(arr: bytearray):
    return len(arr) * 8


def get_hex_bytes_str(bytes):
    bytes_int = int.from_bytes(bytes, byteorder='big')
    return '{:032x}'.format(bytes_int)
