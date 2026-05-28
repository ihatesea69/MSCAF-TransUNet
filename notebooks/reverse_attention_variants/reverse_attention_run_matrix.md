# Reverse Attention notebook run matrix

Các notebook này được tạo từ `transunet-mscaf-reverse-attention.ipynb` để chạy song song ở nhiều Colab runtime/session riêng.

| Notebook | RA_SCALES | RA_REDUCTION | Snapshot suffix | Mục tiêu |
|---|---:|---:|---|---|
| `transunet-mscaf-ra-s1-r4.ipynb` | `1` | `4` | `_attn-pre_hidden-1_16-r16_ra-ra_skip-s1-r4` | Thử RA ở skip index 1 tương ứng feature 1/4 để cân bằng chi tiết biên và ngữ nghĩa. |
| `transunet-mscaf-ra-s0-r8.ipynb` | `0` | `8` | `_attn-pre_hidden-1_16-r16_ra-ra_skip-s0-r8` | Giữ RA ở skip index 0 như run vừa rồi nhưng tăng reduction lên 8 để làm RA nhẹ hơn, kỳ vọng giảm HD95. |
| `transunet-mscaf-ra-s01-r8.ipynb` | `0,1` | `8` | `_attn-pre_hidden-1_16-r16_ra-ra_skip-s01-r8` | Thử RA đa skip 0,1 để kết hợp feature 1/8 và 1/4, dùng reduction 8 để tránh RA quá mạnh. |

Mốc so sánh hiện có:
- `pre_hidden 1/16` không RA: Pancreas DSC khoảng 54.95%, Pancreas HD95 khoảng 13.91.
- `pre_hidden 1/16 + RA s0 r4`: Pancreas DSC khoảng 55.39%, Pancreas HD95 khoảng 19.29.

Tiêu chí chọn notebook tốt hơn:
- Ưu tiên Pancreas DSC cao hơn 55.39%.
- Đồng thời Pancreas HD95 nên thấp hơn 19.29, tốt nhất gần hoặc thấp hơn 13.91.
