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

def mix_columns(s, inv=False):
    m = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]] if inv \
        else [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
    out = []
    for c in range(4):
        col = s[4 * c:4 * c + 4]
        for r in range(4):
            v = 0
            for k in range(4):
                v ^= gmul(m[r][k], col[k])
            out.append(v)
    return out

def add_round_key(s, rk):
    return [a ^ b for a, b in zip(s, rk)]


def aes_encrypt(pt16, key16, log=None):
    log = log or (lambda s: None )
    log("[AES] Sinh khoa vong:")
    rks = aes_key_expansion(key16, log)
    s = list(pt16)
    log(f"[AES] Input              = {hx(s)}")
    s = add_round_key(s, rks[0])
    log(f"[AES] Round 0 AddRoundKey= {hx(s)}")
    for r in range(1, 11):
        log(f"--- Round {r} ---")
        log(f"  start of round   = {hx(s)}")
        s = sub_bytes(s)
        log(f"  after SubBytes   = {hx(s)}")
        s = shift_rows(s)
        log(f"  after ShiftRows  = {hx(s)}")
        if r != 10:
            s = mix_columns()
            log(f"  after MixColumns = {hx(s)}")
        log(f"  round key        = {hx(rks[r])}")
        s = add_round_key(s, rks[r])
        log(f"  after AddRoundKey= {hx(s)}")
    return bytes(s)

def aes_decrypt(ct16, key16, log=None):
    log = log or (lambda s: None)
    rks = aes_key_expansion(key16)
    s = add_round_key(list(ct16), rks[10])
    log(f"[AES-DEC] Round 10 AddRoundKey = {hx(s)}")
    for r in range(9, -1, -1):
        s = inv_shift_rows(s)
        s = sub_bytes(s, INV_SB)
        s = add_round_key(s, rks[r])
        if r != 0:
            s = mix_columns(s, inv=True)
        log(f"[AES-DEC] Sau round nghich {10 - r}   = {hx(s)}")
    return bytes(s)



P_AES = bytes.fromhex("00000000000000000000000000000011")
K_AES = bytes(16)

def run_test_vector(out=print):
    out("=" * 70)
    out("AES-128 - TEST VECTOR CUA BAI TAP")
    out("   P = 0x00000000000000000000000000000011")
    out("   K = 0x00000000000000000000000000000000")
    out("=" * 70)
    ct = aes_encrypt(P_AES, K_AES, log=out)
    out(f"\n>>> AES-128 CIPHERTEXT = 0x{hx(ct)}")
    out("\n--- Giai ma kiem tra ---")
    pt = aes_decrypt(ct, K_AES, log=out)
    out(f">>> AES-128 PLAINTEXT sau giai ma = 0x{hx(pt)} "
        f"{'(khop)' if pt == P_AES else '(SAI)'}")


if __name__ == "__main__":
    run_test_vector()