# Báo cáo sửa khóa luận theo nhận xét GVHD — vòng 2

**Sinh viên:** Danh Hoàng Hiếu Nghị – 23DH112270
**Đề tài:** Phân đoạn ảnh tuyến tụy trên cơ chế Attention
**GVHD:** TS. Võ Thị Hồng Tuyết
**Ngày thực hiện:** 04/08/2026

---

## 1. File bàn giao

| File | Mô tả |
|---|---|
| `KLTN - Danh Hoàng Hiếu Nghị - K29 (v2).docx` | **Bản mới**, đã sửa theo toàn bộ nhận xét — 90 trang |
| `KLTN - Danh Hoàng Hiếu Nghị - K29 (v2).pdf` | Bản PDF xuất từ Word |
| `KLTN - Danh Hoàng Hiếu Nghị - K29.docx` | Bản cũ (vòng 1) — giữ nguyên để đối chiếu |
| `(Draft 1 ) Khóa Luận Tốt Nghiệp HUFLIT -K29- ....docx` | Bản gốc — chưa bao giờ bị sửa |

| Quy mô | Vòng 1 | Vòng 2 |
|---|---|---|
| Số trang | 72 | **90** |
| Số từ | 21.852 | **29.251** |
| Số bảng | 17 | **18** |
| Số hình | 10 | 10 |
| Số công thức | 13 | **14** |
| Tài liệu tham khảo | 22 | **29** |
| Đoạn văn xuôi có dẫn nguồn | 12% | **59%** |
| Số lần dẫn nguồn trong thân bài | ~24 | **227** |
| TLTK có DOI/URL | 1/22 | **29/29** |
| Viết tắt bung đúng lần dùng đầu | 13 chỗ sai | **đạt hết** |

Chuỗi xử lý chạy lại được bất cứ lúc nào:

```bash
python .fmt_audit/make_metrics_chart.py && python .fmt_audit/merge_paper.py && python .fmt_audit/revise_gvhd.py && python .fmt_audit/fmt_kltn.py && python .fmt_audit/update_fields.py && python .fmt_audit/verify.py && python .fmt_audit/audit_tridan.py
```

---

## 2. Đối chiếu từng nhận xét của GVHD

| # | Nhận xét | Đã xử lý |
|---|---|---|
| 1 | Lời cam đoan có chữ ký, ngay đó | Thêm khối `TP. Hồ Chí Minh, ngày … tháng … năm 2026` / `Sinh viên thực hiện` / `(Ký và ghi rõ họ tên)` / họ tên, canh phải cuối trang LỜI CAM ĐOAN |
| 2 | Danh mục → để bảng, sắp theo bảng chữ cái, chỉ để bảng, không cần mô tả ở trên | Bỏ đoạn mô tả và caption “Bảng 0.1”; sắp lại **56 mục theo A→Z** (54 dòng đổi vị trí); mục này cũng tự rời khỏi DANH MỤC CÁC BẢNG |
| 3 | 1,5 giãn dòng, trừ trang bìa | Nội dung `w:line=360` (1,5 dòng); trang bìa và ô bảng giãn đơn |
| 4 | Bảng biểu size 13 | `BangText`/`BangHeader` về **13pt**, xóa hẳn hai style 11pt; viết lại thuật toán chia cột (trần bề rộng theo số cột, nhận biết điểm ngắt dòng của Word) → **18/18 bảng vừa khổ 15,5 cm, không gãy chữ** |
| 5 | Trích dẫn trong bài luận, cơ sở lý thuyết | Thêm **7 nguồn mới**; gắn nguồn **tại chỗ cho từng luận điểm** suốt Chương 2 và Chương 3, không dẫn một lần rồi thôi. Tỷ lệ đoạn văn xuôi có dẫn nguồn: **12% → 59%** (Chương 3 trước đây 0%) |
| 6 | “Cho nên những công trình nghiên cứu tuyến tụy là vấn đề được lưu tâm” | Chèn vào cuối đoạn nói về tuyến tụy ở mục 1.1, kèm dẫn chứng dịch tễ GLOBOCAN |
| 7 | Xài 1 lần đầu tiên, ghi chú | Bung dạng đầy đủ **đúng tại lần dùng đầu tiên trong thân bài**, các lần sau chỉ dùng viết tắt. Script `audit_tridan.py` rà toàn bộ 56 mục của danh mục viết tắt và xác nhận **không còn chỗ nào bung muộn** (trước đó sai 13 chỗ: CBAM dùng ở 1.1 mà bung tận 2.6, ResNet/CUP/Synapse/FCN/MLP/Dice chưa bung) |
| 8 | “Như vậy cần một phương pháp giải quyết” | Chèn làm câu chốt đoạn kỹ thuật ở mục 1.1 |
| 9 | Thiếu dẫn đoạn kết nối giữa các đoạn | Thêm **7 đoạn dẫn nối** giữa các mục của Chương 2 |
| 10 | Ghi rõ nguồn dataset, 18 × 12 | Mục **4.1 Giới thiệu bộ dữ liệu** mới: nguồn Synapse / MICCAI 2015 BTCV, điều kiện sử dụng, 30 ca, cách chia **18/12**, 8 cơ quan, 2.211 lát 2D, tiền xử lý |
| 11 | Đóng góp thực tiễn, chuyển đoạn trên, phải có câu chuyển | Mục 1.3: thêm câu chuyển vào đầu đoạn đóng góp và tách **đóng góp thực tiễn** thành đoạn riêng (3 đóng góp) |
| 12 | Giải thích công thức, từng thành phần, sao ra công thức | **Cả 14 công thức** theo mẫu: câu dẫn → công thức → khối `trong đó:` gạch đầu dòng từng ký hiệu (ý nghĩa, miền giá trị, đơn vị) → đoạn nêu **nguồn gốc công thức** |
| 13 | Những vấn đề tồn đọng, ưu điểm, nhược điểm | Bảng 2.4 thêm cột thứ tư **“Vấn đề còn tồn đọng”** cho cả bốn nhóm mô hình |
| 14 | Kết chương 2 / tổng kết chương, chương nào cũng có | Thêm **1.5**, **2.14**, **3.8**, **4.8 Tổng kết chương** (Chương 5 là chương kết luận nên không cần) |
| 15 | Định hướng 4 hướng | Mục 2.13 thêm hai đoạn nêu rõ **bốn hướng đặt attention** sẽ khảo sát và lý do chọn đúng bốn hướng |
| 16 | Table + hình phải có tham số, bảng tham số | **Bảng 3.5 mới** (số tham số 5 cấu hình + chênh lệch tuyệt đối/tương đối) và **cột “Tham số (triệu)” trong Bảng 4.3** |
| 17 | Tại sao đưa 4 nhánh, tham số, tại sao | Mục 3.6 thêm hai đoạn: bốn nhánh sinh ra từ **hai trục nhị phân** (trước/sau bước tạo token × một tầng/nhiều tầng, trước/sau hợp nhất), và chênh lệch tham số < 1,41 triệu nên so sánh là công bằng |
| 18 | Giới thiệu dataset | Mục 4.1 (xem #10) |
| 19 | Cấu hình hệ thống riêng | Mục **4.2 Cấu hình hệ thống và môi trường thực nghiệm** mới: Tesla T4 16 GB, RAM, PyTorch/CUDA, ràng buộc bộ nhớ quyết định kích thước lô |
| 20 | 4.3 độ đo sử dụng đã trình bày ở mục 2.10, 2.11 | Mục **4.3** nêu rõ bốn độ đo *“đã được định nghĩa và giải thích đầy đủ ở mục 2.10 và mục 2.11, nên ở đây không trình bày lại công thức”*, chỉ nhắc hai quy ước đọc kết quả |
| 21 | 4 nhánh đề xuất ghi rõ ở tên bảng | Tên **Bảng 3.3, 4.3, 4.4** liệt kê đích danh bốn nhánh; các dòng bảng 3.3, 3.4, 3.5, 4.3, 4.4 và trục hoành Hình 4.1 đều đánh **“Nhánh 1–4”** thống nhất |
| 22 | Vừa nêu kết quả vừa phân tích | Gộp “4.2 Kết quả định lượng” và “4.3 Phân tích kết quả” thành một mục **4.4 Kết quả và phân tích** |
| 23 | Chương 5 ưu nhược điểm phương pháp | Mục **5.2 Ưu điểm và nhược điểm của phương pháp đề xuất** mới (4 ưu điểm, 4 nhược điểm); Hướng phát triển thành 5.3 |

---

## 3. Bảy tài liệu tham khảo bổ sung

Đã đối chiếu từng nguồn với Crossref trước khi ghi (đúng tên, tác giả, tạp chí, tập, số, trang, năm).

| Nguồn | Dùng ở |
|---|---|
| G. N. Hounsfield, *Br. J. Radiol.*, 46(552), 1016-1022, 1973 | 1.1, 2.1 — đơn vị Hounsfield |
| G. Litjens et al., *Med. Image Anal.*, 42, 60-88, 2017 | 1.1, 2.2 — khảo sát học sâu ảnh y khoa |
| H. R. Roth et al., MICCAI 2015, 556-564 (DeepOrgan) | 1.1, 2.3 — phân đoạn tuyến tụy |
| J. Ma et al., *IEEE TPAMI*, 44(10), 6695-6714, 2022 (AbdomenCT-1K) | 1.1, 2.1, 2.3 |
| H. Sung et al., *CA Cancer J. Clin.*, 71(3), 209-249, 2021 (GLOBOCAN 2020) | 1.1 — dịch tễ ung thư tụy |
| M. Antonelli et al., *Nat. Commun.*, 13:4128, 2022 (Medical Segmentation Decathlon) | 2.1, 2.3 |
| Z. Zhou et al., DLMIA 2018, 3-11 (UNet++) | 2.13 — trước đây chỉ nhắc tên, không dẫn nguồn |

Toàn bộ 29 tài liệu được đánh số lại tự động theo **thứ tự xuất hiện IEEE**; mỗi tài liệu đều
được trích dẫn ít nhất một lần trong thân bài.

---

## 4. Kết quả kiểm tra tự động — **39/39 tiêu chí ĐẠT**

`python .fmt_audit/verify.py` (kết quả đầy đủ ở `.fmt_audit/verify_out.txt`). Ngoài 23 tiêu chí
hình thức của vòng 1, bổ sung 16 tiêu chí cho nhận xét vòng 2 và cho phần đối chiếu
với khóa luận mẫu:

- Mọi ô bảng dùng style 13pt, không còn style 11pt
- Nội dung 1,5 dòng / trong ô bảng giãn đơn
- LỜI CAM ĐOAN có đủ khối ngày tháng + chữ ký + họ tên
- Danh mục viết tắt chỉ có bảng và sắp đúng A→Z
- Đủ 4 mục Tổng kết chương (1.5, 2.14, 3.8, 4.8)
- Chương 5 có mục ưu/nhược điểm
- Các mục 1.1–1.3 và 2.1–2.3 đều có trích dẫn
- Mọi tài liệu trong danh mục đều được trích dẫn trong thân bài
- Cả 14 công thức đều có khối “trong đó:”
- Bảng kết quả có cột số tham số
- Có bảng tham số riêng
- Tên bảng gọi đích danh bốn nhánh đề xuất
- Mỗi [n] là liên kết nhảy tới đúng mục TLTK, không có liên kết chết
- Liên kết trích dẫn giữ chữ đen, không gạch chân
- Mọi tài liệu tham khảo có DOI hoặc URL
- Chỉ dùng [Online]/[Accessed] cho nguồn trực tuyến

---

## 4b. Hai yêu cầu học thuật — đo bằng `audit_tridan.py`

```bash
python .fmt_audit/audit_tridan.py
```

**(1) Viết tắt bung đúng lần dùng đầu tiên — ĐẠT.** Script rà 56 mục của danh mục viết tắt,
tìm vị trí xuất hiện đầu tiên trong thân bài (bỏ qua tiêu đề mục, vì quy ước là đặt dạng đầy đủ
ở câu văn đầu tiên chứ không nhồi vào tiêu đề) và đối chiếu với vị trí dạng đầy đủ.

**(2) Mật độ trích dẫn — 12% → 59%.** Đo trên 220 đoạn văn xuôi từ 25 từ trở lên (không tính
dòng gạch đầu dòng chú giải ký hiệu công thức).

| Chương | Trước | Sau |
|---|---|---|
| Chương 2 (cơ sở lý thuyết) | 6–29% tùy mục | 57–100% |
| Chương 3 (phương pháp) | **0%** | 43–86% |
| Chương 4 (mục thiết lập) | 0–40% | 40–100% |

27 đoạn còn lại **cố ý không có trích dẫn** vì đó là tiếng nói của chính khóa luận, dẫn nguồn
vào sẽ sai: mục tiêu và câu hỏi nghiên cứu, phương pháp và đóng góp, giả thuyết và định hướng,
các câu chuyển đoạn, phần dẫn xuất công thức từ công thức đã dẫn nguồn ở trên, và các con số
tham số do khóa luận tự đo.

Ngoài ra `fmt_kltn.py` bổ sung bước `sort_citation_groups()` sắp các nhóm trích dẫn liền nhau
theo thứ tự tăng dần (`[13], [4]` → `[4], [13]`) đúng quy ước IEEE — đã sắp lại 16 nhóm.

---

## 4c. Đối chiếu với khóa luận mẫu (PointCloud – GVHD đưa)

Đã phân tích khóa luận mẫu trên 5 góc (bố cục, dẫn nguồn, hình/bảng, định dạng, văn phong),
rút ra 51 nhận định, 12 đề xuất sửa; sau vòng phản biện đối kháng còn **3 đề xuất đứng vững**.

**Đã áp dụng:**

| Học từ bài mẫu | Đã làm |
|---|---|
| Mọi `[n]` là liên kết bấm được | **233 liên kết** `[n]` → đúng mục TLTK bằng bookmark nội bộ. Khác bài mẫu ở chỗ giữ **chữ đen không gạch chân** (bài mẫu để xanh #1155cc gạch chân, in ra giấy trông như trang web) |
| Nguồn phải tra cứu được | **29/29 mục TLTK có DOI hoặc URL** — 27 DOI kiểm chứng ngược qua Crossref/DataCite, riêng Synapse giữ `[Online]. Available … [Accessed]` |
| Dẫn nguồn cho từng câu, không dẫn một lần rồi thôi | Lặp lại `[n]` ở **21 câu** trong cùng đoạn. Số đoạn có nguồn được dẫn lại: **2 → 22** |

**Lỗi phát hiện được nhờ việc tra DOI:** mục `[26]` FMD-TransUNet ghi `arXiv:2504.01517` —
mã đó thực ra thuộc một bài **vật lý hạt** ("Cascade topologies in rare charm decays").
Đã thay bằng bản đã xuất bản: *Applied Intelligence*, vol. 56, no. 6, art. 211, 2026,
doi 10.1007/s10489-026-07240-y.

**Không áp dụng (bài mẫu sai hoặc yếu hơn):**

| Bài mẫu | Vì sao không theo |
|---|---|
| Lề trên/dưới **2,5 cm**, header cách mép **1,5 cm** | Trái hướng dẫn Khoa (3 cm và 2,25 cm). Bài này đã đúng |
| Caption gán style **Heading2** | Làm caption lọt vào MỤC LỤC — lỗi trình bày, không phải kiểu trình bày |
| Danh mục bảng/hình **gõ tay** | Bài mẫu có mô tả trong danh mục lệch với thân bài. Bài này dùng field TOC nên luôn khớp |
| Đánh số trang **Ả Rập xuyên suốt** | Bài này dùng La Mã cho phần đầu, Ả Rập từ Chương 1 — đúng thông lệ hơn |
| Chương/mục **không đánh số** (style Title) | Hướng dẫn Khoa ghi rõ "Chương 1.", "2.1.", "2.1.1." |
| Tiêu đề **in nghiêng** | Không phù hợp thông lệ |
| TLTK phần lớn là **blog / trang web** | 29 nguồn của bài này đều là hội nghị/tạp chí (MICCAI, CVPR, NeurIPS, ICLR, Nature Methods…) — đổi sang blog là bước lùi |
| `[Online]. Available/[Accessed]` cho **mọi** mục | Chuẩn IEEE chỉ dùng cho nguồn chỉ tồn tại trực tuyến; bài báo dùng `doi:` |
| In đậm ký hiệu trong khối "trong đó:" | Bài này dùng **in nghiêng** — đúng chuẩn ISO 80000-2 cho ký hiệu toán học |

**Sinh viên đã quyết định không làm:** thêm mục TÓM TẮT KHÓA LUẬN, và dùng nhãn in đậm
mở đầu đoạn (bài mẫu có 75 nhãn).

---

## 5. Ghi chú kỹ thuật

**Lỗi đã sửa trong bộ script.** `lxml.itertext()` trả về nội dung ô bảng **lặp ba lần**
(`Patch` → `PatchPatchPatch`) vì python-docx gắn thuộc tính `text` cho cả `w:p`, `w:r` lẫn `w:t`.
Lỗi này làm phép đo “từ dài nhất của cột” bị thổi lên gấp ba và chia cột sai. Đã thay bằng hàm
`cell_text()` chỉ đọc `w:t`.

**Ký hiệu toán trong phần giải thích công thức** dùng run có `w:vertAlign` (chỉ số dưới/trên thật
của Word) thay vì ký tự Unicode `ₖ`, `ᴄ`, `ᵀ` — Times New Roman không có glyph cho các ký tự đó
nên Word sẽ thay bằng font khác và chỉ số hiện ra to bằng chữ thường.

**Bảng 3.3** được gộp ba cột tham số (`attention_mode`, `attention_scales`, `ra_mode`) thành một
cột “Tham số dòng lệnh”. Ở cỡ chữ 13, chuỗi `attention_scales` dài 16 ký tự và Word không ngắt
dòng sau dấu gạch dưới, nên giữ 5 cột sẽ chắc chắn gãy chữ.

**Bảng 4.3** bỏ cột `STT` và cột `Run` để lấy chỗ cho cột Tham số. Tên run kỹ thuật
(`baseline`, `mscaf_3scale`, `pre_hidden_03`, `ra_skip`, `ra_concat`) vẫn tra được ở
**Bảng 4.7** và **Phụ lục A**.

**Hình 4.1** được vẽ lại với nhãn tiếng Việt và đánh số nhánh khớp Bảng 3.3 / 3.5 / 4.3
(trước đây còn nhãn tiếng Anh `Baseline`, `MS-CBAM`, `CBAM pre-patch`…).

---

# Vòng 5 — bỏ thuật ngữ “baseline / pipeline”, bổ sung công bố khoa học

**File làm việc:** `(Draft 05082026) KLTN - Danh Hoàng Hiếu Nghị - K29.docx`
(bản sinh viên tự chỉnh trang bìa ngày 05/08/2026, sửa trực tiếp trên file này;
bản gốc trong `Downloads` giữ nguyên, bản dự phòng ở `.fmt_audit/_bak_draft05082026.docx`).
Chạy lại toàn bộ bằng `python .fmt_audit/revise_r5.py && python .fmt_audit/update_fields.py "<file>"`.

## 6. Đổi thuật ngữ

| Từ cũ | Từ mới | Số chỗ |
|---|---|---|
| `TransUNet nền` (trong ô bảng) | `Kiến trúc TransUNet` | 3 |
| `TransUNet nền` (trong câu, chú thích) | `kiến trúc TransUNet` | 14 |
| `cấu hình nền` | `kiến trúc TransUNet` | 23 |
| `so với nền` | `so với kiến trúc TransUNet` | 3 |
| `Pipeline TransUNet nền` (tiêu đề mục 3.2 + MỤC LỤC) | `Kiến trúc TransUNet` | 2 |
| `pipeline` | `luồng xử lý` | 10 |
| `Dice nền` / `HD95 nền` (tiêu đề cột Bảng 4.5) | `Dice TransUNet` / `HD95 TransUNet` | 2 |
| `Mô hình nền có 105,28 triệu tham số` | `Kiến trúc TransUNet có 105,28 triệu tham số` | 1 |
| dòng `Baseline` trong DANH MỤC VIẾT TẮT | đã bỏ (danh mục còn 55 mục) | 1 |

Năm câu phải viết lại tay vì thay máy móc sẽ lặp chữ “TransUNet” hai lần hoặc sai nghĩa:

- “TransUNet [8], **kiến trúc nền của khóa luận**, …” → “… **kiến trúc mà khóa luận lấy làm đối tượng khảo sát**, …”
- “khi khóa luận chọn TransUNet làm **mô hình nền**” → “khi khóa luận chọn **kiến trúc TransUNet làm đối tượng khảo sát**”
- “**Cấu hình nền được dùng làm mốc so sánh là TransUNet ở dạng lai** R50-ViT-B/16” → “**Kiến trúc TransUNet được dùng làm mốc so sánh có dạng lai** R50-ViT-B/16”
- “câu trả lời mà khóa luận **lấy làm nền**” → “… **lấy làm điểm xuất phát**” (ở đây “nền” là nền tảng lập luận, không phải mốc so sánh)
- “**Trên nền TransUNet**, chương đã chỉ ra…” → “**Trên kiến trúc TransUNet**, …”

**Cố ý giữ nguyên** ba nghĩa khác cũng viết là “nền” (45 chỗ): `mạng nền` = backbone
ResNet-50 (15 chỗ), `lớp nền` = lớp background của bài toán 9 lớp (17 chỗ),
`nền tảng` / `nền lý thuyết` / `kiến thức nền` (13 chỗ). Hai tên thư mục có thật
`baseline_reproduction` và `notebooks/01-baseline-transunet` trong Phụ lục A cũng giữ,
vì đổi đi thì phụ lục truy vết sẽ sai.

**Hai hình phải vẽ lại vì chữ nằm chết trong ảnh:**
- **Hình 4.1** — vẽ lại bằng `make_metrics_chart.py`, nhãn cột đầu `TransUNet / nền` → `Kiến trúc / TransUNet`.
- **Hình 4.2** — không có dữ liệu gốc để vẽ lại, nên vá thẳng trên PNG bằng
  `fix_hinh_r5.py`: đo nét chữ “Baseline” (125 × 22 px) để dò ra cỡ chữ DejaVu Sans 29px
  đúng như matplotlib đã dùng, rồi ghi đè “TransUNet”. Hai ảnh mới giữ nguyên số điểm ảnh
  nên khung ảnh trong tài liệu không phải chỉnh.

## 7. Bổ sung minh chứng công bố khoa học (mục 5.1)

Đoạn thêm vào cuối mục 5.1 Kết luận, mọi dữ kiện đối chiếu với email xác nhận của
Microsoft CMT và trang <https://www.ic3t.org/>:

> Kết quả của khóa luận đã được viết thành một bài báo khoa học với nhan đề
> “CBAM-TransUNet: A Pre-Patch Attention Model for Pancreas Segmentation in CT Images”,
> với danh sách tác giả gồm Danh Hoàng Hiếu Nghị, Võ Thị Hồng Tuyết (tác giả liên hệ) và
> Nguyễn Thanh Bình. Bài báo được nộp ngày 31 tháng 7 năm 2026 tại Hội nghị quốc tế lần thứ tám
> về Công nghệ Máy tính và Truyền thông (8th International Conference on Computer and
> Communication Technologies – IC3T 2026), tổ chức từ ngày 13 đến ngày 15 tháng 10 năm 2026
> tại Bali, Indonesia; kỷ yếu hội nghị được xuất bản trong loạt Lecture Notes in Networks and
> Systems của Springer và được Scopus lập chỉ mục. Bài báo mang mã số 88 trên hệ thống
> Microsoft CMT của hội nghị và hiện đang trong quá trình phản biện. Thông tin hội nghị được
> công bố tại https://www.ic3t.org/.

Liên kết `https://www.ic3t.org/` là hyperlink ngoài thật nhưng **giữ chữ đen, không gạch chân**,
cùng quy ước với các liên kết `[n]` trong thân bài.

## 8. Ba lỗi bắt được khi kiểm chứng

**8.1 — `[8]` biến thành `ref8` giữa câu.** Lệnh thay chuỗi đầu tiên của tôi trùm qua cụm
`TransUNet [8],`. Trích dẫn `[8]` là một `w:hyperlink` trỏ tới bookmark `ref8`; khi bị xóa rỗng
chữ bên trong, Word tự “sửa” bằng cách điền tên bookmark vào, thành
*“…đối tượng khảo sát,**ref8** giữ lại…”*. Đã tách chuỗi cho khỏi chạm `[8]`, đồng thời
thêm chốt chặn trong `replace_in_el()`: chuỗi cần thay mà trùm qua ranh giới một liên kết
thì script dừng hẳn, không cho chạy tiếp.

**8.2 — Bảng 4.5 gãy chữ `TransUNe / t`.** Cột chỉ rộng 2,14 cm. Lần đầu tôi tính “TransUNet”
theo Times New Roman thường (2,04 cm) nên tưởng vừa, nhưng **dòng tiêu đề bảng in đậm**:
Times New Roman Bold 13 rộng 2,19 cm, cộng lề ô 2 × 0,19 cm thành 2,57 cm. Đã chia lại bảy cột
thành `[1667, 1520, 1060, 900, 1520, 1060, 1060]` twip (tổng vẫn 8787 = 15,5 cm).
Đồng thời thêm tiêu chí mới vào `verify.py`: đo từng từ trong từng ô bằng **đúng phông sẽ in ra**
(đậm cho `BangHeader`, thường cho `BangText`) — 63 cột của 18 bảng đều đủ rộng.

**8.3 — dòng bảng bị cắt đôi qua trang.** Dòng đầu Bảng 4.4 có nhãn “Nhánh 1 –” cùng bốn con số
ở cuối trang 59, phần còn lại “CBAM đa tỷ lệ” sang trang 60 với bốn ô trống. Không dòng bảng nào
trong file đặt `cantSplit`. Đã đặt `cantSplit` cho **176 dòng của 18 bảng**, và thêm `keepNext`
cho style `BangHeader` để dòng tiêu đề không trơ trọi cuối trang rồi lặp lại ở trang sau.
Rà toàn bộ 91 trang: không còn trang nào kết thúc bằng một dòng tiêu đề bảng.

## 9. Hai điểm CHƯA ĐẠT còn lại — đều nằm ở trang bìa sinh viên tự sửa

`verify.py` cho **38/40**. Hai tiêu chí trượt đều thuộc section trang bìa của bản 05/08:

| Tiêu chí | Hướng dẫn Khoa | Section bìa hiện tại | Ba section còn lại |
|---|---|---|---|
| Lề trên / dưới | 3 cm | **2,5 cm** | 3 cm ✔ |
| Header cách mép trên | 2,25 cm | **1,5 cm** | 2,25 cm ✔ |

Ngoài ra **trang bìa chính bị mất dòng “TP. HỒ CHÍ MINH – 08/2026”** (bìa phụ vẫn còn),
và tên trường ở bìa đang dùng dấu nối `-` thay vì gạch ngang `–` như phần còn lại của khóa luận.

Chưa tự sửa ba điểm này vì trang bìa là phần vừa được căn tay: đưa lề về 3 cm sẽ đẩy nội dung
bìa phụ xuống khoảng 28 pt, mà dòng cuối của bìa phụ hiện chỉ còn dư 8 pt trước lề dưới —
nghĩa là phải bỏ bớt một hai dòng trống thì mới không tràn sang trang thứ ba.

---

# Vòng 6 — vẽ lại toàn bộ hình kiến trúc Chương 3 bằng draw.io

Trước vòng này chỉ **Hình 3.3** là hình vẽ thật (`CBAM_TransUNet_architecture_compact.drawio`).
Bốn hình còn lại có vấn đề về nguồn gốc:

| Hình | Trước | Vấn đề |
|---|---|---|
| 3.1 | ảnh 1031×525, ~116 DPI | là ảnh chụp lại **Figure 1 của bài TransUNet** nhưng chú thích không dẫn nguồn |
| 3.4 | ảnh AI 1431×806 | **sai số kênh**: ghi 1/2 = [256,56,56], 1/4 = [512,28,28], 1/8 = [1024,28,28] trong khi mô hình thật là 1/2 = (64,112,112), 1/4 = (256,56,56), 1/8 = (512,28,28) |
| 3.5 | ảnh AI 1431×806 | nhãn tiếng Anh, không khớp Bảng 3.4 |
| 3.6 | ảnh AI 1431×806 | nhãn tiếng Anh, không khớp Bảng 3.4 |

## 10. Năm file .drawio mới

Đặt trong thư mục **`hinh_drawio/`**, mỗi hình một file, kèm sẵn `.pdf` (vector) và
`.png` (300 DPI) đã dựng:

```
hinh_drawio/Hinh_3.1_Kien_truc_TransUNet.drawio
hinh_drawio/Hinh_3.3_CBAM_truoc_buoc_tao_token.drawio
hinh_drawio/Hinh_3.4_CBAM_da_ty_le.drawio
hinh_drawio/Hinh_3.5_RA_nhanh_noi_tat.drawio
hinh_drawio/Hinh_3.6_RA_sau_phep_noi.drawio
```

Sinh bằng `python .fmt_audit/make_drawio.py --png`. Mở và sửa trực tiếp bằng draw.io.

**Năm hình dùng chung một khung xương và chung một hệ tọa độ**, chỉ khác nhau ở cột can
thiệp ở giữa, nên lật qua lại giữa Hình 3.3–3.6 là thấy ngay mô-đun đã dịch chỗ nào.
Bố cục đọc từ trái sang phải: ảnh vào + bộ mã hóa CNN → **can thiệp** → tạo token +
Transformer → bộ giải mã → đầu phân đoạn + ảnh ra + chú giải. Ba đường nối tắt chạy
theo ba làn riêng dưới đáy rồi vòng lên từ bên phải nên không cắt qua cột can thiệp.

Mọi con số lấy đúng theo **Bảng 3.2** (luồng tensor) và **Bảng 3.4** (vị trí chèn):
CNN 1/2 (64,112,112) · 1/4 (256,56,56) · 1/8 (512,28,28) · ẩn 1/16 F (1024,14,14) →
196 token × 768 chiều → 12 khối Transformer → ba phép nối 1024×28×28, 512×56×56,
192×112×112 → đầu phân đoạn 9 lớp. Bảng màu và kiểu nét giữ đúng file gốc của sinh viên.

Mỗi hình có thêm một hộp ghi rõ tham số dòng lệnh của cấu hình
(`attention_mode`, `attention_scales`, `ra_mode`) để đối chiếu thẳng với Bảng 3.3.

## 11. Ba lỗi kỹ thuật gặp khi dựng

**11.1 — XML hỏng làm mất quá nửa sơ đồ.** Thuộc tính `value` của draw.io chứa HTML,
nhưng nó nằm trong một thuộc tính XML nên `<br>`, `<i>` phải được escape. Lần đầu tôi
ghi thẳng HTML thô; bộ phân tích của draw.io vốn dễ dãi nên **không báo lỗi**, chỉ lặng
lẽ bỏ toàn bộ phần sau chỗ hỏng rồi vẫn xuất ra một PNG trông có vẻ bình thường mà thiếu
hẳn khối can thiệp, chú giải và ảnh ra. Đã thêm bước bắt buộc `etree.parse()` sau khi ghi
mỗi file.

**11.2 — `--format png` của draw.io 29.6.6 xuất sai.** Ảnh PNG được dựng ở mức thu phóng
khác rồi cắt theo khung nhỏ hơn, mất khoảng một phần ba bên phải. Bản `--format svg` và
`--format pdf` của cùng file thì đầy đủ. Đã chuyển sang **xuất PDF rồi dựng PNG 300 DPI
bằng PyMuPDF**.

**11.3 — chữ quá nhỏ khi in.** Ở bề rộng 2060 đơn vị in ra khổ 14,82 cm, cỡ chữ 18 chỉ
còn khoảng 3,8 pt trên giấy. Đã phóng toàn bộ cỡ chữ lên 1,45 lần và gọt lại tiêu đề các
khung cho khỏi tràn xuống đè hộp con.

Bộ dựng còn tự kiểm tra **hộp chồng lên nhau** sau mỗi lần sinh; hiện cả năm hình đều sạch.

---

# Vòng 7 — đối chiếu văn phong với bài báo của GVHD

Bài đối chiếu: **Võ Thị Hồng Tuyết, Nguyễn Thanh Bình**, “Cải tiến mạng học sâu GoogLeNet
hỗ trợ phân loại bệnh cao huyết áp trên ảnh võng mạc mắt”, *HUFLIT Journal of Science*.

## 12. Mười quy ước rút từ bài báo

| # | Quy ước | Khóa luận |
|---|---|---|
| 1 | Mở mỗi phần bằng câu nối ngược (“Như đã trình bày ở phần 1…”) | có — mọi mục con đều mở bằng câu nối về mục trước |
| 2 | Chốt mỗi nhóm công trình bằng câu khái quát (“Điểm chung của…”, “Nhìn chung…”) | có — dưới dạng khác: mục 2.5 mở nhóm bằng “điều đáng chú ý là phần lớn chúng không thay đổi bộ trích xuất đặc trưng…”, Bảng 2.4 chốt bằng cột Ưu điểm / Hạn chế / Vấn đề còn tồn đọng |
| 3 | Nêu thẳng nhược điểm của hướng đang bàn | có — 13 chỗ |
| 4 | Giải thích lý do chọn từng thành phần, truy về tính chất dữ liệu | có — ví dụ mục 3.3 truy vị trí đặt CBAM về “biểu diễn cuối cùng còn giữ cấu trúc lưới hai chiều” |
| 5 | Sau công thức: khối “Trong đó:” rồi một câu nói chiều đọc chỉ số | **thiếu 1 chỗ — đã bổ sung** |
| 6 | Sau bảng kết quả: đoạn giải thích cơ chế, không chỉ đọc lại số | có — bốn nhận xét ở mục 4.4, mỗi nhận xét gắn một cơ chế |
| 7 | Thí nghiệm phụ kiểm chứng một lựa chọn thiết kế | có — bốn nhánh đối chứng ở Bảng 3.3 |
| 8 | Nói rõ điều kiện so sánh công bằng | có — mục 4.3 “chỉ để một biến thay đổi”, mục 4.5 nêu giới hạn của phép so sánh với công bố ngoài |
| 9 | Kết luận: hạn chế và hướng mở rộng cụ thể, mỗi hướng gắn một lý do | có — mục 5.2 và 5.3 |
| 10 | Liên từ nhân quả dày | có — 17 chỗ |

## 13. Kết quả rà

Chạy 33 agent: năm agent soát năm chương theo mười quy ước trên, mỗi đề xuất chỉnh sửa
bị một agent khác phản biện với yêu cầu “nghi ngờ thì bác bỏ”.

**28 đề xuất → 27 bị bác bỏ, 1 đứng vững.** Lý do bác bỏ tập trung ở hai nhóm:

- **Khóa luận đã có ý đó, chỉ khác cách diễn đạt** (phần lớn). Ví dụ: đề xuất thêm câu
  chốt nhóm ở mục 2.5 bị bác vì câu mở đầu chính đoạn đó đã nói đúng ý ấy; đề xuất thêm
  câu giải thích cơ chế sau Bảng 4.5 bị bác vì Nhận xét thứ ba ở mục 4.4 đã giải thích
  gần như nguyên văn.
- **Đề xuất đưa vào khẳng định mới không có trong khóa luận**, cần trích dẫn mà đoạn đó
  không có. Ví dụ một đề xuất viết “tuyến tụy bao gồm các vùng giải phẫu có kích thước
  và mức độ biến thiên hình dạng khác nhau” — cụm “vùng giải phẫu” không xuất hiện ở bất
  kỳ chỗ nào trong khóa luận.

**Chỗ duy nhất thiếu thật** — quy ước 5, mục 2.11: bài báo luôn chốt khối “Trong đó:”
bằng một câu nói rõ chiều đọc chỉ số (“Khi đánh giá, ACC càng cao cho thấy phương pháp
đang thử nghiệm cho kết quả phân loại càng chính xác.”). Khóa luận có cột **Chiều tốt**
ở Bảng 2.2 cho cả bốn chỉ số, nhưng riêng Dice thì ngay sau công thức (2.9) chưa có câu
đó. Đã thêm:

> …giá trị Dice nằm trong khoảng từ 0 đến 1 và thường được báo cáo theo phần trăm.
> **Khi đánh giá, Dice càng cao cho thấy dự đoán của mô hình càng trùng khớp với nhãn
> tham chiếu.**

Ba chỉ số còn lại không thêm: Jaccard và recall đã có câu tương đương ở ngay hai dòng kế,
HD95 đã có “càng thấp càng tốt” trong Bảng 2.2 và một đoạn giải thích riêng.

## 14. Một lỗi trong bộ script

Phép thay chữ mới có chuỗi thay thế **chứa nguyên chuỗi bị thay** (thêm một câu vào sau
câu cũ). Hàm `replace_in_el()` dò lại từ đầu đoạn sau mỗi lần thay nên rơi vào **vòng lặp
vô hạn**. Đã sửa: luôn dò tiếp từ sau chỗ vừa thay.

---

# Vòng 8 — vá lại hai trang bìa

## 15. Ba hệ quả của việc căn tay lại trang bìa

Bản 05/08 sinh viên căn tay hai trang bìa, kéo theo:

| Hệ quả | Đã xử lý |
|---|---|
| Lề trên/dưới section bìa tụt còn **2,5 cm** (Khoa yêu cầu 3), header còn **1,5 cm** (yêu cầu 2,25) | trả về 3 / 3 / 2,25 / 2 cm — cả 4 section nay đồng nhất |
| **Bìa chính mất dòng “TP. HỒ CHÍ MINH – 08/2026”**, bìa phụ vẫn còn | nhân bản đúng đoạn của bìa phụ (cùng thụt lề, cùng in đậm, cùng cỡ 14) đặt vào cuối bìa chính |
| Chỗ sang trang giữa bìa chính và bìa phụ **không có ngắt trang tường minh**, chỉ dựa vào số dòng trống | đặt `pageBreakBefore` cho dòng đầu bìa phụ — đổi lề sau này không vỡ bố cục nữa |

Nới lề thêm 1 cm lấy mất chiều cao nên phải cân lại số dòng trống: bỏ **3 dòng** ở bìa
chính và **2 dòng** ở bìa phụ. Sau khi dựng lại, dòng địa danh của bìa chính nằm ở
y = 735 pt và của bìa phụ ở y = 705 pt, đều dưới mốc lề dưới 757 pt — không tràn sang
trang thứ ba, tổng vẫn 90 trang.

**Không sửa dấu nối trong tên trường.** Bìa đang ghi `TRƯỜNG ĐẠI HỌC NGOẠI NGỮ - TIN HỌC
TP. HỒ CHÍ MINH` với dấu nối `-`; mẫu của Khoa (`04 - MẪU HÌNH THỨC KLTN`) cũng dùng dấu
nối chứ không dùng gạch ngang, nên chỗ này vốn không sai.

## 16. Kết quả cuối

`verify.py` **40/40 tiêu chí ĐẠT** — hai tiêu chí lề trước đây trượt nay đã đạt.
Bản draft gốc `(Draft 1 )…` vẫn nguyên vẹn, MD5 `b05641ac…`.

## 17. Vẽ lại năm hình Chương 3 từ chính file draw.io của sinh viên

Vòng trước, năm hình được dựng lại từ đầu bằng một bố cục ngang mới. Bản này làm theo
đúng yêu cầu tiếp theo: **sao nguyên `CBAM_TransUNet_architecture_compact.drawio` rồi chỉ
thêm/bớt thành phần**, nên năm hình dùng chung một bố cục, một bảng màu và một cỡ chữ với
hình mà sinh viên đã tự vẽ.

Bộ dựng: `.fmt_audit/make_drawio.py` — đọc file gốc bằng `lxml`, sửa tại chỗ theo `id`
của từng ô (`drop`, `place`, `shift`, `value`, `sty`, `link`, `points`), rồi ghi ra
`hinh_drawio/`. File gốc của sinh viên **không bị ghi đè** (MD5 `392bf10f…`).

| Hình | Việc đã làm trên bản sao |
|---|---|
| **3.1** Kiến trúc TransUNet | bỏ khung CBAM cùng 4 ô con và 5 cạnh; ô “Refined hidden feature” trở lại thành `Hidden feature F (1024, 14, 14)`, dời lên giữa khoảng trống và canh thẳng cột với Linear Projection |
| **3.3** CBAM trước bước tạo token | **giữ nguyên**, 95/95 ô trùng khớp từng byte với file gốc |
| **3.4** CBAM đa tỷ lệ | thêm `CBAM 1/2`, `CBAM 1/4`, `CBAM 1/8` sau ba tầng nông; đổi khung CBAM thành *Multi-scale CBAM fusion* (`Proj 1×1 + BN + ReLU` → `Weighted mean (learnable α)` → ⊕ với đặc trưng ẩn → `Fused hidden feature h′`); ba nhánh nối tắt đổi nguồn sang ba khối CBAM và dời làn sang phải |
| **3.5** RA trên nhánh nối tắt | chèn `Reverse Attention (skip 1/8)` vào giữa nhánh 1/8 và Concat 1; thêm khung phóng to *Reverse Attention module* ở khoảng trống bên phải, cùng kiểu với khung *Transformer layer detail* vốn có |
| **3.6** RA sau phép nối | nới nhẹ cột giải mã (đẩy Concat 2 lên 20, Concat 1 xuống 16) để lấy chỗ đặt `Reverse Attention (after Concat 1)` đúng giữa Concat 1 và Conv 3×3 (256, 28, 28); cùng khung phóng to như 3.5 |

Nội dung khối chú ý bám theo mã nguồn thật chứ không theo sơ đồ minh họa:
`ResidualAttention2d` (kênh → không gian → cộng phần dư), `CNNFeatureFusion` chế độ
`cnn_fusion` (chiếu 1×1 + BN + ReLU, trung bình có trọng số học được, và **thay luôn đặc
trưng nối tắt** bằng bản đã tinh chỉnh), `ReverseAttentionModule`
(`1 − σ(BN(Conv 3×3 depthwise))` ⊙ đầu vào → bottleneck 1×1–3×3–1×1 → cộng phần dư).

Ba đường về khung hợp nhất ở Hình 3.4 buộc phải cắt qua đường dẫn sang khối CBAM; chỗ cắt
đã bật ký hiệu bắc cầu (`jumpStyle=arc`) để không bị đọc nhầm thành điểm nối.

Xuất ảnh vẫn đi đường **PDF → PyMuPDF 300 DPI**: `--format png` của draw.io 29.6.6 cắt mất
phần bên phải. Năm hình cùng ra `4033 × 3342` px, chèn vào khóa luận ở khổ
`14,82 × 12,28 cm`.

## 18. Đổi nguồn Hình 3.1 và xuất lại ba hình đã chỉnh tay

Sinh viên mở draw.io chỉnh tay ba file `Hinh_3.4`, `Hinh_3.5`, `Hinh_3.6` trong `hinh_drawio/`,
nên **thư mục đó mới là bản gốc**, không phải `make_drawio.py`. Hai thay đổi đi kèm:

**a) Tách khâu xuất ảnh khỏi khâu dựng hình.** Thêm `.fmt_audit/export_drawio.py` — chỉ đọc
`hinh_drawio/*.drawio` rồi xuất PDF → PNG 300 DPI, chạy bao nhiêu lần cũng không đụng vào nội
dung hình. `make_drawio.py` (dựng lại từ đầu, sẽ **đè** mất phần chỉnh tay) nay đòi cờ `--force`
mới chạy.

```bash
python .fmt_audit/export_drawio.py            # xuất tất cả
python .fmt_audit/export_drawio.py 3.4 3.5    # chỉ hình khớp chuỗi
```

**b) Hình 3.1 lấy thẳng từ bài báo gốc.** Vẽ lại kiến trúc TransUNet nguyên bản là thừa, nên
Hình 3.1 dùng đúng Figure 1 của Chen và cộng sự (arXiv:2102.04306 — tài liệu tham khảo **[8]**),
và **dẫn nguồn ngay trong chú thích**:

> *Hình 3.1. Luồng tổng quát của kiến trúc TransUNet dùng trong khóa luận: (a) cấu tạo một khối
> Transformer, (b) bộ mã hóa lai và bộ giải mã có đường nối tắt ở các tỷ lệ 1/2, 1/4 và 1/8.
> Hình lấy từ công trình gốc của Chen và cộng sự [8].*

Số `[8]` dựng thành siêu liên kết nội bộ trỏ tới bookmark `ref8`, chữ đen không gạch chân —
đúng khuôn chú thích Hình 2.1 vốn đã dẫn nguồn CBAM [9]. Hàm mới: `buoc4c_nguon_hinh31()` trong
`revise_r5.py`. Bản draw.io tự vẽ chuyển sang `hinh_drawio/khong_dung_nua/` kèm ghi chú, không xoá.

| Hình | Nguồn ảnh hiện dùng | Khổ in |
|---|---|---|
| 3.1 | `.fmt_audit/fig_transunet_paper.png` — Figure 1 bài báo [8] | 14,82 × 7,55 cm |
| 3.3 | `hinh_drawio/Hinh_3.3_…png` — giữ nguyên, không cần vẽ thêm | 14,82 × 12,28 cm |
| 3.4 · 3.5 · 3.6 | xuất lại từ bản `.drawio` sinh viên đã chỉnh tay | 14,82 × 12,28 cm |

## 19. Thụt dòng hai danh mục và tách ba câu hỏi nghiên cứu thành danh sách

**a) Danh mục bảng và danh mục hình thụt treo.** Chú thích dài hơn một dòng thì dòng sau vẫn
về sát lề trái, nhìn không phân biệt được đâu là mục mới. Đặt thụt treo **1100 twip (1,94 cm)**
ngay trên style `TOC1` — đủ chỗ cho nhãn dài nhất là `Bảng P.1. ` (đo bằng Times New Roman 13
được 1,91 cm). Phải đặt ở style chứ không đặt tay từng đoạn, vì Word dựng lại toàn bộ mục lục
mỗi lần cập nhật trường và xoá sạch định dạng đặt tay.

Mục lục chính cũng dùng `TOC1`, nhưng tiêu đề dài nhất (`DANH MỤC CÁC KÝ HIỆU, CHỮ VIẾT TẮT VÀ
THUẬT NGỮ`) chỉ 12,50 cm nên không bao giờ xuống dòng — thụt treo không đụng gì tới nó.

**b) Ba câu hỏi nghiên cứu ở mục 1.2 thành danh sách đánh số.** Trước đây ba câu nằm chung một
đoạn văn xuôi, người đọc phải tự dò xem câu nào là câu nào; nay tách thành `(i)`, `(ii)`, `(iii)`
với nhãn ở 1 cm và chữ ở 2 cm, mọi dòng sau thẳng cột với chữ. Đối chiếu với phần trả lời ở
Chương 4 và Chương 5 nhờ vậy dễ hơn hẳn.

Hai hàm mới trong `revise_r5.py`: `buoc4d_thut_danh_muc()` và `buoc4e_cau_hoi_nghien_cuu()`.

## 20. Đổi cách làm việc: sửa thẳng trên bản hiện tại

Ngày 06/08 sinh viên tự mở Word chỉnh hai trang bìa — cỡ chữ dòng `KHÓA LUẬN TỐT NGHIỆP` và tên
đề tài lên **18** và **24** (bản gửi ngày 05/08 để 16 và 20, tôi giữ nguyên khi vá lề nên sai
mẫu). Từ đó bản trên đĩa mới là bản gốc, không phải bản dự phòng.

| Chốt chặn | Tác dụng |
|---|---|
| [.fmt_audit/sua_tai_cho.py](.fmt_audit/sua_tai_cho.py) | script mới, đọc và ghi thẳng bản hiện tại, không đụng trang bìa; mỗi bước tự bỏ qua nếu đã làm rồi |
| `revise_r5.py` | tự **dừng** nếu file trên đĩa mới hơn dấu thời gian lần chạy trước, kèm thông báo chỉ sang script mới. Nó phát lại mọi bước từ bản dự phòng nên sẽ xoá mất phần chỉnh tay |
| [.fmt_audit/export_drawio.py](.fmt_audit/export_drawio.py) | chỉ xuất ảnh từ `hinh_drawio/`, không dựng lại hình |

## 21. Bỏ Hình 2.2, bỏ Bảng 3.1 và các sửa kèm theo

| Việc | Kết quả |
|---|---|
| Bỏ **Hình 2.2** (cấu trúc thư mục Synapse) | gỡ cả quan hệ `rId18`, gói docx nhẹ đi 1,27 MB. Không phải đánh số lại vì Chương 2 chỉ còn Hình 2.1 |
| Bỏ **Bảng 3.1** cũ (nguồn cài đặt để truy vết) | bỏ bảng, chú thích, đoạn dẫn; tiêu đề mục 3.1 còn `Định nghĩa bài toán` |
| Đánh số lại | Bảng 3.2→3.1, 3.3→3.2, 3.4→3.3, 3.5→3.4 — **21 chỗ** trong chú thích, thân bài Chương 3 và câu dẫn ở Chương 5 |
| `lai` → `kết hợp` | **22 chỗ**, kể cả tiêu đề mục 2.8 và ô bảng. Chừa `ngoại lai` ở mục HD95 vì chữ đó nghĩa là outlier |
| Đường dẫn kho mã nguồn | đã chèn rồi lại **gỡ bỏ** — xem mục 24 |
| Bỏ `nguồn truy vết` ngoài Chương 3 | mục 4.6 → `Khả năng tái lập`; Phụ lục A → `Tóm tắt tham số dòng lệnh`; Bảng P.1 tương ứng |

**Sửa hệ số hợp nhất đa tỷ lệ cho khớp mã nguồn.** Mục 3.4 đang viết một hệ số α chung khởi tạo
bằng 0, rồi lập luận rằng nhờ vậy mô hình lúc bắt đầu huấn luyện trùng khít với kiến trúc
TransUNet. Đọc `CNNFeatureFusion` trong `networks/vit_seg_modeling.py` thì không phải: mỗi tỷ lệ
có một hệ số riêng (`nn.ParameterDict`), cả ba khởi tạo bằng **1.0**, và ba đóng góp được lấy
**trung bình** chứ không cộng dồn. Công thức (3.2) viết lại thành

> h′ = h + (1/3) · Σ(s∈S) α_s · Proj₁ₓ₁(F̂_s)

cùng khối *trong đó* và đoạn lập luận. Lập luận mới không dựa vào giá trị khởi tạo nữa mà dựa
vào tính chất còn đúng: nhánh hợp nhất chỉ góp thêm một lượng hiệu chỉnh, mạng có thể ép hệ số về
gần 0 để đóng bớt nhánh, mỗi tỷ lệ có hệ số riêng nên phân bổ được mức đóng góp khác nhau.

**Thêm câu dẫn tên hình.** Trước đây chỉ Hình 3.2 được thân bài gọi tên. Nay cả năm hình còn lại
đều có câu dẫn; riêng Hình 3.1 và 3.3 chèn hẳn một đoạn đứng ngay trước hình, nhờ đó lấp luôn
khoảng trắng gần một trang do Hình 3.2 và Hình 3.3 vốn nằm sát nhau không có chữ xen giữa.

## 22. Xếp lại thứ tự hình/bảng cho hết trang trắng

Câu dẫn thêm ở mục trên đẩy khối Hình 3.1 xuống trang sau, để lại 10 cm trắng ở đáy trang 41.
Khối đó cao 290 pt trong khi dưới Bảng 3.1 chỉ còn 287 pt — hụt đúng ba điểm. Rút câu dẫn về một
dòng vẫn không đủ, nên xếp lại thứ tự trình bày ở hai chỗ:

| Chỗ | Thứ tự cũ | Thứ tự mới |
|---|---|---|
| Mục 3.2 | bốn giai đoạn → **Bảng 3.1** → **Hình 3.1** → bàn về Bảng 3.1 | bốn giai đoạn → **Hình 3.1** → **Bảng 3.1** → bàn về Bảng 3.1 |
| Mục 3.3 | Hình 3.2 → **Hình 3.3** → đoạn lập luận | Hình 3.2 → **đoạn lập luận** → Hình 3.3 |

Cả hai đều thuận mạch đọc hơn: sơ đồ tổng quát trước rồi mới tới bảng chi tiết, và đoạn bàn về
bảng nằm ngay sau bảng; ở mục 3.3 thì xem khối CBAM → hiểu vì sao đặt nó ở đó → nhìn nó nằm đâu
trong toàn kiến trúc.

Khoảng trắng ở Chương 3 sau khi xếp lại: chỗ rộng nhất còn **4,6 cm** (trước là 10,1 cm và 8,0 cm).

## 24. Gỡ đường dẫn kho mã nguồn khỏi khóa luận

Kho `MSCAF-TransUNet` đang để riêng tư nên đường dẫn vừa chèn sẽ ra trang 404. Trước khi bật
công khai, quét toàn bộ lịch sử đã đẩy thấy hai chỗ đáng lưu ý:

| Chỗ | Nội dung |
|---|---|
| `notebooks/transunet-drive-data-setup.ipynb` | file ID Google Drive `1BvpY0g9…` trỏ tới `project_TransUNet.zip`; truy cập ẩn danh trả **HTTP 200**, ai có link cũng tải được. Chính `datasets/README.md` của kho ghi rằng muốn lấy bộ Synapse phải đăng ký trên synapse.org — bật công khai là phát tán lại dữ liệu có ràng buộc |
| `scripts/sagemaker_run.py`, `sagemaker_test.py`, `get_results.py`, `delete_s3_output.py` | số tài khoản AWS `879654127886` nằm cứng trong tên bucket và ARN vai trò. Rủi ro thấp — trust policy chỉ cho `sagemaker.amazonaws.com`, không phải dấu sao |

Không có khoá, token hay mật khẩu nào trong lịch sử; không có dữ liệu bệnh nhân; blob lớn nhất
chỉ 0,2 MB; git không theo dõi file khóa luận nào.

**Quyết định: bỏ đường dẫn khỏi khóa luận, giữ kho ở chế độ riêng tư.** Câu cuối mục 3.7 nay là
*"Phụ lục A tóm tắt tham số dòng lệnh của từng cấu hình, cho phép người đọc dựng lại đúng lần chạy
tương ứng."* — Phụ lục A vẫn còn bảng tham số nên khả năng tái lập không mất.

## 25. Bỏ mục 4.6 và chèn minh chứng nộp bài vào Chương 5

**Bỏ mục 4.6 "Khả năng tái lập" cùng Bảng 4.7.** Mục này chỉ có một đoạn và một bảng liệt kê
thành phần artifact — cùng loại nội dung với Bảng 3.1 đã bỏ. Không đoạn nào trong bài trỏ tới
mục 4.6 hay Bảng 4.7 nên bỏ đi không để lại câu hụt. Bảng 4.7 là bảng cuối của Chương 4 nên
không phải đánh số lại bảng nào; chỉ dời hai tiêu đề: `4.7 Hạn chế` → **4.6**, `4.8 Tổng kết
chương` → **4.7**.

**Chèn Hình 5.1 vào cuối mục 5.1.** Đoạn công bố đang khẳng định bài báo đã nộp và đang phản biện
mà không có gì chứng thực. Ảnh chụp thư xác nhận của Microsoft CMT cho thấy đúng mã bài 88, nhan
đề, danh sách ba tác giả và ngày nộp 31/7/2026. Khổ 14,82 × 12,90 cm, kèm câu dẫn ở cuối đoạn.

**Sửa một tiêu chí trong `verify.py`.** Tiêu chí "Chương nào cũng có mục Tổng kết chương" ghim
cứng bộ số hiệu `{1.5, 2.14, 3.8, 4.8}` nên báo trượt oan ngay khi Chương 4 bớt một mục. Đổi
thành soi theo **số chương** — thêm hay bớt mục bất kỳ cũng không làm tiêu chí sai lệch nữa.

## 26. Trang bìa: đường kẻ ngang thay cho gạch chân

Hai trang bìa đang **gạch chân** dòng `KHOA CÔNG NGHỆ THÔNG TIN`. Mẫu của Khoa không gạch chân
chữ mà kẻ một **đường ngang riêng** ngay dưới. Đo trên bản PDF của mẫu (`04 - MẪU HÌNH THỨC
KLTN.docx.pdf`, quét điểm ảnh ở 300 DPI): đường kẻ rộng **5,21 cm**, canh giữa, dày **0,75 pt**.

Đã bỏ gạch chân ở cả bốn chỗ (`w:u` trong `rPr` của đoạn và của run, hai trang bìa) và kẻ hai
đường ngang 5,20 cm, dày 0,75 pt.

Không chèn đoạn mới mà đặt viền dưới cho **đúng dòng trống có sẵn** ngay sau tên khoa, nên chiều
cao trang bìa không đổi một dòng nào — phần căn chỉnh tay của sinh viên giữ nguyên, vẫn đúng
hai trang.

## 27. Gọt văn phong theo đối chiếu với hai bài báo của GVHD

Sinh viên nêu nhận xét: *"sao có mấy từ cứ không có thật sự ý nghĩa"* sau khi đọc lại bài báo
của cô Tuyết. Đối chiếu định lượng thân bài (23.484 từ) với hai bài báo của cô (mỗi bài ~4.850
từ, cùng phong cách HUFLIT Journal of Science) cho thấy khóa luận dùng dày đặc một nhóm cụm từ
mà cô gần như không dùng: `một cách` 17 lần (cô: 0), `gần như` 9 (0), `đáng kể` 7 (0), `nói cách
khác` 7 (0), `thực sự` 6 (0), `tương đối` 5 (0), `rất` 27 lần so với 1 lần trong 4.850 từ của cô.

**Mười hai luật áp dụng**, soạn và kiểm bởi các đợt agent riêng biệt rồi gộp lại:

1. `khóa luận` làm chủ ngữ → câu bị động, hoặc `chúng tôi` khi bị động gượng (theo đúng cách cô
   viết: *"chúng tôi đề xuất…"*, *"phương pháp đề xuất được thử nghiệm…"*). Giữ nguyên khi
   `khóa luận` là tân ngữ/bổ ngữ (`trong khóa luận`, `phạm vi của khóa luận`).
2. Bỏ chuỗi liệt kê `Thứ nhất… Thứ hai… Thứ ba…`, nối lại tự nhiên.
3. Bỏ ngoặc kép nhấn giọng `"…"`, giữ khi dẫn nguyên văn tên dòng dữ liệu hay nhan đề.
4. Bỏ `Vì vậy / Do đó / Chính vì vậy` đứng đầu câu.
5. Bỏ cụm gạch ngang chen giữa câu (`– … –`).
6. Bỏ `Nói cách khác`.
7. Bỏ `cần nói rõ / cần nhấn mạnh / cần lưu ý / đáng chú ý`.
8. Bỏ câu dẫn bố cục rỗng (`Mục sau trình bày…`).
9. Bỏ câu hỏi tu từ — **trừ ba câu hỏi nghiên cứu ở mục 1.2** (`(i)/(ii)/(iii)`), giữ nguyên vì
   đó là câu hỏi nghiên cứu thật.
10. Bỏ chữ định tính rỗng (`đáng kể`, `rất`, `gần như`, `tương đối`, `thực sự`, `một cách` +
    tính từ). Giữ `một cách chia dữ liệu` (danh từ), `vị trí tương đối` (thuật ngữ hình học),
    `vị trí quan trọng hơn quy mô` (mệnh đề so sánh có nội dung).
11. Chẻ câu dài hơn 45 từ.
12. Bỏ nhân cách hóa mô hình (`mô hình quyết định nên nhìn cái gì`).

**Quy trình kỹ thuật:** chia thân bài Chương 1–5 thành các phần nhỏ, mỗi phần một agent soạn cặp
`chuỗi cũ → chuỗi mới`, một agent khác kiểm duyệt độc lập (khắt khe: loại bỏ nếu chuỗi cũ không
khớp nguyên văn, chứa `[`/`]`, hoặc câu mới đổi nghĩa). Ba chốt chặn kỹ thuật khi áp:
chuỗi cũ phải khớp nguyên văn đúng đoạn; không được chứa dấu ngoặc vuông (tránh phá liên kết
trích dẫn `[n]`); `replace_in_el` tự dừng nếu chuỗi trùm qua ranh giới một liên kết.

**Kết quả:** 208 cặp áp sạch, 0 lỗi, 0 cặp chạm trích dẫn.

| Hạng mục | Trước | Sau |
|---|---|---|
| `khóa luận` đứng đầu mệnh đề | 26 | 1 |
| `Thứ nhất/hai/ba/tư` | 23 | 0 |
| Ngoặc kép nhấn giọng | 28 | 9 |
| `Nói cách khác` | 7 | 0 |
| `cần nói rõ/nhấn mạnh/lưu ý` | 7 | 0 |
| `rất` | 27 | 4 |
| `một cách` | 17 | 4 |
| Câu dài hơn 45 từ | 134 | 100 |

5 dấu `?` còn lại đều thuộc ba câu hỏi nghiên cứu mục 1.2 — đúng ngoại lệ, không sót câu hỏi tu
từ nào. Kiểm PDF thật: không còn bookmark hỏng kiểu `refN`, 233 trích dẫn nguyên vẹn, công thức
và khối "trong đó:" không bị xáo trộn.

## 28. Từ viết tắt dùng trước khi giải thích, và rà chính tả

Sinh viên đổi tên file làm việc thành `(Draft 07082026)` và yêu cầu đảm bảo mọi từ viết tắt
được bung đầy đủ ở lần dùng đầu tiên, theo đúng mẫu đã có sẵn trong bài: *"chụp cắt lớp vi tính
(Computed Tomography – CT)"*.

**Quét toàn bộ thân bài** (không dựa vào bảng Danh mục viết tắt theo yêu cầu): bắt mọi cụm 2+
ký tự hoa liên tiếp, xác định lần xuất hiện đầu tiên của mỗi cụm, rồi tự đọc từng ngữ cảnh để
phân loại — vì phần lớn "?" ban đầu là nhiễu: tên mô hình khác chỉ cần trích dẫn `[n]` (UNETR,
SETR, FMD-TransUNet), ký hiệu công thức đã có khối "trong đó:" riêng (TP, FN, QKT), hay tên
thương hiệu (NVIDIA, CUDA, Microsoft CMT).

**Lỗi thật tìm được — bốn chỗ:**

| Từ | Vấn đề | Sửa |
|---|---|---|
| `ResNet` | dùng ở mục 1.3 (`ResNet-50 [11]`) **trước khi** được giải thích ở mục 2.4 | thêm `(Residual Network)` ngay tại mục 1.3 |
| `CLAHE` | chưa giải thích ở lần dùng duy nhất (mục 4.1) | thêm `(Contrast Limited Adaptive Histogram Equalization)` |
| `NIfTI` | chưa giải thích ở lần dùng duy nhất (mục 4.2) | thêm `(Neuroimaging Informatics Technology Initiative)` |
| `MICCAI` | chưa giải thích ở lần dùng duy nhất (mục 4.1) | thêm `(Medical Image Computing and Computer-Assisted Intervention)` |

**Rà chính tả** bằng 9 agent đọc kỹ từng phần thân bài, một agent kiểm duyệt độc lập mỗi phần —
chỉ tìm được **một lỗi thật**: khoảng trắng kép ở mục 3.7 (`điều  kiện` → `điều kiện`). Phần lớn
báo cáo ban đầu bị loại vì không phải lỗi thật, cho thấy bài đã khá sạch sau các vòng sửa trước.

Cả 5 cặp đã kiểm chứng trên PDF thật (nối lại toàn văn để không bỏ sót do ngắt dòng giữa trang).

## 29. Đổi "cơ chế chú ý" → Attention, "tự chú ý"/"chú ý ngược" → self-attention/reverse attention

Sinh viên nhận xét cụm tiếng Việt "cơ chế chú ý" nghe kỳ, muốn dùng thẳng thuật ngữ tiếng Anh —
rồi mở rộng luôn sang "tự chú ý" (self-attention) và "chú ý ngược" (reverse attention), áp dụng
cùng nguyên tắc "giải thích đầy đủ tại lần dùng đầu tiên" đã dùng cho các từ viết tắt khác.

**Phạm vi:** chỉ đổi trong thân bài. **Giữ nguyên bảng Danh mục viết tắt** ở đầu sách — đó là
bảng tra cứu, cột "Ý nghĩa tiếng Việt" của các mục `Attention`, `MSA`, `RA`, `Self-attention`
chính là chỗ cần giữ nguyên tiếng Việt làm định nghĩa. Cũng không đụng "cơ chế tự chú ý" khi đó
là *self-attention* (khái niệm khác với attention nói chung).

| Cụm cũ | Cụm mới | Số chỗ | Nơi giữ nguyên làm định nghĩa |
|---|---|---|---|
| `cơ chế chú ý` | `attention` | 12 | mục 1.1 (đoạn đầu): `cơ chế chú ý (attention)` |
| `tự chú ý` | `self-attention` | 9 | mục 1.1: `self-attention (tự chú ý)` |
| `chú ý ngược` | `reverse attention` | 30 (25 thân bài + 5 trong Bảng 3.1/3.4) | mục 1.2, câu hỏi nghiên cứu (ii): `reverse attention (chú ý ngược)` |

**Bỏ sót ban đầu:** lượt đổi `chú ý ngược` đầu tiên chỉ quét `doc.paragraphs` (thân bài dạng văn
xuôi), bỏ sót 5 ô nằm trong Bảng 3.1 ("Năm cấu hình được khảo sát") và Bảng 3.4 ("Vị trí chèn
mô-đun chú ý"). Phát hiện bằng cách quét lại toàn văn PDF, đối chiếu số lần xuất hiện còn lại có
đúng bằng "định nghĩa + bảng danh mục" hay không. Viết `.fmt_audit/sua_bang_reverse.py` xử lý
riêng vì các script trước không đụng tới nội dung trong ô bảng.

Cả 47 chỗ đã kiểm chứng trên PDF thật (nối toàn văn, không bỏ sót do ngắt dòng giữa trang).

## 30. Lỗi bảng Phụ lục A — chưa xử lý, chờ quyết định

`verify.py` phát hiện Bảng P.1 (Phụ lục A, "Tóm tắt tham số dòng lệnh") có 4 ô cột 1 tràn khổ vì
chứa tên run kỹ thuật dài không có khoảng trắng để ngắt dòng: `baseline_reproduction`,
`mscaf_cnn_fusion_3scale`, `pre_hidden_1_16_r16_run_03`, `reverse_attention_s0_r4_run_01`.

Đây **không liên quan** tới vòng đổi thuật ngữ vừa làm — Phụ lục A không nằm trong phạm vi sửa.
Chưa tự ý xử lý vì cần đổi cấu trúc bảng (nới cột, chèn điểm ngắt, hoặc rút gọn tên run), ngoài
phạm vi yêu cầu hiện tại.

## 32. Đổi toàn bộ "chú ý" còn lại — cơ chế attention / tầng attention

Sau vòng 29, thân bài vẫn còn ~42 chỗ dùng "chú ý" ở các cụm ghép chưa đụng tới: "chú ý theo
kênh/không gian" (channel/spatial attention), "mô-đun chú ý", "khối chú ý", "nhánh chú ý",
"bản đồ chú ý". Sinh viên tự tay sửa mẫu tại một câu ("chú ý theo kênh" → "tầng attention theo
kênh") trong lúc xem file; tôi lấy đó làm chuẩn áp dụng nhất quán cho toàn bộ phần còn lại:

| Ngữ cảnh | Quy tắc | Ví dụ |
|---|---|---|
| Cụm đứng riêng, không có từ phân loại đi kèm | `chú ý theo kênh/không gian` → `tầng attention theo kênh/không gian` | mục 2.6, 3.3, 3.6, 4.7 |
| Đã có từ phân loại đi trước (`mô-đun`, `khối`, `nhánh`, `bản đồ`, `cổng`) | chỉ đổi `chú ý` → `attention` | `mô-đun chú ý` → `mô-đun attention`, `nhánh chú ý kênh` → `nhánh attention kênh` |
| Nói khái niệm chung, không thành phần cụ thể | `chú ý` → `cơ chế attention` | "kiến trúc TransUNet không có chú ý" → "...không có cơ chế attention" |
| Động từ ("chú ý vào") | **giữ nguyên** | "mạng chú ý vào phần bù" — không phải thuật ngữ, không đổi |

31 chỗ trong thân bài (script `.fmt_audit/ap_ban_sua.py`) + 2 ô bảng (Bảng 3.4 mục 4, Bảng 4.6
dòng Att-UNet — mở rộng `.fmt_audit/sua_bang_reverse.py`) đã áp sạch. Còn lại đúng 13 chỗ trên
PDF: 9 dòng trong bảng Danh mục viết tắt (giữ nguyên làm định nghĩa) + 3 chỗ định nghĩa tại lần
dùng đầu tiên (`self-attention (tự chú ý)`, `cơ chế chú ý (attention)`, `reverse attention (chú
ý ngược)`) + 1 động từ. Kiểm chứng bằng cách đếm lại toàn văn PDF, khớp đúng con số kỳ vọng.

**Sự cố xuất PDF (2 lần):** Word báo "read-only" khi `ExportAsFixedFormat` — không phải do file
`.docx`, mà do **Foxit PDF Reader** đang mở sẵn bản PDF cũ, khoá file đích. Đóng tiến trình Foxit
(an toàn, chỉ là trình xem, không mất dữ liệu) rồi xuất lại thành công cả hai lần.

## 34. "Mạng nền" → mạng trích xuất đặc trưng / mạng cơ sở; "mặt nạ" → phân đoạn (đoạn định nghĩa)

Sinh viên chỉ ra "mạng nền" là dịch của *backbone network*, và "nền" ở đây nghĩa nền tảng/cơ sở
— khác hẳn "lớp nền" (background) đang dùng trong bài, hai nghĩa "nền" khác nhau đụng vào cùng
một từ là điều đáng ngại. Đối chiếu với bài báo của GVHD, đề xuất chia hai nhóm:

| Ngữ cảnh | Thay bằng | Số chỗ |
|---|---|---|
| Đứng riêng, mô tả chức năng | `mạng trích xuất đặc trưng` | 11 |
| Liệt kê nhanh trong câu liệt kê yếu tố cố định (đoạn 183, 476, 496) | `mạng cơ sở` (ngắn, giữ nhịp câu liệt kê thuần Việt) | 3 |

Riêng đoạn định nghĩa bài toán ở mục 3.1 (*"cần dự đoán một mặt nạ gán cho mỗi điểm ảnh…"*), đổi
sang lối viết bằng lời như bài báo của cô hay dùng — bỏ hẳn "mặt nạ", dùng "phân đoạn" làm động
từ chính: *"cần phân đoạn mỗi điểm ảnh thành một trong chín lớp gồm nền và tám cơ quan."*
**Giữ nguyên "mặt nạ" ở mục 2.2** (định nghĩa hình thức bằng công thức toán, cần nói rõ ŷ là một
tensor rời rạc) — đúng như đã thống nhất trước đó.

Toàn bộ 15 cặp áp sạch (script `.fmt_audit/ap_ban_sua.py`), không sót `mạng nền` nào; `lớp nền`
và `nền tảng` không bị đụng nhầm; đoạn công thức mục 2.2 vẫn nguyên "mặt nạ".

**Sự cố Foxit lặp lại lần thứ ba:** lần này `Get-Process` không hiện tiêu đề cửa sổ (Foxit chạy
nền, không có cửa sổ active) nên phải dò qua tên tiến trình mới phát hiện. Đóng xong xuất PDF
thành công.

## 35. Kết quả cuối

`verify.py` **39/40 tiêu chí ĐẠT** (1 tiêu chí treo ở Bảng P.1, xem mục 30 — chưa xử lý), PDF
**90 trang**, 28.685 từ. File làm việc: `(Draft 07082026) KLTN - Danh Hoàng Hiếu Nghị - K29.docx`.
10 hình (2.1 · 3.1–3.6 · 4.1 · 4.2 · 5.1) và 15 bảng, số hiệu liên tục trong từng chương.
Bản draft gốc `(Draft 1 )…` vẫn nguyên vẹn, MD5 `b05641ac…`.


