from z3 import *

flag = [BitVec(f'c{i}', 32) for i in range(30)]
s = Solver()

for c in flag:
    s.add(c >= 0x20, c <= 0x7e)

s.add(flag[0] == 0x48)  # 'H'

def sx(x):
    # sign extend 8-bit to 32-bit
    return If(x > 127, x - 256, x)

def funcOne(a, b, c):
    # a*b*0x3eb + c*13 + a*c - 0x64
    t1 = a * b
    t2 = t1 * 0x3eb
    t3 = c + c  # c*2
    t3 = t3 + c  # c*3
    t3 = t3 * 4  # c*12
    t3 = t3 + c  # c*13
    t4 = a * c
    return t2 + t3 + t4 - 0x64

def funcTwo(a, b, c):
    t1 = a * c - 0x539
    t2 = b * 0x65
    t3 = t1 + t2
    t4 = a + b + 0x89
    t5 = t3 - t4
    t6 = a * b - 0x43e5
    return t5 + t6

def funcThree(a, b, c):
    return a * b + URem(b, 19)

def funcFour(a, b, c):
    return a * b * c - b * c

def funcFive(a, b, c):
    t = a + b * c
    return URem(t, 10000)

def funcSix(a, b, c):
    return a * b + c - b * c

def funcSeven(a, b, c):
    return a * b + c * c - c

def funcEight(a, b, c):
    return a * b * c - b * c

def funcNine(a, b, c):
    return a * b - c * b + a - 0x64

def funcTen(a, b, c):
    return c * (a + b) - 0x2710 + b

def funcEleven(a, b, c):
    return a * b * c - 0x539 + a * b

def funcTwelve(a, b, c):
    # a*c + b*(4+1)*2 - a + 0x89 = a*c + b*10 - a + 0x89
    return a * c + b * 10 - a + 0x89

def funcThirteen(a, b, c):
    t = a * b * c
    return URem(t, 10000) - 0x1f4

def funcFourteen(a, b, c):
    return a * b * c - a * b + c

def funcFifteen(a, b, c):
    return (a + b + c) * 0x539 - c

def funcSixteen(a, b, c):
    # a*b + c*(4+1)*2 - a*c + 0x1f4
    return a * b + c * 10 - a * c + 0x1f4

def funcSeventeen(a, b, c):
    return a * b - c * b + c * 0x65

def funcEighteen(a, b, c):
    return a * b * c - b * c + a * 0x89

def funcNineteen(a, b, c):
    return a + b + c * 0x89 - c * b

def funcTwenty(a, b, c):
    return a * b + c * c - a * c

constraints = [
    (funcOne,       0,  1,  2,  0x7a73e0),
    (funcTwo,       1,  2,  3,  0x396c),
    (funcThree,     2,  3,  4,  0x295b),
    (funcFour,      3,  4,  5,  0x110aba),
    (funcFive,      4,  5,  6,  0xcfd),
    (funcSix,       5,  6,  7,  0x1cb),
    (funcSeven,     6,  7,  8,  0x6122),
    (funcEight,     7,  8,  9,  0x16b5ac),
    (funcNine,      8,  9,  10, 0x5ce),
    (funcTen,       9,  10, 11, 0x2d0f),
    (funcEleven,    10, 11, 12, 0x10ce2f),
    (funcTwelve,    11, 12, 13, 0x2c6f),
    (funcThirteen,  12, 13, 14, 0x133d),
    (funcFourteen,  13, 14, 15, 0xee949),
    (funcFifteen,   14, 15, 16, 0x64d5a),
    (funcSixteen,   15, 16, 17, 0xc6c),
    (funcSeventeen, 16, 17, 18, 0x2d63),
    (funcEighteen,  17, 18, 19, 0x105869),
    (funcNineteen,  18, 19, 20, 0x13b1),
    (funcTwenty,    19, 20, 21, 0x319d),
    (funcOne,       22, 23, 24, 0xc33bd5),
    (funcTwo,       23, 24, 25, 0x4201),
    (funcThree,     24, 25, 26, 0x2d2d),
    (funcFour,      25, 26, 27, 0x104645),
    (funcFive,      26, 27, 28, 0xca6),
    (funcSix,       27, 28, 29, 0xfffffc9f),
]

for fn, i, j, k, val in constraints:
    s.add(fn(flag[i], flag[j], flag[k]) == val)

print("Solving...")
if s.check() == sat:
    m = s.model()
    result = ''.join(chr(m[flag[i]].as_long()) for i in range(30))
    print(f"Flag: {result}")
else:
    print("No solution found - checking which constraints fail...")
    # Debug: test each constraint individually
    for fn, i, j, k, val in constraints:
        s2 = Solver()
        for c in flag:
            s2.add(c >= 0x20, c <= 0x7e)
        s2.add(flag[0] == 0x48)
        s2.add(fn(flag[i], flag[j], flag[k]) == val)
        if s2.check() == unsat:
            print(f"  UNSAT: func with indices {i},{j},{k} == {hex(val)}")