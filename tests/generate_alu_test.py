#!/usr/bin/env python3
"""
ALU Test Vector Generator for Logisim-evolution
Inputs:  ZA, NA, A16[16], ZB, NB, B16[16], F, NY
Outputs: Y16[16], OVF
"""

BITS = 16
MASK = (1 << BITS) - 1
MAX_16 =  (1 << (BITS)) - 1


def to_signed(value: int) -> int:
    """Convert an unsigned 16-bit integer to a signed one."""
    return value if value <= MAX_S16 else value - (1 << BITS)

def to_bin(value: int, width: int) -> str:
    """Format an unsigned integer as a zero-padded binary string."""
    return format(value & ((1 << width) - 1), f"0{width}b")


def alu(a: int, b: int, za: int, na: int, zb: int, nb: int, f: int, ny: int):
    a &= MASK
    b &= MASK

    if za:
        a = 0
    if zb:
        b = 0
    if na:
        a = (~a) & MASK
    if nb:
        b = (~b) & MASK

    if f:
        raw = a + b
        out = raw & MASK
        ovf = to_bin(0 if raw <= MAX_16 else 1, 1)
    else:
        out = a & b
        ovf = "<DC>"  # OVF is only meaningful for addition

    if ny:
        out = (~out) & MASK

    return out, ovf


# (ZA, NA, ZB, NB, F, NY)
OPERATIONS = [
    (1, 0, 1, 0, 1, 0),  # 0
    (1, 1, 1, 1, 1, 1),  # 1
    (1, 1, 1, 0, 1, 0),  # -1
    (0, 0, 1, 1, 0, 0),  # x
    (1, 1, 0, 0, 0, 0),  # y
    (0, 0, 1, 1, 0, 1),  # !x
    (1, 1, 0, 0, 0, 1),  # !y
    (0, 0, 1, 1, 1, 1),  # -x
    (1, 1, 0, 0, 1, 1),  # -y
    (0, 1, 1, 1, 1, 1),  # x+1
    (1, 1, 0, 1, 1, 1),  # y+1
    (0, 0, 1, 1, 1, 0),  # x-1
    (1, 1, 0, 0, 1, 0),  # y-1
    (0, 0, 0, 0, 1, 0),  # x+y
    (0, 1, 0, 0, 1, 1),  # x-y
    (0, 0, 0, 1, 1, 1),  # y-x
    (0, 0, 0, 0, 0, 0),  # x&y
    (0, 1, 0, 1, 0, 1),  # x|y
]

SIGNED_TEST_VALUES = [
    0, 1, -1,
    2, -2,
    17, -17,
    127, -128,
    32767,   # INT16_MAX
    -32768,  # INT16_MIN
    1000, -1000,
]

OUTPUT_FILE = "alu_tests.txt"


def main():
    cols = ["ZA", "NA", "A16[16]", "ZB", "NB", "B16[16]", "F", "NY", "Y16[16]", "OVF"]
    rows = []

    for a_signed in SIGNED_TEST_VALUES:
        for b_signed in SIGNED_TEST_VALUES:
            a = a_signed & MASK
            b = b_signed & MASK
            for za, na, zb, nb, f, ny in OPERATIONS:
                y, ovf = alu(a, b, za, na, zb, nb, f, ny)
                rows.append([
                    to_bin(za,  1),
                    to_bin(na,  1),
                    to_bin(a,  16),
                    to_bin(zb,  1),
                    to_bin(nb,  1),
                    to_bin(b,  16),
                    to_bin(f,   1),
                    to_bin(ny,  1),
                    to_bin(y,  16),
                    ovf,  # "0"/"1" for ADD, "<DC>" for AND
                ])

    with open(OUTPUT_FILE, "w") as fh:
        fh.write(" ".join(cols) + "\n")
        for row in rows:
            fh.write(" ".join(row) + "\n")

    print(f"[✓] {len(rows)} test vectors written → {OUTPUT_FILE}")


if __name__ == "__main__":
    main()