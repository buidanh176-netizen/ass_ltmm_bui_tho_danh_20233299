"""Chay kiem tra vector chuan, sau do chay test vector cua bai (DES + AES-128)."""
import des
import aes


def self_test():
    print("=" * 70)
    print("KIEM TRA TINH DUNG DAN VOI VECTOR CHUAN")
    print("=" * 70)
    c = des.des_crypt(0x0123456789ABCDEF, 0x133457799BBCDFF1)
    print(f"DES      : {c:016X} (ky vong 85E813540F0AB405) "
          f"{'OK' if c == 0x85E813540F0AB405 else 'SAI'}")
    c = aes.hx(aes.aes_encrypt(bytes.fromhex("00112233445566778899aabbccddeeff"),
                               bytes(range(16))))
    print(f"AES-128  : {c} (FIPS-197 C.1) "
          f"{'OK' if c == '69c4e0d86a7b0430d8cdb78070b4c55a' else 'SAI'}")
    c = aes.hx(aes.aes_encrypt(bytes.fromhex("3243f6a8885a308d313198a2e0370734"),
                               bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")))
    print(f"AES-128  : {c} (FIPS-197 B)   "
          f"{'OK' if c == '3925841d02dc09fbdc118597196a0b32' else 'SAI'}")
    print()


if __name__ == "__main__":
    self_test()
    des.run_test_vector()
    print()
    aes.run_test_vector()
