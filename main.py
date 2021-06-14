# Custom Md5 Hash function implementation made by Jan Radzimiński
# Index number: 293052
# Md5 algorithm implementation based on algorithm from Wikipedia (https://en.wikipedia.org/wiki/MD5)

from test import test_custom_md5_hash_function

INPUT_FILES = ['test-message-1.txt',
               'test-message-2.txt', 'test-message-3.txt',  'test-message-4.txt']

print('=======================================================')
print('Md5 Hash function implementation made by Jan Radzimiński')
print('Index number: 293052')
print('=======================================================')
print('')
print('Running custom md5 hash function test with input files: ', INPUT_FILES)
print('')

for file in INPUT_FILES:
    test_custom_md5_hash_function(file)
    print('')
