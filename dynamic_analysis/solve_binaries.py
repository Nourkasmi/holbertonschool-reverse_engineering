import subprocess
import os
import re

binaries_dir = os.path.dirname(os.path.abspath(__file__))
results = {}

for i in range(100):
    binary_name = f"binary_{i:03d}"
    binary_path = os.path.join(binaries_dir, binary_name)

    if not os.path.exists(binary_path):
        print(f"[!] Missing: {binary_name}")
        continue

    result = subprocess.run(
        ["objdump", "-d", "-M", "intel", binary_path],
        capture_output=True, text=True
    )
    asm = result.stdout

    operand_match = re.search(r'mov\s+DWORD PTR \[rbp-0xc\],(0x[0-9a-fA-F]+)', asm)
    cmp_match = re.search(r'cmp\s+eax,(0x[0-9a-fA-F]+)', asm)

    # Pattern 1: sub eax,DWORD PTR [rbp-0xc]  -> char = cmp + operand
    # Pattern 2: add eax,edx                  -> char = cmp - operand
    op_match1 = re.search(r'sub\s+eax,DWORD PTR \[rbp-0xc\]', asm)
    op_match2 = re.search(r'add\s+eax,edx', asm)

    if not operand_match or not cmp_match or (not op_match1 and not op_match2):
        print(f"[!] Could not parse {binary_name}")
        continue

    operand = int(operand_match.group(1), 16)
    cmp_val = int(cmp_match.group(1), 16)

    if op_match1:
        op = "sub"
        char_val = cmp_val + operand
    else:
        op = "add"
        char_val = cmp_val - operand

    char = chr(char_val)
    results[i] = char
    print(f"[{binary_name}] op={op}, operand={operand}, cmp=0x{cmp_val:02x} ({cmp_val}) => char='{char}' (0x{char_val:02x})")

flag = ''.join(results[i] for i in sorted(results.keys()))
print(f"\n[+] FLAG: {flag}")