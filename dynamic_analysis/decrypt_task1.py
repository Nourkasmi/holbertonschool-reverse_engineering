import struct

# From disassembly (little-endian 8-byte chunks):
# 0x4ef0a378ebed0049
# 0x459656f85013994a
# 0x0dabf8aa60e91585  (note: 0x0 prefix)
# 0xce48306873d32868
# 0x7323a57a29d08d6d
# 0xe1ea56d8 (4 bytes)
# 0x605f (2 bytes)
# 0x5a (1 byte)

chunks = [
    struct.pack('<Q', 0x4ef0a378ebed0049),
    struct.pack('<Q', 0x459656f85013994a),
    struct.pack('<Q', 0x0dabf8aa60e91585),
    struct.pack('<Q', 0xce48306873d32868),
    struct.pack('<Q', 0x7323a57a29d08d6d),
    struct.pack('<I', 0xe1ea56d8),
    struct.pack('<H', 0x605f),
    struct.pack('<B', 0x5a),
]

encrypted = b''.join(chunks)

def prng(state):
    state = (state * 0x41c64e6d + 0x3039) & 0x7fffffff
    return state, (state >> 16) & 0xff

def rotate_right(byte, n):
    byte = byte & 0xff
    return ((byte >> n) | (byte << (8 - n))) & 0xff

state = 0x3039
flag = ""
for enc_byte in encrypted:
    state, rnd = prng(state)
    b = (enc_byte + 0x5b) & 0xff
    b = rotate_right(b, 3)
    b = b ^ rnd
    flag += chr(b)

print(f"Flag: {flag}")