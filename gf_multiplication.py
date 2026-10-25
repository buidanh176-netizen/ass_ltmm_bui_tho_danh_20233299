
"""
Nhan hai da thuc trong truong huu han GF(2^m)
voi da thuc toi gian cho truoc.

GF(2^4): x^4 + x + 1 -> 0x13
GF(2^8): x^8 + x^4 + x^3 + x + 1 -> 0x11B

Bieu dien: moi da thuc duoc luu bang mot so nguyen,
bit i la he so cua x^i.
"""


def poly_to_str(p: int) -> str:
    """Chuyen so nguyen thanh chuoi bieu dien da thuc."""
    if p == 0:
        return "0"

    terms = []
    for i in range(p.bit_length() - 1, -1, -1):
        if (p >> i) & 1:
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("x")
            else:
                terms.append(f"x^{i}")

    return " + ".join(terms)


def gf_mul(a: int, b: int, irreducible: int, m: int) -> int:
    """
    Nhan hai phan tu trong GF(2^m).

    - Phep cong da thuc su dung XOR.
    - Nhan voi x tuong ung dich trai 1 bit.
    - Neu xuat hien so hang x^m, rut gon bang da thuc toi gian.
    """
    if m < 1:
        raise ValueError("m phai lon hon hoac bang 1")

    mask = (1 << m) - 1

    if not (0 <= a <= mask and 0 <= b <= mask):
        raise ValueError(
            f"a va b phai nam trong khoang [0, {mask}]"
        )

    if irreducible.bit_length() != m + 1:
        raise ValueError("Da thuc toi gian phai co bac m")

    result = 0

    while b:
        if b & 1:
            result ^= a

        b >>= 1
        a <<= 1

        if (a >> m) & 1:
            a ^= irreducible

    return result & mask


# Da thuc toi gian cua hai truong
IRRED_GF16 = 0x13    # x^4 + x + 1
IRRED_GF256 = 0x11B  # x^8 + x^4 + x^3 + x + 1


def gf16_mul(a: int, b: int) -> int:
    """Nhan hai phan tu trong GF(2^4)."""
    return gf_mul(a, b, IRRED_GF16, 4)


def gf256_mul(a: int, b: int) -> int:
    """Nhan hai phan tu trong GF(2^8)."""
    return gf_mul(a, b, IRRED_GF256, 8)


def poly_mod(a: int, b: int) -> int:
    """Tinh phan du cua phep chia da thuc tren GF(2)[x]."""
    if b == 0:
        raise ValueError("Khong the chia da thuc cho 0")

    db = b.bit_length()

    while a != 0 and a.bit_length() >= db:
        a ^= b << (a.bit_length() - db)

    return a


def is_irreducible(p: int) -> bool:
    """
    Kiem tra da thuc p co toi gian tren GF(2) hay khong.

    Da thuc bac n la toi gian neu khong co uoc da thuc
    nao co bac tu 1 den n//2.
    """
    if p < 2:
        return False

    n = p.bit_length() - 1

    for d in range(1, n // 2 + 1):
        # Duyet cac da thuc co bac d
        for q in range(1 << d, 1 << (d + 1)):
            if poly_mod(p, q) == 0:
                return False

    return True


def main():
    # Kiem tra da thuc toi gian
    print("Kiem tra tinh toi gian:")

    assert is_irreducible(IRRED_GF16)
    assert is_irreducible(IRRED_GF256)

    print(f"  {poly_to_str(IRRED_GF16)}: True")
    print(f"  {poly_to_str(IRRED_GF256)}: True")

    # Vi du GF(2^4)
    print("\n=== GF(2^4) ===")

    a, b = 0b0111, 0b1010
    c = gf16_mul(a, b)

    print(
        f"({poly_to_str(a)}) * ({poly_to_str(b)}) "
        f"= {poly_to_str(c)} "
        f"[{a:#x} * {b:#x} = {c:#x}]"
    )

    # Vi du GF(2^8)
    print("\n=== GF(2^8) ===")

    a, b = 0x57, 0x83
    c = gf256_mul(a, b)

    print(
        f"({poly_to_str(a)}) * ({poly_to_str(b)}) "
        f"= {poly_to_str(c)} "
        f"[{a:#x} * {b:#x} = {c:#x}]"
    )

    # Kiem thu cac ket qua nhan
    assert gf16_mul(0x2, 0x8) == 0x3
    assert gf256_mul(0x57, 0x83) == 0xC1
    assert gf256_mul(0x57, 0x13) == 0xFE

    # Kiem thu GF(2^4)
    for x in range(16):
        assert gf16_mul(x, 1) == x
        assert gf16_mul(x, 0) == 0

        for y in range(16):
            assert gf16_mul(x, y) == gf16_mul(y, x)

    # Kiem thu nghich dao nhan trong GF(2^8)
    for x in range(1, 256):
        assert any(
            gf256_mul(x, y) == 1
            for y in range(1, 256)
        )

    print("\nTat ca test deu dung!")


if __name__ == "__main__":
    main()
