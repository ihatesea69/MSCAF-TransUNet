# Báo cáo format Khóa luận tốt nghiệp — HUFLIT K29

**Sinh viên:** Danh Hoàng Hiếu Nghị – 23DH112270
**Đề tài:** Phân đoạn ảnh tuyến tụy trên cơ chế Attention
**Chuẩn áp dụng:** `ref/04 - MẪU HÌNH THỨC KLTN.docx` (đối chiếu thêm với `ref/Example KLTN khóa trước.docx`)
**Ngày thực hiện:** 03/08/2026

---

## 1. File bàn giao

| File | Mô tả |
|---|---|
| `KLTN - Danh Hoàng Hiếu Nghị - K29 (Formatted).docx` | Bản đã format **và đã hợp nhất nội dung bài báo**, **72 trang**, mục lục đã dựng sẵn |
| `KLTN - Danh Hoàng Hiếu Nghị - K29 (Formatted).pdf` | Bản PDF xuất từ Word (dùng để kiểm tra / nộp file) |
| `(Draft 1 ) Khóa Luận Tốt Nghiệp HUFLIT -K29- ....docx` | **Bản gốc — giữ nguyên, không bị sửa** |
| `.fmt_audit/` | Script hợp nhất + format + kiểm tra, nhật ký thay đổi (để chạy lại nếu cần) |

Bản gốc 59 trang → 64 trang sau khi format → **72 trang** sau khi hợp nhất nội dung bài báo.
Quy mô hiện tại: 21.852 từ, **17 bảng**, **10 hình**, 13 công thức, **22 tài liệu tham khảo**.

Chuỗi xử lý gồm ba bước, chạy lại được bất cứ lúc nào:

```bash
python .fmt_audit/make_metrics_chart.py && python .fmt_audit/merge_paper.py && python .fmt_audit/fmt_kltn.py && python .fmt_audit/update_fields.py && python .fmt_audit/verify.py
```

---

## 2. Đối chiếu từng yêu cầu của hướng dẫn — **23/23 ĐẠT**

| # | Yêu cầu (mục trong HD) | Kết quả | Bằng chứng |
|---|---|---|---|
| 1 | Khổ giấy A4 210 × 297 mm (3.2) | ĐẠT | 21,0 × 29,7 cm |
| 2 | Lề trên 3 cm, dưới 3 cm, trái 3,5 cm, phải 2 cm (3.2) | ĐẠT | cả 3 section |
| 3 | Header cách mép biên trên 2,25 cm (3.3) | ĐẠT | 2,25 cm |
| 4 | Nội dung Times New Roman cỡ 13 (3.1) | ĐẠT | style `Normal` |
| 5 | Giãn dòng 1,5 (3.2) | ĐẠT | `w:line=360` |
| 6 | Canh đều hai bên | ĐẠT | `jc=both` |
| 7 | Chương/mục Times New Roman cỡ 14 (3.1) | ĐẠT | Heading 1 & 2 = TNR 14 đậm |
| 8 | Header: tên chương, TNR 11, dóng lề trái, một dòng (3.3) | ĐẠT | field `STYLEREF 1` |
| 9 | Footnote TNR 11 (3.4) | ĐẠT | style `FootnoteText` |
| 10 | Số trang đặt giữa, phía dưới mỗi trang (3.2) | ĐẠT | field `PAGE`, canh giữa, TNR 11 |
| 11 | Không còn font theme (Calibri Light) | ĐẠT | không style đang dùng nào còn theme-font |
| 12 | Đánh số trang: bìa không số, phần đầu La Mã, thân bài Ả Rập từ 1 | ĐẠT | S1 không số / S2 `i` / S3 `1` |
| 13 | Bìa không có số trang | ĐẠT | footer section 1 trống |
| 14 | Bố cục phần đầu đúng thứ tự (3) | ĐẠT | Lời cảm ơn → Lời cam đoan → Mục lục → Danh mục ký hiệu → Danh mục bảng → Danh mục hình |
| 15 | Có trang bìa phụ in theo mẫu bìa chính (2.1) | ĐẠT | trang 2 giống hệt trang 1 |
| 16 | Mục lục + Danh mục bảng + Danh mục hình có số trang | ĐẠT | 3 field TOC tự sinh, có dấu chấm dẫn |
| 17 | Bảng đúng khổ chữ, lặp dòng tiêu đề khi sang trang | ĐẠT | 17/17 bảng |
| 18 | Đánh số bảng tăng dần theo thứ tự xuất hiện (3.2) | ĐẠT | 0.1 → 2.1 … 2.4 → 3.1 … 3.4 → 4.1 … 4.7 → P.1 |
| 19 | Đánh số hình tăng dần theo thứ tự xuất hiện (3.2) | ĐẠT | 2.1 → 2.2 → 3.1 … 3.6 → 4.1 → 4.2 |
| 20 | Trích dẫn IEEE: số TLTK theo thứ tự xuất hiện (4.i) | ĐẠT | thứ tự xuất hiện = 1…22 liên tục, kể cả trích dẫn trong ô bảng |
| 21 | Danh mục TLTK xếp theo số thứ tự đã chú dẫn (4.i) | ĐẠT | [1]…[22] |
| 22 | Không còn đoạn dùng style lẫn lộn | ĐẠT | thân bài chỉ dùng Body Text / First Paragraph |
| 23 | Trang bìa đúng cỡ chữ mẫu (mục 1) | ĐẠT | 14 / 18 / 24 / 14 / 14 pt |

Chạy lại kiểm tra bất cứ lúc nào:

```bash
python .fmt_audit/verify.py
```

---

## 3. Những lỗi đã sửa

### 3.1 Lỗi hình thức nghiêm trọng

| Lỗi | Trước | Sau |
|---|---|---|
| Style `Heading 1/2/3` dùng font theme + màu xanh accent | Calibri Light, xanh `#4F81BD`, 16 pt | Times New Roman 14 pt đậm, màu đen |
| Thiếu trang bìa phụ (HD bắt buộc) | không có | đã thêm, giống hệt bìa chính |
| Cỡ chữ trang bìa sai | 13 / 16 / 18 pt | 14 / 18 / 24 pt đúng mẫu |
| Lề trên/dưới | 2,5 cm | 3,0 cm |
| Header | tên đề tài, in nghiêng, **canh phải**, cách mép 1,25 cm | **tên chương**, TNR 11, **canh trái**, cách mép 2,25 cm, có viền dưới |
| Mục lục | dòng ghi chú "Bảng mục lục sẽ hiện ở đây…" | mục lục thật, 2 cấp, có số trang + chấm dẫn |
| Danh mục bảng / hình | danh sách gõ tay, **không có số trang** | field TOC tự sinh kèm số trang |
| Đánh số trang phần đầu | không tách được (file chỉ có 1 section) | chia 3 section: bìa không số / La Mã / Ả Rập |
| Lưới cột của bảng | 5 bảng có `tblGrid` rỗng, Word tự đoán độ rộng | 17/17 bảng có lưới hợp lệ, cố định đúng 15,5 cm |
| Bảng dài không lặp dòng tiêu đề | Bảng 0.1 tràn 3 trang, mất tiêu đề | bật `tblHeader` cho cả 13 bảng gốc |

### 3.2 Thay đổi chạm vào con số trong bài (đã được duyệt trước)

**a) Đánh lại số Tài liệu tham khảo theo chuẩn IEEE.** HD mục 4.i quy định *"Số của TLTK là thứ tự xuất hiện của tài liệu trong văn bản"*. Thứ tự cũ là `1, 4, 2, 3, 11, 12, 13, 14, 15, 9, 5, 6, 7, 8, 10, 21, 16, 17, 19, 18, 20` — sai. Ánh xạ đã áp dụng cho **cả `[n]` trong thân bài lẫn danh mục cuối bài**:

| cũ → mới | cũ → mới | cũ → mới |
|---|---|---|
| 1 → 1 | 8 → 14 | 15 → 9 |
| 2 → 3 | 9 → 10 | 16 → 17 |
| 3 → 4 | 10 → 15 | 17 → 18 |
| 4 → 2 | 11 → 5 | 18 → 20 |
| 5 → 11 | 12 → 6 | 19 → 19 |
| 6 → 12 | 13 → 7 | 20 → 21 |
| 7 → 13 | 14 → 8 | 21 → 16 |

Cả 21 tài liệu đều được trích dẫn trong bài, không thừa không thiếu.

**b) Đánh lại số bảng và hình theo thứ tự xuất hiện.** Bản thảo có hai lỗi cùng loại: Hình 3.3 đứng trước Hình 3.2, và Bảng 2.3 / 2.4 đứng trước Bảng 2.2. Thay vì sửa tay, chương trình nay **tự quét toàn tài liệu, đánh lại số theo đúng thứ tự xuất hiện và cập nhật mọi tham chiếu trong văn xuôi**. Nhờ vậy các bảng/hình mới thêm từ bài báo cũng tự vào đúng vị trí trong dãy số. Nếu sau này bạn chèn thêm bảng hay hình, chỉ cần chạy lại là số tự đúng.

### 3.3 Sửa nhỏ

- **2 đoạn văn xuôi bị dính định dạng caption** (canh giữa, in nghiêng, 12 pt) — các câu *"Bảng 4.2 trình bày kết quả…"* và *"Bảng 4.3 trình bày mức chênh lệch…"* — đã trả về định dạng thân bài.
- **11 đoạn dùng style `Normal` lạc** giữa thân bài (rải rác ở mục 3.2, 3.3, 3.7, 4.1, 4.3) → gộp về `Body Text`.
- **46 tiêu đề** bị gõ đè direct formatting → gỡ bỏ để chịu style chung.
- **16 chỗ dùng `-` thay cho gạch ngang** → đổi thành `–`.
- **13 công thức** được canh giữa và đánh số `(2.1)…(2.11)`, `(3.1)`, `(3.2)` canh phải.
- **Đổi tên tiêu đề cho khớp HD:** thêm chữ "CÁC" vào 3 danh mục, và `DANH MỤC HÌNH` → `DANH MỤC CÁC HÌNH VẼ, ĐỒ THỊ`.
- **Đặt ngôn ngữ vi-VN** cho toàn bộ 1135 run — Word sẽ không còn gạch chân đỏ toàn bài.
- **Thêm trang Nhận xét của GVHD** (13 dòng kẻ chấm + khối ký tên).
- **Cắt bỏ tiêu đề tiếng Anh nướng sẵn trong ảnh.** Hình 4.1 và Hình 4.2 còn dính dòng *"Figure 8. Quantitative comparison…"* và *"Figure 9. Qualitative comparison…"* từ bài báo tiếng Anh — vừa trùng caption tiếng Việt bên dưới, vừa mang số hiệu sai. Đã cắt dải tiêu đề đó. (Hình 4.1 sau đó được vẽ lại hoàn toàn, xem mục 3.4.)

---

## 3.4 Hợp nhất nội dung bài báo CBAM-TransUNet vào khóa luận

Nguồn: `CBAM-TransUNet_submit_31072026 (1).docx` (bản LNCS nộp hội nghị, 5 mục, 6 bảng, 5 hình, 22 TLTK).

Nguyên tắc: **chỉ đưa vào phần bài báo CÓ mà khóa luận CHƯA có**, dịch sang tiếng Việt, viết thẳng vào đúng chương/mục liên quan chứ không đính kèm thành phụ lục. Những phần trùng lặp về chữ (kiến trúc tổng quát, giao thức huấn luyện) đã có sẵn trong khóa luận nên bỏ qua. Riêng phần hình được đối chiếu từng cái một — xem bảng bên dưới.

| # | Nội dung bổ sung | Nguồn trong bài báo | Vị trí trong khóa luận |
|---|---|---|---|
| 1 | Sơ đồ chi tiết hai mô-đun chú ý thành phần của CBAM | Fig. 1 | **Hình 2.1**, mục 2.6 |
| 2 | Hai đơn vị đếm của bộ dữ liệu: 2.211 lát cắt, 88–195 lát mỗi ca, trung bình 122,8 | §4.1 | đoạn văn mới, mục 2.12 |
| 3 | CBAM dạng luồng tuần tự kèm kết nối phần dư | Fig. 3 | **Hình 3.2**, mục 3.3 |
| 4 | Số tham số mô hình: 105,28M → 106,46M (+1,1%), bốn biến thể 106,18–107,59M | Table 4, cột #Params | đoạn văn mới ở mục 3.3 **và** mục 4.3 |
| 5 | Vị trí chèn attention theo trình tự bảy giai đoạn pipeline | Table 1 | **Bảng 3.4**, mục 3.6 |
| 6 | Quy trình dữ liệu huấn luyện (theo lát cắt) / kiểm thử (theo khối) | Table 2 | **Bảng 4.2**, mục 4.1 |
| 7 | Kết quả theo từng cơ quan, có ΔDice và ΔHD95 | Table 6 | **Bảng 4.5**, mục 4.3 |
| 8 | **So sánh với các công trình đã công bố** (V-Net, TransUNet, Swin-Unet, Att-UNet) | Table 5 + §4.3 | **mục 4.4 mới** + **Bảng 4.6** |
| 9 | Tài liệu FMD-TransUNet (Lu và cs., 2025) | ref. 22 | **TLTK [22]**, trích dẫn ở mục 4.4 |

### Đối chiếu 5 hình của bài báo

| Hình bài báo | Khóa luận trước đó | Xử lý |
|---|---|---|
| Fig. 1 — hai mô-đun thành phần CBAM | **không có** | thêm mới → **Hình 2.1** |
| Fig. 2 — sơ đồ kiến trúc | có sơ đồ **cũ, khác hẳn** | **thay** bằng sơ đồ mới, dùng bản gốc `CBAM_TransUNet_architecture_compact.png` **4080×3390** thay cho ảnh 789×656 nhúng trong .docx bài báo → **Hình 3.3** |
| Fig. 3 — luồng tuần tự CBAM | **không có** | thêm mới, dùng bản gốc `CBAM_attention.png` **3846×2484** → **Hình 3.2** |
| Fig. 4 — biểu đồ 4 chỉ số | có, nhưng nhãn cũ (`DSC`, `RA on skip`) | **vẽ lại** ở **2938×1763** bằng `make_metrics_chart.py`, dùng đúng nhãn bài báo (`Pancreas Dice`, `lower is better`, `CBAM+RA skip/concat`) → **Hình 4.1** |
| Fig. 5 — kết quả định tính | **đã là đúng hình đó**, bản gốc 3057×1823 | **giữ nguyên** — trùng khít bài báo (cùng ca, cùng lát, cùng Dice) nhưng nét gấp 3,5 lần ảnh 877×515 trong .docx |

Lý do vẽ lại Fig. 4 thay vì chép thẳng: ảnh trong .docx bài báo chỉ 849×514, in ở khổ 15 cm chỉ được ~145 DPI. Bản vẽ lại giữ nguyên cách trình bày và nhãn của bài báo nhưng đạt trên 500 DPI. Số liệu lấy đúng từ Bảng 4.3.

Hệ quả kéo theo, đã xử lý tự động:

- **Mục 4.4 cũ và 4.5 cũ được đổi thành 4.5 và 4.6** để nhường chỗ cho mục So sánh mới.
- **Toàn bộ số hiệu bảng và hình được đánh lại theo thứ tự xuất hiện.** Ví dụ: hình Synapse cũ là Hình 2.1 nay thành Hình 2.2; Bảng 4.2 cũ (kết quả) nay là Bảng 4.3. Mọi tham chiếu trong văn xuôi đã được cập nhật đồng bộ.
- **22 tài liệu tham khảo được đánh lại số theo chuẩn IEEE**, kể cả các trích dẫn nằm **trong ô bảng** (V-Net [19], TransUNet [15], [16], Swin-Unet [8], Att-UNet [4]).
- Bảng nhiều cột tự động hạ xuống cỡ chữ 11 để vừa khổ chữ 15,5 cm mà không bị ngắt giữa từ.

**Một quyết định biên tập cần bạn biết:** bài báo có cột `#Params` ngay trong bảng kết quả. Thêm cột đó vào Bảng 4.3 của khóa luận sẽ thành 8 cột và làm chữ bị ngắt giữa từ (`TransUN / et`). Vì vậy tôi để số tham số ở **hai đoạn văn** — một ở mục 3.3 và một ở mục 4.3 — thay vì thêm cột. Thông tin không mất, chỉ đổi cách trình bày. Nếu bạn vẫn muốn có cột, tôi có thể chuyển bảng đó sang khổ ngang.

---

## 4. Việc bạn cần làm

1. **Mở file .docx bằng Word, nhấn `Ctrl+A` rồi `F9`** trước khi in — để mục lục và số trang khớp tuyệt đối nếu bạn có sửa thêm nội dung. (Hiện tại các mục lục đã được dựng sẵn, mở ra là thấy ngay.)
2. **Kiểm tra lại nội dung 3 mục đã đổi số** (TLTK, hình, bảng) xem có chỗ nào bạn viện dẫn bằng lời mà script chưa bắt được không.
3. **Trang Nhận xét của GVHD** — xác nhận với khoa xem có bắt buộc không; nếu không cần thì xóa trang đó đi (không ảnh hưởng phần còn lại).
4. Ở nhà in: **bìa simili xanh dương, chữ nhũ vàng, gáy ghi tên tác giả + niên khóa, in 01 mặt.** Kèm **Giấy xác nhận đồng ý chia sẻ nội dung KLTN** vào ngay sau tờ bìa lót.
5. **Hạn nộp: trước 16g00 ngày 17/09/2026**, 02 cuốn bìa mạ vàng tại VP Khoa CNTT, lầu 2 khu A (828 Sư Vạn Hạnh).

---

## 5. Điểm cần bạn biết

- **HD tự mâu thuẫn về in 1 mặt / 2 mặt.** Mục 1 ghi *"In nội dung cuốn báo cáo KLTN trên 01 mặt"*, mục 3.2 ghi *"KLTN được in trên hai mặt"*. Đã làm theo **1 mặt** (lề trái 3,5 cm cố định, không mirror margin) — giống bài mẫu K28 đã được hội đồng duyệt. Nếu khoa yêu cầu in 2 mặt, báo lại để đổi sang mirror margins.

- **Lề 3 cm khác bài mẫu K28.** Bài mẫu khóa trước đã được duyệt dùng lề trên/dưới 2,5 cm, nhưng bạn đã chọn bám văn bản HD (3 cm). Hoàn toàn hợp lệ, chỉ khiến bài dài thêm vài trang.

- **Số La Mã bắt đầu từ LỜI CẢM ƠN = i**, nên MỤC LỤC rơi vào trang `iii`. Mẫu mục lục minh họa trong HD ghi "Mục lục … i", tức cách hiểu kia là Lời cảm ơn/Lời cam đoan không đánh số. Tôi chọn cách phổ biến hơn để không có trang nội dung nào bị bỏ trống số. Muốn đổi thì báo, sửa rất nhanh.

- **Công thức dùng font Cambria Math**, không phải Times New Roman. Đây là font toán mặc định của Word và là chuẩn thực tế trong luận văn — Times New Roman không đủ ký tự toán học. HD chỉ quy định font cho "mặt chữ nội dung".

- **Các hình kiến trúc (Hình 3.1–3.5) vẫn có nhãn tiếng Anh bên trong sơ đồ** (Encoder, Decoder, Input CT slice…). Đây là thuật ngữ kỹ thuật trong hình vẽ, không phải caption trùng lặp, nên giữ nguyên. Nếu muốn Việt hóa thì phải vẽ lại hình từ file `.drawio`.

- **Phần lớn hình vẫn chưa được viện dẫn bằng số trong văn xuôi.** Hai hình mới bổ sung (Hình 2.1 và Hình 3.2) đã có câu dẫn, nhưng các hình cũ (Hình 3.1, 3.3–3.6, 4.1, 4.2) mới chỉ có caption chứ chưa có câu kiểu "như Hình 3.4 cho thấy…". Đây là điểm về nội dung chứ không phải hình thức, nhưng hội đồng có thể hỏi — cân nhắc bổ sung vài câu dẫn hình.

- **Bài báo và khóa luận nay là một công trình thống nhất.** Mọi con số trong hai tài liệu đã khớp nhau: Dice 59,23%, HD95 12,97 mm, Jaccard 43,94%, recall 48,94%, 105,28M → 106,46M tham số, Dice trung bình 78,15% và HD95 trung bình 25,59 mm trên tám cơ quan.
