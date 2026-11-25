# Bài tập môn Mật mã học: DES và AES-128

Cài đặt thuật toán DES và AES-128 bằng Python (chỉ dùng thư viện chuẩn), có in
giá trị kiểm định của từng trạng thái/vòng.

## Cấu trúc
| File | Nội dung |
|---|---|
| `des.py` | DES: sinh khóa con, IP, 16 vòng Feistel, FP, giải mã |
| `aes.py` | AES-128: key expansion, SubBytes, ShiftRows, MixColumns, AddRoundKey, giải mã |
| `main.py` | Kiểm tra vector chuẩn, rồi chạy test vector của bài |
| `logs/` | Kết quả chạy (DES, AES, tổng hợp) |

## Cách chạy
```bash
python3 main.py        # chạy tất cả
python3 des.py         # chỉ DES
python3 aes.py         # chỉ AES-128
```

## Test vector
| | DES | AES-128 |
|---|---|---|
| Plaintext | `0000000000000011` | `00000000000000000000000000000011` |
| Key | `0000000000000000` | `00000000000000000000000000000000` |
| Ciphertext | `799A09FB40DF6019` | `0410befccde6944b69dd007debe39a9d` |

Đã đối chiếu với vector chuẩn: DES `133457799BBCDFF1` / `0123456789ABCDEF` → `85E813540F0AB405`;
AES-128 FIPS-197 Appendix B và C.1.

Lưu ý: khóa toàn 0 là khóa yếu của DES (K1..K16 đều bằng 0).