import sys

if len(sys.argv) < 2:
    print("usage: python int_to_hex.py <integer> <integer>*")

for i in range(1, len(sys.argv)):
    numb = int(sys.argv[i])
    print(hex(numb))
