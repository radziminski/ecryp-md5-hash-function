# Custom Md5 Hash function implementation made by Jan Radzimiński
# Index number: 293052
# Md5 algorithm implementation based on algorithm from Wikipedia (https://en.wikipedia.org/wiki/MD5)

from utils import len_in_bits
from constants import SINE_BYTES as K, SHIFT_AMOUNTS as S, \
    SINGLE_1_BIT_WITH_ZEROS, EMPTY_BYTE, BITS_IN_BYTE, \
    REMAINING_BITS_NUM, MESSAGE_CHUNK_LENGTH, DEFAULT_BYTE_ORDER,\
    CHUNK_WITH_1s_512

# Initial values
a0 = 0x67452301
b0 = 0xefcdab89
c0 = 0x98badcfe
d0 = 0x10325476

# Main md5 hash function - taksed message in bytes as the input and returns
# array of 16 bytes which are the md5 hash of the input message


def hash(message: bytes):
    padded_message = md5_message_padding(message)
    message_chunks = break_into_chunks(padded_message, MESSAGE_CHUNK_LENGTH)

    initial_values = [a0, b0, c0, d0]
    values = initial_values

    for chunk in message_chunks:
        # 16 - 32bis words of 512 bit chunk
        message_words = break_into_chunks(chunk, 32)

        a, b, c, d = values

        for i in range(0, 64, 1):
            # 1st cycle
            if i <= 15:

                f = (b & c) | (~b & d)
                g = i
            # 2nd cycle
            elif 16 <= i <= 31:

                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
            # 3rd cycle
            elif 32 <= i <= 47:

                f = xor(xor(b, c), d)
                g = (3 * i + 5) % 16
            # 2th cycle
            else:

                f = xor(c, (b | (~d)))
                g = (7 * i) % 16

            f += a + K[i] + \
                int.from_bytes(message_words[g], byteorder=DEFAULT_BYTE_ORDER)

            a, d, c = d, c, b
            b = b+rotate_left(f, S[i])
            b &= CHUNK_WITH_1s_512

        for i, val in enumerate([a, b, c, d]):
            values[i] += val
            values[i] &= CHUNK_WITH_1s_512

    values_enum = enumerate(values)
    values_sum = sum([val << (32 * i) for i, val in values_enum])

    return values_sum.to_bytes(16, byteorder=DEFAULT_BYTE_ORDER)


def md5_message_padding(bytes_obj: bytes):
    bytes_arr = bytearray(bytes_obj)
    init_message_length_bits = len_in_bits(bytes_obj)

    # Appending 1 bit at the end of the message (with 7 additional 0 to fill the byte)
    bytes_arr.append(SINGLE_1_BIT_WITH_ZEROS)

    # Filling bits with 0 till the message has only 64 bits left till be a multiple of 512
    while (len(bytes_arr) % (MESSAGE_CHUNK_LENGTH / BITS_IN_BYTE) != ((MESSAGE_CHUNK_LENGTH - REMAINING_BITS_NUM) / BITS_IN_BYTE)):
        bytes_arr.append(EMPTY_BYTE)

    # Adding the length of input mod 2^64 at the end (as 64 bits)
    remaining_bits = init_message_length_bits % (2 ** REMAINING_BITS_NUM)
    remaining_bits = remaining_bits.to_bytes(
        int(REMAINING_BITS_NUM / BITS_IN_BYTE), byteorder=DEFAULT_BYTE_ORDER)

    bytes_arr += remaining_bits

    return bytes_arr


def break_into_chunks(byte_arr: bytearray, chunk_size_bits: int = 512):
    chunks = []
    chunk_size_in_bytes = int(chunk_size_bits / BITS_IN_BYTE)

    for i in range(0, int(len(byte_arr) / chunk_size_in_bytes), 1):
        chunks.append(byte_arr[(chunk_size_in_bytes * i):(chunk_size_in_bytes * (i + 1))])

    return chunks


def xor(a, b):
    return (a & ~b) | (~a & b)


def rotate_left(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount)))
