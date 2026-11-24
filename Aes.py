#                               AES-128
# =====================================================================
def xtime(a):
    a <<= 1
    if a & 0x100:
        a ^= 0x11B
    return a & 0xFF


def gmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a = xtime(a)
        b >>= 1
    return r
def _make_sbox():
    sb = [0] * 256
    for x in range(256):
        inv = 0 if x == 0 else next(y for y in range(1, 256) if gmul(x, y) == 1)
        s = inv
        for i in range(1, 5):
            s ^= ((inv << i) | (inv >> (8 - i))) & 0xFF
        sb[x] = s ^ 0x63
    return sb

SB = _make_sbox()
INV_SB = [0] * 256
for _i, _v in enumerate(SB):
    INV_SB[_v] = _i
RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def hx(bs):
    return "".join(f"{b:02x}" for b in bs)


def aes_key_expansion(key16, log=None):
    w = [list(key16[4 * i:4 * i + 4]) for i in range(4)]
    for i in range(4, 44):
        t = w[i - 1][:]
        if i % 4 == 0:
            t = t[1:] + t[:1]
            t = [SB[b] for b in t]
            t[0] ^= RCON[i // 4 - 1]
        w.append([w[i - 4][j] ^ t[j] for j in range(4)])
    rks = [sum(w[4 * r:4 * r + 4], []) for r in range(11)]
    if log:
        for r, rk in enumerate(rks):
            log(f"  RoundKey[{r:2d}] = {hx(rk)}")
    return rks

def sub_bytes(s, box=SB):
    return [box[b] for b in s]


def shift_rows(s):
    return [s[r + 4 * ((c + r) % 4)] for c in range(4) for r in range(4)]


def inv_shift_rows(s):
    return [s[r + 4 * ((c - r) % 4)] for c in range(4) for r in range(4)]