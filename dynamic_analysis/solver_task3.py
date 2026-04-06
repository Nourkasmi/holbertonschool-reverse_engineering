import struct

# Key from strings output
key = b"kjkjf_ckzj9274jdlfdvn-dpakkk__AhfNNtdsp592"

# Target values from decrypted code (little-endian 32-bit)
targets = [
    (0,  0x08070523),
    (4,  0x04172d03),
    (8,  0x5a4e1114),
    (12, 0x05354056),
    (16, 0x0211090e),
    (20, 0x033b4c31),
    (24, 0x340d0704),
    (28, 0x11253032),
    (32, 0x13202700),
    (36, 0x5a02033b),
]
# Last 2 bytes (word)
last = (40, 0x4f5e)

# The decrypted code receives x1(input, key, 0x80)
# x1 XORs input[i] with key[i % keylen]
# So: xored[i] = input[i] ^ key[i % keylen]
# We know xored values from the targets
# So: input[i] = xored[i] ^ key[i % keylen]

keylen = len(key)

# Build xored buffer from targets
xored = [0] * 42

for offset, val in targets:
    chunk = struct.pack('<I', val)
    for j in range(4):
        xored[offset + j] = chunk[j]

# Last word
chunk = struct.pack('<H', last[1])
xored[40] = chunk[0]
xored[41] = chunk[1]

# Recover input by XORing back with key
flag = ""
for i in range(42):
    c = xored[i] ^ key[i % keylen]
    flag += chr(c)

print(f"Flag: {flag}")

# Verify
print("\nVerifying...")
xored_check = []
for i in range(len(flag)):
    xored_check.append(ord(flag[i]) ^ key[i % keylen])

for offset, val in targets:
    chunk = struct.unpack('<I', bytes(xored_check[offset:offset+4]))[0]
    status = "OK" if chunk == val else f"FAIL (got {hex(chunk)})"
    print(f"  offset {offset}: {hex(val)} -> {status}")
