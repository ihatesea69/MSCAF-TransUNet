# -*- coding: utf-8 -*-
"""Nội dung 33 slide bảo vệ khóa luận. Tiện ích dựng hình nằm ở dung_slide.py.

    python slides/noi_dung.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from dung_slide import *          # noqa: F401,F403

# Dựng ngay trên Template.pptx để giữ nguyên theme, master và layout của mẫu.
# Slide mẫu sẽ được xóa ở cuối tệp, sau khi đã sao chép hết phần trang trí.
pr = bo_phong()
SO_SLIDE_MAU = len(pr.slides._sldIdLst)

# ═══════════════════════════════════════════════════════════════════════
#  MỞ ĐẦU
# ═══════════════════════════════════════════════════════════════════════

# ── 1. Bìa ─────────────────────────────────────────────────────────────
# Dùng đúng khung bìa của Template.pptx (logo, dải chân trang, nền trắng),
# chữ đặt theo toạ độ thật của mẫu nên gọi hop_that/ct.
s = moi(pr, khung="bia")
tf = hop_that(s, 3.1, 0.35, 14.3, 0.55)
dat(tf.paragraphs[0], "TRƯỜNG ĐẠI HỌC NGOẠI NGỮ – TIN HỌC TP. HỒ CHÍ MINH",
    cỡ=ct(28), mau=HUFLIT, dam=True, sau=0, canh=PP_ALIGN.CENTER)

tf = hop_that(s, 3.1, 0.98, 15.8, 0.35)
dat(tf.paragraphs[0],
    "HO CHI MINH CITY UNIVERSITY OF FOREIGN LANGUAGES – "
    "INFORMATION TECHNOLOGY",
    cỡ=ct(19), mau=HUFLIT, sau=0, canh=PP_ALIGN.CENTER)

tf = hop_that(s, 1.5, 1.78, 17.4, 0.5)
dat(tf.paragraphs[0], "Khoa Công Nghệ Thông Tin", cỡ=ct(21.5), mau=HUFLIT,
    dam=True, sau=0, canh=PP_ALIGN.CENTER)

tf = hop_that(s, 0, 2.2, 20, 0.9)
dat(tf.paragraphs[0], "KHÓA LUẬN TỐT NGHIỆP", cỡ=ct(38), mau=HUFLIT,
    dam=True, sau=0, canh=PP_ALIGN.CENTER)

tf = hop_that(s, 0, 3.0, 20, 0.9)
dat(tf.paragraphs[0], "CHUYÊN NGÀNH KHOA HỌC MÁY TÍNH", cỡ=ct(38),
    mau=HUFLIT, dam=True, sau=0, canh=PP_ALIGN.CENTER)

# Tên đề tài: dùng màu nhấn đỏ của mẫu
tf = hop_that(s, 0.6, 4.35, 18.8, 2.7, canh=MSO_ANCHOR.MIDDLE)
khoi(tf, [
    [("PHÂN ĐOẠN ẢNH TUYẾN TỤY", True, DO_MAU, ct(60))],
    [("TRÊN CƠ CHẾ ATTENTION", True, DO_MAU, ct(60))],
], gian=1.10, sau=0)
for _p in tf.paragraphs:
    _p.alignment = PP_ALIGN.CENTER

tf = hop_that(s, 0.6, 7.05, 18.8, 0.5)
dat(tf.paragraphs[0],
    "Khảo sát vị trí đặt mô-đun Attention trong kiến trúc TransUNet",
    cỡ=ct(24), mau=HUFLIT, nghieng=True, sau=0, canh=PP_ALIGN.CENTER)

tf = hop_that(s, 1.1, 7.9, 13.0, 2.2)
khoi(tf, [
    [("Giảng viên hướng dẫn:  ", False, HUFLIT, ct(26)),
     ("TS. Võ Thị Hồng Tuyết", True, HUFLIT, ct(26))],
    [("Sinh viên thực hiện:  ", False, HUFLIT, ct(26)),
     ("Danh Hoàng Hiếu Nghị", True, HUFLIT, ct(26)),
     ("  –  MSSV: 23DH112270", False, HUFLIT, ct(26))],
    [("Niên khóa:  ", False, HUFLIT, ct(26)),
     ("K29", True, HUFLIT, ct(26))],
], gian=1.24, sau=4)

tf = hop_that(s, 2.4, 10.8, 15.2, 0.5)
dat(tf.paragraphs[0], "TP.HCM, tháng 8 năm 2026", cỡ=ct(20), mau=TRANG,
    nghieng=True, sau=0, canh=PP_ALIGN.CENTER)

# ── 2. Nội dung trình bày ──────────────────────────────────────────────
s = moi(pr)
nhan_muc(s, "", "NỘI DUNG")
tieu_de(s, "Nội dung trình bày")
for i, (so, ten, mo) in enumerate([
        ("1", "Mở đầu", "Bối cảnh, câu hỏi nghiên cứu, phạm vi và đóng góp"),
        ("2", "Cơ sở lý thuyết",
         "TransUNet, CBAM, Reverse Attention và khoảng trống nghiên cứu"),
        ("3", "Phương pháp đề xuất",
         "Vị trí chèn, bốn nhánh khảo sát, chi phí tham số"),
        ("4", "Thực nghiệm và đánh giá",
         "Kết quả trên bốn chỉ số, phân tích và giới hạn kết luận"),
        ("5", "Kết luận", "Ưu nhược điểm của phương pháp và hướng phát triển")]):
    y = Y_ND + i * 1.03
    chu_nhat(s, LE, y, 0.62, 0.76, to=NAVY, bo_tron=True)
    tf = hop_chu(s, LE, y, 0.62, 0.76, canh=MSO_ANCHOR.MIDDLE)
    dat(tf.paragraphs[0], so, cỡ=24, mau=TRANG, dam=True, sau=0,
        canh=PP_ALIGN.CENTER)
    tf = hop_chu(s, LE + 0.92, y + 0.02, RONG - 1.0, 0.8)
    khoi(tf, [[(ten, True, NAVY, 25)], [(mo, False, XAM, 18)]], sau=2)

# ═══════════════════════════════════════════════════════════════════════
#  CHƯƠNG 1 — MỞ ĐẦU
# ═══════════════════════════════════════════════════════════════════════

# ── 3. Vì sao chọn tuyến tụy ───────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Tuyến tụy nằm trong nhóm cơ quan khó phân đoạn nhất: "
           "Dice chỉ 54% trong khi gan đạt 94%", ch=1)
hinh(s, "moi_1_tam_co_quan.png", LE, Y_ND, 7.1, 4.55)
nhan_cot(s, "Ba khó khăn cộng dồn", 8.05, Y_ND, 4.68)
tf = hop_chu(s, 8.05, Y_ND + 0.48, 4.68, 4.1)
khoi(tf, [
    gach_dau("với mô mềm lân cận, ranh giới mờ  [3]", "Tương phản thấp ", 20),
    gach_dau("về hình dạng và vị trí giữa các ca  [3]", "Biến thiên lớn ", 20),
    gach_dau("chưa tới 1% số điểm ảnh mỗi lát cắt  [4]", "Thể tích nhỏ ", 20),
    [("Chênh 39,97 điểm Dice so với gan, cùng một mô hình, cùng một lần "
      "chạy.", True, DO, 20)],
], cỡ=20, sau=15)
nguon(s, [3, 4], "Số liệu Dice do khóa luận tự đo trên bộ Synapse, "
      "cách chia 18/12 — Bảng 4.5")

# ── 4. Câu hỏi nghiên cứu ──────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Câu hỏi: đặt mô-đun Attention ở đâu trong TransUNet thì có lợi "
           "nhất cho tuyến tụy?", ch=1)
hop_nhan_manh(s, LE, Y_ND, RONG, 1.35, [
    [("Vị trí đặt Attention có phải một biến thiết kế độc lập, "
      "tự nó tạo ra khác biệt hay không?", True, NAVY, 26)]], cỡ=26)
tf = hop_chu(s, LE, Y_ND + 1.72, RONG, 3.3)
khoi(tf, [
    [("(i)  ", True, XANH, 23),
     ("CBAM ngay trước bước tạo token có cải thiện kết quả tuyến tụy so với "
      "kiến trúc TransUNet không?", False, THAN, 23)],
    [("(ii)  ", True, XANH, 23),
     ("So với tinh chỉnh nhiều tầng nông hơn, hoặc thêm reverse attention ở "
      "phía bộ giải mã, phương án này có ưu thế không?", False, THAN, 23)],
    [("(iii)  ", True, XANH, 23),
     ("Khi xét đồng thời độ trùng khớp vùng và sai lệch biên, cấu hình nào "
      "cho hành vi cân bằng nhất?", False, THAN, 23)],
], cỡ=23, sau=18)

# ── 5. Phạm vi và đóng góp (gộp) ──────────────────────────────────────
s = moi(pr)
tieu_de(s, "Phạm vi: một bộ dữ liệu, một giao thức cố định — đủ để trả lời "
           "câu hỏi vị trí một cách công bằng", ch=1)
nhan_cot(s, "Phạm vi", LE, Y_ND, 6.5)
tf = hop_chu(s, LE, Y_ND + 0.48, 6.5, 4.3)
khoi(tf, [
    gach_dau("Synapse [10], 18 ca huấn luyện / 12 ca kiểm thử — đúng cách "
             "chia của [8]", "Dữ liệu:  ", 20),
    gach_dau("theo lát cắt hai chiều, đánh giá ở mức khối ba chiều [8]",
             "Huấn luyện:  ", 20),
    gach_dau("lớp tuyến tụy; bảy cơ quan còn lại chỉ để đặt bối cảnh",
             "Mục tiêu chính:  ", 20),
    gach_dau("không nhằm lập kỷ lục hiệu năng, mà cố định mọi yếu tố ngoài "
             "vị trí can thiệp", "Chủ đích:  ", 20),
], cỡ=20, sau=15)
nhan_cot(s, "Ba đóng góp", 7.5, Y_ND, 5.23)
tf = hop_chu(s, 7.5, Y_ND + 0.48, 5.23, 4.3)
khoi(tf, [
    gach_dau("chỉ ra vì sao điểm nối CNN – Transformer đáng can thiệp",
             "Lý thuyết:  ", 20),
    gach_dau("chèn khối CBAM [9] phần dư trước bước tạo token, kèm bốn nhánh "
             "đối chứng", "Phương pháp:  ", 20),
    gach_dau("dẫn đầu đồng thời độ trùng khớp và sai lệch biên, với +1,1% "
             "tham số", "Thực nghiệm:  ", 20),
], cỡ=20, sau=15)
nguon(s, [8, 9, 10])

# ═══════════════════════════════════════════════════════════════════════
#  CHƯƠNG 2 — CƠ SỞ LÝ THUYẾT
# ═══════════════════════════════════════════════════════════════════════

# ── 7. TransUNet ───────────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "TransUNet ghép CNN với Transformer: CNN giữ chi tiết vị trí, "
           "Transformer nhìn ngữ cảnh toàn cục", ch=2)
hinh(s, "h3_1_transunet.png", LE, Y_ND + 0.15, 7.1, 4.2)
nhan_cot(s, "Vì sao cần cả hai", 8.05, Y_ND, 4.68)
tf = hop_chu(s, 8.05, Y_ND + 0.50, 4.68, 4.4)
khoi(tf, [
    gach_dau("tầm nhìn cục bộ, không thấy quan hệ xa  [6]",
             "CNN đơn thuần: ", 21),
    gach_dau("thấy toàn cục nhưng đánh mất cấu trúc lưới  [12]",
             "ViT đơn thuần: ", 21),
    gach_dau("ghép ResNet-50 [11] với 12 khối Transformer [7], bộ giải mã "
             "CUP và ba nhánh nối tắt  [8]", "TransUNet: ", 21),
], cỡ=21, sau=20)
nguon(s, [6, 7, 8, 11, 12], "Nguồn hình: [8] — Hình 3.1 của khóa luận")

# ── 8. CBAM ────────────────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "CBAM chọn lọc theo kênh rồi theo không gian, chi phí tham số "
           "gần như bằng không", ch=2)
hinh(s, "h3_2_cbam_luong.png", LE, Y_ND + 0.15, 7.1, 4.3)
nhan_cot(s, "Hai bước nối tiếp", 8.05, Y_ND, 4.68)
tf = hop_chu(s, 8.05, Y_ND + 0.50, 4.68, 4.4)
khoi(tf, [
    gach_dau("kênh đặc trưng nào đáng chú trọng — kế thừa SE [25]",
             "Theo kênh: ", 21),
    gach_dau("vùng không gian nào đáng chú trọng  [9]",
             "Theo không gian: ", 21),
    gach_dau("cho phép mạng thoái lui về hành vi ban đầu nếu khối không có "
             "ích  [11]", "Kết nối phần dư: ", 21),
], cỡ=21, sau=22)
nguon(s, [9, 11, 25], "Nguồn cơ chế: [9] — Hình 3.2 của khóa luận")

# ── 9. Reverse Attention ───────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Reverse Attention buộc mô hình học lại đúng phần đang bị bỏ sót "
           "ở rìa đối tượng", ch=2)
hop_nhan_manh(s, LE, Y_ND, RONG, 1.2, [
    [("Nghịch đảo bản đồ dự đoán:   ", False, THAN, 25),
     ("A", True, NAVY, 25), ("ngược", True, NAVY, 16),
     ("  =  1 − σ(A)", True, NAVY, 25),
     ("   rồi nhân ngược vào đặc trưng  [28]", False, THAN, 25)]], cỡ=25)
tf = hop_chu(s, LE, Y_ND + 1.62, RONG, 3.4)
khoi(tf, [
    gach_dau("vùng mô hình đã tự tin bị hạ trọng số, vùng còn do dự được "
             "đẩy lên", "Hệ quả:  ", 23),
    gach_dau("thường là đường viền và các nhánh mảnh — đúng chỗ tuyến tụy "
             "hay bị mất", "Vùng do dự:  ", 23),
    gach_dau("đẩy độ phủ lên cao nhưng có thể làm đường viền xấu đi, sẽ thấy "
             "rõ ở Chương 4  [29]", "Rủi ro:  ", 23),
], cỡ=23, sau=22)
nguon(s, [28, 29])

# ── 10. Khoảng trống ───────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Khoảng trống: các công trình đều can thiệp ở nhánh nối tắt hoặc "
           "bộ giải mã, chưa ai chạm vào điểm nối trước tạo token", ch=2)
tf = hop_chu(s, LE, Y_ND, RONG, 1.9)
khoi(tf, [
    gach_dau("thêm cổng chọn lọc lên đường nối tắt  [19], [23]",
             "Attention U-Net, UCTransNet:  ", 22),
    gach_dau("can thiệp bên trong bộ giải mã  [26], [29]",
             "Các biến thể reverse attention:  ", 22),
], cỡ=22, sau=16)
hop_nhan_manh(s, LE, Y_ND + 1.70, RONG, 1.95, [
    [("Bản đồ đặc trưng ngay trước bước tạo token là biểu diễn cuối cùng "
      "còn hội đủ CẢ HAI tính chất:", False, THAN, 22)],
    [("đã đủ trừu tượng về ngữ nghĩa   ·   vẫn còn nguyên cấu trúc lưới "
      "hai chiều", True, NAVY, 24)]], cỡ=22)
tf = hop_chu(s, LE, Y_ND + 3.76, RONG, 0.9)
dat(tf.paragraphs[0], "Sau bước tạo token, tính chất thứ hai biến mất — đây "
    "là cơ hội cuối cùng để can thiệp theo không gian.",
    cỡ=21, mau=DO, dam=True, sau=0)
nguon(s, [19, 23, 26, 29])

# ═══════════════════════════════════════════════════════════════════════
#  CHƯƠNG 3 — PHƯƠNG PHÁP ĐỀ XUẤT
# ═══════════════════════════════════════════════════════════════════════

# ── 11. Vị trí chèn ────────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Đặc trưng ẩn 1024 × 14 × 14 là biểu diễn cuối cùng còn giữ cấu "
           "trúc lưới hai chiều", ch=3)
hinh(s, "h3_3_dexuat.png", LE, Y_ND - 0.06, 6.4, 4.55)
nhan_cot(s, "Điểm chèn", 7.45, Y_ND, 5.28)
tf = hop_chu(s, 7.45, Y_ND + 0.48, 5.28, 4.1)
khoi(tf, [
    gach_dau("bộ mã hóa ResNet-50 [11] sinh đặc trưng ẩn 1024 × 14 × 14  [8]",
             "Trước:  ", 21),
    gach_dau("một khối CBAM [9] phần dư tinh chỉnh đúng bản đồ này",
             "Chèn:  ", 21),
    gach_dau("chiếu xuống 768 kênh, trải thành 196 token  [8], [12]",
             "Sau:  ", 21),
    [("Khối nằm đúng tại ranh giới giữa mạng tích chập và Transformer.",
      True, NAVY, 20)],
], cỡ=20, sau=14)
nguon(s, [8, 9, 11, 12], "Hình 3.3 của khóa luận — thiết kế của đề tài")

# ── 12. Không xâm lấn ──────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Khối CBAM phần dư bảo toàn hình dạng tensor nên không phải đổi "
           "bất kỳ phần nào còn lại", ch=3)
nhan_cot(s, "Giữ nguyên hoàn toàn", LE, Y_ND, 5.9)
tf = hop_chu(s, LE, Y_ND + 0.50, 5.9, 4.2)
khoi(tf, [
    gach_dau("196", "Số token:  ", 22),
    gach_dau("768", "Số chiều token:  ", 22),
    gach_dau("12", "Số khối Transformer:  ", 22),
    gach_dau("CUP, ba nhánh nối tắt", "Bộ giải mã:  ", 22),
    gach_dau("không đổi một siêu tham số nào", "Giao thức huấn luyện:  ", 22),
], cỡ=22, sau=15)
nguon(s, [8, 9], "Số tham số do khóa luận đếm trực tiếp — Bảng 3.4")
chu_nhat(s, 6.95, Y_ND + 0.1, 5.78, 3.3, to=VANG, vien=VIEN_VANG, day=1.5,
         bo_tron=True)
tf = hop_chu(s, 7.3, Y_ND + 0.42, 5.1, 2.7)
khoi(tf, [[("Cái giá phải trả", True, NAU, 22)],
          [("+1,18", True, NAVY, 44)],
          [("triệu tham số, tức +1,12% so với 105,28 triệu của kiến trúc "
            "TransUNet", False, THAN, 20)]], sau=6)
tf = hop_chu(s, 6.95, Y_ND + 3.65, 5.78, 1.0)
dat(tf.paragraphs[0], "Ghép được vào hệ thống TransUNet đang chạy mà không "
    "phải hiệu chỉnh lại hạ tầng.", cỡ=20, mau=XAM, sau=0)

# ── 13. Ma trận bốn nhánh ──────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Bốn nhánh phủ trọn hai trục nhị phân: trước hay sau bước tạo "
           "token, can thiệp hẹp hay rộng", ch=3)
hinh(s, "moi_3_ma_tran.png", LE, Y_ND, 8.3, 4.9)
tf = hop_chu(s, 9.15, Y_ND + 0.45, 3.58, 4.3)
khoi(tf, [
    [("Vì sao đúng bốn?", True, XANH, 22)],
    [("Hai trục nhị phân cho đúng bốn tổ hợp.", False, THAN, 20)],
    [("Thêm nhánh thứ năm chỉ lặp lại một tổ hợp ở tỷ lệ khác, mà phải trả "
      "giá bằng một lần huấn luyện đầy đủ.", False, THAN, 20)],
    [("Bớt một nhánh sẽ để trống một tổ hợp và làm kết luận về vị trí không "
      "còn đầy đủ.", False, THAN, 20)],
], cỡ=20, sau=15)
nguon(s, [9, 28], "Cách bố trí bốn nhánh là thiết kế của đề tài — Bảng 3.2")

# ── 14. Chi phí tham số ────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Bốn nhánh chênh nhau dưới 1,3% tham số nên chênh lệch kết quả "
           "không đến từ dung lượng mô hình", ch=3)
bang(s, [["Cấu hình", "Tham số (triệu)", "Chênh lệch", "Chênh lệch (%)"],
         ["Kiến trúc TransUNet", "105,28", "—", "—"],
         ["N1 — CBAM đa tỷ lệ", "106,18", "+0,90", "+0,86"],
         ["N2 — CBAM trước bước tạo token", "106,46", "+1,18", "+1,12"],
         ["N3 — CBAM + RA trên nhánh nối tắt", "106,74", "+1,46", "+1,39"],
         ["N4 — CBAM + RA sau phép nối", "107,59", "+2,31", "+2,19"]],
     LE, Y_ND, RONG, cot_w=[4.6, 2.0, 1.7, 1.9], cỡ=19, cao=0.55,
     dam_dong=3)
tf = hop_chu(s, LE, Y_ND + 3.50, RONG, 1.3)
khoi(tf, [
    [("Nhánh đề xuất (dòng tô vàng) không phải nhánh nặng nhất — chỉ đứng "
      "thứ ba về số tham số.", True, NAVY, 20)],
    [("Nhánh nhẹ nhất và nặng nhất chỉ cách nhau 1,41 triệu tham số.",
      False, THAN, 19)]], sau=8)
nguon(s, [8], "Số liệu do khóa luận đếm trực tiếp trên mô hình đã dựng — Bảng 3.4")

# ═══════════════════════════════════════════════════════════════════════
#  CHƯƠNG 4 — THỰC NGHIỆM VÀ ĐÁNH GIÁ
# ═══════════════════════════════════════════════════════════════════════

# ── 15. Giao thức ──────────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Năm cấu hình chạy chung một giao thức: cùng dữ liệu, cùng ngân "
           "sách, cùng cách đo", ch=4)
nhan_cot(s, "Thiết lập", LE, Y_ND, 5.9)
tf = hop_chu(s, LE, Y_ND + 0.50, 5.9, 4.3)
khoi(tf, [
    gach_dau("Synapse [10], 18 ca / 12 ca", "Dữ liệu:  ", 21),
    gach_dau("224 × 224, chín lớp", "Đầu vào:  ", 21),
    gach_dau("150 vòng, hạt giống cố định", "Huấn luyện:  ", 21),
    gach_dau("entropy chéo kết hợp Dice loss", "Hàm mất mát:  ", 21),
    gach_dau("một GPU Tesla T4", "Phần cứng:  ", 21),
], cỡ=21, sau=17)
nhan_cot(s, "Bốn chỉ số, hai nhóm bổ sung nhau", 6.95, Y_ND, 5.78)
tf = hop_chu(s, 6.95, Y_ND + 0.50, 5.78, 4.3)
khoi(tf, [
    [("Trùng khớp vùng", True, NAVY, 21)],
    gach_dau("mức chồng lấn dự đoán ↔ nhãn  [16]", "Dice, Jaccard:  ", 20),
    gach_dau("tỷ lệ phần thật được tìm thấy", "Recall:  ", 20),
    [("Sai lệch biên", True, NAVY, 21)],
    gach_dau("khoảng cách viền, phạt nặng phần lạc chỗ  [16]", "HD95:  ", 20),
], cỡ=20, sau=13)
nguon(s, [10, 16], "Bốn chỉ số đã trình bày ở mục 2.10 và 2.11 của khóa luận")

# ── 16. Kết quả chính ──────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Đặt CBAM trước bước tạo token đạt Dice 59,23% và HD95 12,97 mm — "
           "tốt nhất ở cả hai", ch=4)
bang(s, [["Cấu hình", "Tham số", "Dice ↑", "HD95 ↓", "Jaccard ↑", "Recall ↑"],
         ["Kiến trúc TransUNet", "105,28", "54,37", "15,38", "39,66", "44,41"],
         ["N1 — CBAM đa tỷ lệ", "106,18", "58,93", "13,20", "44,24", "50,22"],
         ["N2 — CBAM trước bước tạo token", "106,46", "59,23", "12,97",
          "43,94", "48,94"],
         ["N3 — CBAM + RA trên nhánh nối tắt", "106,74", "58,32", "32,17",
          "42,95", "52,33"],
         ["N4 — CBAM + RA sau phép nối", "107,59", "55,95", "13,13",
          "40,99", "46,28"]],
     LE, Y_ND, RONG, cot_w=[4.4, 1.5, 1.4, 1.4, 1.6, 1.5], cỡ=18, cao=0.55,
     dam_dong=3)
tf = hop_chu(s, LE, Y_ND + 3.62, RONG, 1.2)
khoi(tf, [
    [("So với kiến trúc TransUNet: +4,86 điểm Dice và giảm 2,41 mm HD95.",
      True, NAVY, 22)],
    [("Dòng tô vàng là cấu hình đề xuất. Dice và Jaccard tính theo phần "
      "trăm, HD95 tính theo milimét.", False, XAM, 18)]], sau=9)
nguon(s, [8, 9], "Số liệu do khóa luận tự đo ở mức khối ba chiều trên 12 ca kiểm thử — Bảng 4.3")

# ── 17. Đánh đổi ───────────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Đây là cấu hình duy nhất dẫn đầu cả hai trục — ba nhánh còn lại "
           "đều phải đánh đổi", ch=4)
hinh(s, "moi_2_danh_doi.png", LE, Y_ND, 7.1, 4.6)
nhan_cot(s, "Đọc hình thế nào", 8.05, Y_ND, 4.68)
tf = hop_chu(s, 8.05, Y_ND + 0.48, 4.68, 4.1)
khoi(tf, [
    [("Đường đứt nét là mốc TransUNet. Vùng vàng là nơi tốt hơn mốc ở cả hai "
      "chỉ số.", False, THAN, 19)],
    gach_dau("nằm sâu nhất trong vùng vàng", "Nhánh đề xuất:  ", 19),
    gach_dau("văng hẳn lên trên, HD95 32,17 mm — gấp gần hai lần rưỡi nhánh "
             "đề xuất", "Nhánh RA nối tắt:  ", 19),
    [("Nếu chỉ nhìn recall thì đã chọn nhầm nhánh này.", True, DO, 19)],
], cỡ=19, sau=12)
nguon(s, [9, 28], "Hình do khóa luận dựng từ số liệu tự đo — Bảng 4.3")

# ── 18. Nhiều tầng không tốt hơn ───────────────────────────────────────
s = moi(pr)
tieu_de(s, "Can thiệp nhiều tầng hơn không đồng nghĩa với tốt hơn: ba tầng "
           "vẫn thua một tầng", ch=4)
bang(s, [["So với kiến trúc TransUNet", "ΔDice", "ΔHD95", "ΔJaccard",
          "ΔRecall"],
         ["N1 — CBAM đa tỷ lệ (ba tầng)", "+4,56", "−2,18", "+4,58", "+5,81"],
         ["N2 — CBAM trước tạo token (một tầng)", "+4,86", "−2,41",
          "+4,28", "+4,53"],
         ["N3 — CBAM + RA trên nhánh nối tắt", "+3,95", "+16,79", "+3,29",
          "+7,92"],
         ["N4 — CBAM + RA sau phép nối", "+1,58", "−2,25", "+1,33", "+1,87"]],
     LE, Y_ND, RONG, cot_w=[5.2, 1.5, 1.7, 1.8, 1.7], cỡ=18, cao=0.58,
     dam_dong=2, do_dong=(3,))
tf = hop_chu(s, LE, Y_ND + 3.30, RONG, 1.6)
khoi(tf, [
    gach_dau("dùng ba tầng đặc trưng, thêm cả nhánh chiếu lẫn hệ số hợp nhất "
             "học được, nhưng vẫn thấp hơn 0,30 điểm Dice.",
             "Nhánh đa tỷ lệ  ", 21),
    [("ΔHD95 mang dấu âm là có lợi. Ô đỏ cho thấy nhánh RA nối tắt làm sai "
      "lệch biên xấu đi 16,79 mm.", False, XAM, 18)],
], cỡ=21, sau=10)
nguon(s, [9, 28], "Số liệu do khóa luận tự đo — Bảng 4.4")

# ── 18b. Trả lời ba câu hỏi nghiên cứu ────────────────────────────────
s = moi(pr)
tieu_de(s, "Ba câu hỏi đặt ra ở đầu bài đều đã có câu trả lời bằng số liệu",
        ch=4)
_qa = [
    ("(i)", "CBAM trước bước tạo token có cải thiện không?", "CÓ",
     "Dice +4,86 điểm và HD95 giảm 2,41 mm so với kiến trúc TransUNet.",
     NAVY),
    ("(ii)", "Có ưu thế hơn đa tỷ lệ và reverse attention không?",
     "CÓ, nhưng cần nói thận trọng",
     "Dẫn đầu ở Dice và HD95; đa tỷ lệ nhỉnh hơn ở Jaccard, RA nối tắt "
     "nhỉnh hơn ở recall.", NAU),
    ("(iii)", "Cấu hình nào cân bằng nhất?", "Nhánh 2 — CBAM trước tạo token",
     "Cấu hình duy nhất dẫn đầu đồng thời cả hai nhóm chỉ số.", NAVY),
]
for k, (so, hoi, dap, vi, mau) in enumerate(_qa):
    y = Y_ND + k * 1.66
    chu_nhat(s, LE, y, RONG, 1.46,
             to=VANG if k == 2 else NHAT,
             vien=VIEN_VANG if k == 2 else RGBColor(0xC8, 0xD6, 0xE5),
             day=1.5 if k == 2 else 1.0, bo_tron=True)
    tf = hop_chu(s, LE + 0.32, y + 0.16, 5.5, 1.2)
    khoi(tf, [[(so + "  ", True, XANH, 21), (hoi, False, THAN, 21)]], sau=0)
    tf = hop_chu(s, 6.4, y + 0.14, 6.05, 1.2)
    khoi(tf, [[("→  " + dap, True, mau, 21)],
              [(vi, False, THAN, 18)]], sau=3)
nguon(s, [8, 9, 28], "Số liệu do khóa luận tự đo — Bảng 4.3 và Bảng 4.4")

# ── 19. Định tính ──────────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Kết quả định tính khớp với số liệu: đường viền tuyến tụy được "
           "khôi phục nhiều hơn", ch=4)
hinh(s, "h4_2_dinh_tinh.png", LE, Y_ND, 7.6, 5.0)
nhan_cot(s, "Quan sát", 8.5, Y_ND, 4.23)
tf = hop_chu(s, 8.5, Y_ND + 0.50, 4.23, 4.4)
khoi(tf, [
    [("Trên các lát cắt được chọn, cấu hình đề xuất khôi phục được nhiều "
      "phần đường viền hơn so với kiến trúc TransUNet.", False, THAN, 20)],
    [("Xu hướng này trùng với hướng mà bốn chỉ số định lượng phản ánh.",
      False, THAN, 20)],
], cỡ=20, sau=16)
nguon(s, [8], "Ảnh dự đoán do khóa luận tự sinh — Hình 4.2")

# ── 20. So sánh công bố ────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Trên cùng cách chia 18/12, Dice tuyến tụy vượt Att-UNet, "
           "Swin-Unet và TransUNet", ch=4)
bang(s, [["Phương pháp", "Kiểu kiến trúc", "Dice tụy ↑", "Dice TB ↑",
          "HD95 TB ↓"],
         ["V-Net [15]", "CNN ba chiều", "40,05", "68,81", "—"],
         ["TransUNet [8], [27]", "Kết hợp CNN – Transformer", "55,86",
          "77,48", "31,69"],
         ["Swin-Unet [22]", "Transformer thuần", "56,58", "79,13", "21,55"],
         ["Att-UNet [19]", "CNN kèm tầng attention", "58,04", "77,77",
          "36,02"],
         ["CBAM-TransUNet — khóa luận", "Kết hợp, CBAM trước tạo token",
          "59,23", "78,15", "25,59"]],
     LE, Y_ND, RONG, cot_w=[3.9, 3.6, 1.6, 1.5, 1.6], cỡ=18, cao=0.52,
     dam_dong=5)
tf = hop_chu(s, LE, Y_ND + 3.40, RONG, 1.0)
khoi(tf, [
    [("Phép so sánh tham chiếu, không phải phép đo lại: ", True, DO, 20),
     ("bốn dòng trên lấy nguyên từ công bố gốc, chỉ dòng cuối do khóa luận "
      "tự chạy.", False, THAN, 20)]], sau=6)
nguon(s, [8, 15, 19, 22, 27])

# ── 21. Giới hạn kết luận ──────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Kết luận chỉ có hiệu lực trong lớp tuyến tụy: gan và động mạch "
           "chủ giảm nhẹ", ch=4)
bang(s, [["Cơ quan", "ΔDice", "ΔHD95 (mm)"],
         ["Lách", "+4,17", "−23,96"],
         ["Tuyến tụy", "+4,86", "−2,41"],
         ["Thận trái", "+4,30", "−15,36"],
         ["Thận phải", "+3,71", "−17,80"],
         ["Dạ dày", "+2,77", "−0,83"],
         ["Túi mật", "+0,53", "−8,32"],
         ["Gan", "−0,55", "+7,45"],
         ["Động mạch chủ", "−0,85", "+8,05"]],
     LE, Y_ND, 6.5, cot_w=[2.6, 1.5, 2.0], cỡ=17, cao=0.44,
     dam_dong=2, do_dong=(7, 8))
nhan_cot(s, "Vì sao chỉ kết luận cho tuyến tụy", 7.5, Y_ND, 5.23)
tf = hop_chu(s, 7.5, Y_ND + 0.50, 5.23, 4.3)
khoi(tf, [
    [("Sáu cơ quan cải thiện, hai cơ quan giảm nhẹ. Bức tranh không đồng "
      "nhất.", False, THAN, 20)],
    [("Vì vậy khóa luận chỉ phát biểu trong phạm vi lớp tuyến tụy và trong "
      "đúng giao thức đã báo cáo.", True, NAVY, 20)],
    [("Mọi kết quả là nghiên cứu kỹ thuật trên dữ liệu công khai, không phải "
      "bằng chứng lâm sàng.", False, DO, 20)],
], cỡ=20, sau=14)
nguon(s, [16], "ΔHD95 mang dấu âm là có lợi. Số liệu do khóa luận tự đo — Bảng 4.5")

# ═══════════════════════════════════════════════════════════════════════
#  CHƯƠNG 5 — KẾT LUẬN
# ═══════════════════════════════════════════════════════════════════════

# ── 22. Ưu / nhược ─────────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Chi phí rất thấp so với lợi ích, nhưng đóng góp từng thành phần "
           "chưa được tách bạch", ch=5)
chu_nhat(s, LE, Y_ND, 5.9, 4.95, to=NHAT, vien=RGBColor(0xC8, 0xD6, 0xE5),
         bo_tron=True)
tf = hop_chu(s, LE + 0.32, Y_ND + 0.28, 5.26, 4.4)
khoi(tf, [
    [("Ưu điểm", True, NAVY, 23)],
    gach_dau("+1,18 triệu tham số đổi lấy +4,86 Dice và −2,41 mm HD95",
             "Chi phí thấp:  ", 19),
    gach_dau("bảo toàn hình dạng tensor, không đổi siêu tham số nào",
             "Không xâm lấn:  ", 19),
    gach_dau("cấu hình duy nhất dẫn đầu cả Dice lẫn HD95", "Cân bằng:  ", 19),
    gach_dau("mạng thoái lui được nếu khối không có ích  [11]",
             "Kết nối phần dư:  ", 19),
], cỡ=19, sau=13)
chu_nhat(s, 6.95, Y_ND, 5.78, 4.95, to=VANG, vien=VIEN_VANG, day=1.5,
         bo_tron=True)
tf = hop_chu(s, 7.27, Y_ND + 0.28, 5.14, 4.4)
khoi(tf, [
    [("Nhược điểm", True, NAU, 23)],
    gach_dau("chưa loại bỏ từng thành phần với tham số cân bằng",
             "Chưa tách bạch:  ", 19),
    gach_dau("gan và động mạch chủ giảm nhẹ", "Lợi ích không đều:  ", 19),
    gach_dau("chưa khai thác quan hệ giữa các lát liên tiếp",
             "Huấn luyện 2D:  ", 19),
    gach_dau("một bộ dữ liệu công khai duy nhất  [10]",
             "Phạm vi hẹp:  ", 19),
], cỡ=19, sau=13)
nguon(s, [10, 11], "Đánh giá của khóa luận, mục 5.2")

# ── 23. Kết luận ───────────────────────────────────────────────────────
s = moi(pr)
tieu_de(s, "Ba kết luận của khóa luận", ch=5)
tf = hop_chu(s, LE, Y_ND, RONG, 3.5)
khoi(tf, [
    [("1.  ", True, XANH, 23),
     ("Vị trí đặt Attention là một biến thiết kế độc lập.  ", True, NAVY, 23),
     ("Điểm nối ngay trước bước tạo token xứng đáng được xem xét riêng.",
      False, THAN, 23)],
    [("2.  ", True, XANH, 23),
     ("Chi phí +1,1% tham số đổi lấy +4,86 điểm Dice và −2,41 mm HD95.",
      True, NAVY, 23),
     ("  Đây là cấu hình duy nhất dẫn đầu đồng thời cả hai nhóm chỉ số.",
      False, THAN, 23)],
    [("3.  ", True, XANH, 23),
     ("Không thể chọn mô hình theo một chỉ số đơn lẻ.  ", True, NAVY, 23),
     ("Nhánh recall cao nhất lại có sai lệch biên tệ nhất.", False, THAN, 23)],
], cỡ=23, sau=16)
hop_nhan_manh(s, LE, Y_ND + 3.62, RONG, 1.02, [
    [("Kết quả đã được viết thành bài báo ", False, THAN, 19),
     ("“CBAM-TransUNet: A Pre-Patch Attention Model for Pancreas "
      "Segmentation in CT Images”", True, NAVY, 19),
     (", nộp tại hội nghị IC3T 2026, mã bài số 88.", False, THAN, 19)]],
    cỡ=19)
tf = hop_chu(s, LE, Y_NGUON + 0.30, RONG, 0.4)
dat(tf.paragraphs[0], "Xin cảm ơn quý Thầy Cô trong hội đồng đã lắng nghe.",
    cỡ=17, mau=XAM, nghieng=True, sau=0)

# ── 24. Tài liệu tham khảo ─────────────────────────────────────────────
s = moi(pr)
nhan_muc(s, "", "TÀI LIỆU THAM KHẢO")
tieu_de(s, "Tài liệu tham khảo")
_ds = [3, 4, 6, 7, 8, 9, 10, 11, 12, 15, 16, 19, 22, 25, 26, 27, 28, 29]
_nua = (len(_ds) + 1) // 2
for _c, _nhom in enumerate((_ds[:_nua], _ds[_nua:])):
    tf = hop_chu(s, LE + _c * 6.15, Y_ND, 5.85, CAO_ND)
    khoi(tf, [TLTK[n] for n in _nhom], cỡ=12, gian=1.12, sau=6)
tf = hop_chu(s, LE, Y_NGUON + 0.40, RONG, 0.32)
dat(tf.paragraphs[0], "Số hiệu giữ đúng như trong khóa luận. Nguồn của từng "
    "luận điểm được ghi ngay dưới chân slide tương ứng.",
    cỡ=12, mau=XAM, sau=0)

# ═══════════════════════════════════════════════════════════════════════
#  PHỤ LỤC — slide dựng sẵn cho phần hỏi đáp
# ═══════════════════════════════════════════════════════════════════════

def phu_luc(nhan, tieu):
    sl = moi(pr)
    nhan_muc(sl, "PL", "PHỤ LỤC")
    nhan_phu_luc(sl, nhan)
    tf_ = hop_chu(sl, LE, Y_TD, RONG, H_TD)
    dat(tf_.paragraphs[0], tieu, cỡ=25 if len(tieu) < 74 else 23, mau=NAVY,
        dam=True, gian=1.14, sau=0)
    chu_nhat(sl, LE, Y_GACH, RONG, 0.018, to=KE)
    return sl

# ── A. Dice 59% có thấp không ──────────────────────────────────────────
s = phu_luc("Phụ lục A", "Dice 59% là cao hay thấp đối với riêng lớp "
                         "tuyến tụy?")
tf = hop_chu(s, LE, Y_ND, RONG, CAO_ND)
khoi(tf, [
    gach_dau("tuyến tụy là lớp có Dice thấp nhất nhì trong tám cơ quan ở mọi "
             "công trình, do tương phản thấp và thể tích nhỏ.  [3], [4]",
             "Bối cảnh:  ", 22),
    gach_dau("V-Net [15] 40,05  ·  TransUNet [8] 55,86  ·  Swin-Unet [22] "
             "56,58  ·  Att-UNet [19] 58,04  ·  khóa luận 59,23.",
             "Trên cùng cách chia:  ", 22),
    gach_dau("con số tuyệt đối phụ thuộc tiền xử lý và hậu xử lý; điều khóa "
             "luận khẳng định là chênh lệch nội bộ giữa năm cấu hình chạy "
             "cùng giao thức.", "Lưu ý:  ", 22),
], cỡ=22, sau=20)
nguon(s, [3, 4, 8, 15, 19, 22])

# ── B. CBAM chi tiết ───────────────────────────────────────────────────
s = phu_luc("Phụ lục B", "Bên trong CBAM: hai mô-đun thành phần")
hinh(s, "h2_1_cbam.png", LE, Y_ND, 6.2, 3.2)
tf = hop_chu(s, 7.1, Y_ND + 0.05, 5.63, CAO_ND)
khoi(tf, [
    gach_dau("gộp theo hai chiều không gian bằng trung bình và cực đại, đưa "
             "qua một perceptron nhiều tầng dùng chung, cộng lại rồi lấy "
             "sigmoid.", "Theo kênh:  ", 20),
    gach_dau("gộp theo chiều kênh bằng trung bình và cực đại, nối lại, đưa "
             "qua một tầng tích chập 7×7 rồi lấy sigmoid.",
             "Theo không gian:  ", 20),
    gach_dau("nhân theo kênh trước, nhân theo không gian sau, cuối cùng cộng "
             "phần dư.", "Thứ tự:  ", 20),
], cỡ=20, sau=16)
nguon(s, [9, 25], "Nguồn hình: [9] — Hình 2.1 của khóa luận")

# ── C. Vì sao chưa ablation ────────────────────────────────────────────
s = phu_luc("Phụ lục C", "Vì sao chưa tách riêng đóng góp của tầng theo kênh "
                         "và tầng theo không gian?")
tf = hop_chu(s, LE, Y_ND, RONG, CAO_ND)
khoi(tf, [
    gach_dau("khóa luận đo hiệu quả của cả khối đặt tại một vị trí, chưa "
             "thực hiện thí nghiệm loại bỏ từng thành phần với số tham số "
             "được cân bằng.", "Thừa nhận:  ", 22),
    gach_dau("câu hỏi nghiên cứu là VỊ TRÍ đặt khối, không phải THÀNH PHẦN "
             "nào trong khối. Mỗi nhánh phải trả giá bằng một lần huấn "
             "luyện đầy đủ 150 vòng.", "Vì sao:  ", 22),
    gach_dau("đây là hướng phát triển thứ nhất đã nêu ở mục 5.3.",
             "Kế tiếp:  ", 22),
], cỡ=22, sau=20)
nguon(s, [9], "Nhận định của khóa luận, mục 4.6 và 5.2")

# ── D. Cấu hình huấn luyện ─────────────────────────────────────────────
s = phu_luc("Phụ lục D", "Cấu hình huấn luyện chi tiết")
bang(s, [["Thành phần", "Giá trị"],
         ["Bộ dữ liệu", "Synapse (BTCV), 18 ca huấn luyện / 12 ca kiểm thử"],
         ["Kích thước đầu vào", "224 × 224, ba kênh nhân bản"],
         ["Kiến trúc gốc", "R50-ViT-B/16, 12 khối Transformer"],
         ["Số vòng huấn luyện", "150"],
         ["Hàm mất mát", "Entropy chéo kết hợp Dice loss"],
         ["Phần cứng", "Một GPU NVIDIA Tesla T4"],
         ["Hạt giống ngẫu nhiên", "Cố định cho cả năm cấu hình"],
         ["Cách đánh giá", "Theo khối ba chiều, ghép từ dự đoán từng lát"]],
     LE, Y_ND, RONG, cot_w=[3.4, 8.0], cỡ=19, cao=0.5)
nguon(s, [8, 10], "Thiết lập do khóa luận cấu hình — Bảng 4.2; tham số "
      "dòng lệnh đầy đủ ở Phụ lục A của khóa luận")

# ── E. Kết quả tám cơ quan ─────────────────────────────────────────────
s = phu_luc("Phụ lục E", "Kết quả đầy đủ trên tám cơ quan")
bang(s, [["Cơ quan", "Dice TransUNet", "Dice đề xuất", "ΔDice",
          "HD95 TransUNet", "HD95 đề xuất", "ΔHD95"],
         ["Động mạch chủ", "87,45", "86,59", "−0,85", "5,37", "13,42", "+8,05"],
         ["Túi mật", "50,32", "50,84", "+0,53", "40,34", "32,02", "−8,32"],
         ["Thận trái", "81,32", "85,62", "+4,30", "49,97", "34,62", "−15,36"],
         ["Thận phải", "78,23", "81,94", "+3,71", "49,34", "31,54", "−17,80"],
         ["Gan", "94,34", "93,79", "−0,55", "25,89", "33,34", "+7,45"],
         ["Tuyến tụy", "54,37", "59,23", "+4,86", "15,38", "12,97", "−2,41"],
         ["Lách", "85,69", "89,86", "+4,17", "53,12", "29,16", "−23,96"],
         ["Dạ dày", "74,54", "77,31", "+2,77", "18,46", "17,62", "−0,83"]],
     LE, Y_ND, RONG, cot_w=[2.6, 1.9, 1.7, 1.3, 1.9, 1.7, 1.4], cỡ=16,
     cao=0.46, dam_dong=6, do_dong=(1, 5))
nguon(s, [16], "ΔHD95 mang dấu âm là có lợi. Hai dòng chữ đỏ là hai cơ quan "
      "giảm. Số liệu do khóa luận tự đo — Bảng 4.5")

# ── F. Vì sao một bộ dữ liệu, vì sao 2D ────────────────────────────────
s = phu_luc("Phụ lục F", "Vì sao chỉ một bộ dữ liệu và vì sao huấn luyện "
                         "theo lát hai chiều?")
tf = hop_chu(s, LE, Y_ND, RONG, CAO_ND)
khoi(tf, [
    gach_dau("Synapse [10] với cách chia 18/12 là thiết lập mà TransUNet [8] "
             "và phần lớn công trình đối chiếu dùng, nên kết quả đặt được "
             "vào bối cảnh chung.", "Một bộ dữ liệu:  ", 22),
    gach_dau("giữ đúng thiết lập của TransUNet để biến duy nhất thay đổi là "
             "vị trí đặt attention; chuyển sang mô hình ba chiều sẽ đổi "
             "nhiều yếu tố cùng lúc.", "Theo lát 2D:  ", 22),
    gach_dau("mở rộng sang bộ dữ liệu tuyến tụy khác [4], và đưa vào một số "
             "lát lân cận thay vì một lát đơn lẻ.", "Hướng tiếp:  ", 22),
], cỡ=22, sau=20)
nguon(s, [4, 8, 10])

# ── G. Hai nhánh reverse attention ─────────────────────────────────────
s = phu_luc("Phụ lục G", "Hai nhánh đối chứng dùng Reverse Attention")
hinh(s, "h3_5_ra_noi_tat.png", LE, Y_ND, 5.85, 4.15)
hinh(s, "h3_6_ra_sau_noi.png", 6.9, Y_ND, 5.85, 4.15)
tf = hop_chu(s, LE, 6.38, 5.85, 0.5)
dat(tf.paragraphs[0], "N3 — RA trên nhánh nối tắt 1/8", cỡ=19, mau=NAVY,
    dam=True, sau=0, canh=PP_ALIGN.CENTER)
tf = hop_chu(s, 6.9, Y_NGUON, 5.85, 0.5)
dat(tf.paragraphs[0], "N4 — RA sau phép nối đầu tiên", cỡ=19, mau=NAVY,
    dam=True, sau=0, canh=PP_ALIGN.CENTER)
nguon(s, [28, 29], "Hai nhánh đối chứng do khóa luận thiết kế — Hình 3.5 "
      "và Hình 3.6")

# ── H. HD95 ────────────────────────────────────────────────────────────
s = phu_luc("Phụ lục H", "HD95 là gì và vì sao phải dùng cùng lúc bốn "
                         "chỉ số?")
tf = hop_chu(s, LE, Y_ND, RONG, CAO_ND)
khoi(tf, [
    gach_dau("phân vị 95 của khoảng cách Hausdorff giữa viền dự đoán và viền "
             "nhãn. Lấy phân vị 95 thay vì cực đại để bớt nhạy với một vài "
             "điểm lạc.  [16]", "HD95:  ", 22),
    gach_dau("Dice và Jaccard đo phần chồng lấn nên bỏ qua hình dạng viền. "
             "Một dự đoán phình ra đúng chỗ vẫn có Dice tốt.  [16]",
             "Vì sao chưa đủ:  ", 22),
    gach_dau("nhánh RA nối tắt có recall cao nhất 52,33% nhưng HD95 32,17 mm. "
             "Chỉ nhìn recall sẽ chọn nhầm.", "Bằng chứng:  ", 22),
], cỡ=22, sau=20)
nguon(s, [16], "Số liệu do khóa luận tự đo — Bảng 4.3")

# ── I. Thư xác nhận IC3T ───────────────────────────────────────────────
s = phu_luc("Phụ lục I", "Xác nhận nộp bài tại hội nghị IC3T 2026")
hinh(s, "h5_1_cmt.jpg", LE, Y_ND, 6.6, 4.2)
tf = hop_chu(s, 7.5, 1.95, 5.23, 4.4)
khoi(tf, [
    [("“CBAM-TransUNet: A Pre-Patch Attention Model for Pancreas "
      "Segmentation in CT Images”", True, NAVY, 21)],
    gach_dau("Danh Hoàng Hiếu Nghị, Võ Thị Hồng Tuyết (tác giả liên hệ), "
             "Nguyễn Thanh Bình", "Tác giả:  ", 20),
    gach_dau("Hội nghị quốc tế lần thứ tám về Công nghệ Máy tính và Truyền "
             "thông (IC3T 2026)", "Nơi nộp:  ", 20),
    gach_dau("31 tháng 7 năm 2026, mã bài số 88", "Ngày nộp:  ", 20),
], cỡ=20, sau=14)
nguon(s, [], "Thư xác nhận của hệ thống Microsoft CMT — Hình 5.1 của "
      "khóa luận")

# ═══════════════════════════════════════════════════════════════════════
#  GHI CHÚ NGƯỜI TRÌNH BÀY  —  ngân sách 20 phút
# ═══════════════════════════════════════════════════════════════════════
GHI_CHU = [
    ("0:00", "Chào hội đồng. Giới thiệu tên, đề tài, giảng viên hướng dẫn. "
             "Nói ngắn, đừng đọc lại slide."),
    ("0:30", "Điểm nhanh năm chương. Nói: “phần trọng tâm là Chương 3 và "
             "Chương 4”."),
    ("1:00", "Mở bài bằng con số. Chỉ vào cột đỏ. Nhấn: cùng một mô hình, "
             "cùng một lần chạy, gan 94 mà tụy chỉ 54. Nếu bị hỏi vì sao túi "
             "mật còn thấp hơn: đúng, túi mật cũng khó, nhưng đề tài chọn "
             "tuyến tụy vì ý nghĩa lâm sàng và vì nó gom đủ ba khó khăn."),
    ("2:30", "Đọc chậm câu trong khung — câu hội đồng cần nghe rõ nhất. Ba "
             "câu hỏi con thì đọc lướt, nói “ba câu này sẽ được trả lời ở "
             "Chương 4” rồi chuyển. Nhớ: có hẳn một slide đóng lại ba câu "
             "hỏi này ở phút 16:30."),
    ("3:45", "Lướt cả hai cột. Nhấn “so sánh nội bộ” — đây là chỗ bảo vệ "
             "tính công bằng của kết luận."),
    ("4:45", "Chỉ vào hình: bên trái CNN, giữa Transformer, phải bộ giải mã. "
             "Không đi vào chi tiết từng tầng."),
    ("5:45", "Hai bước nối tiếp: kênh rồi không gian. Nhấn kết nối phần dư — "
             "nếu khối vô ích thì mạng tự bỏ qua được."),
    ("6:45", "Ngắn thôi. Ý chính: reverse attention ép mô hình nhìn vào chỗ "
             "nó đang do dự. Báo trước rủi ro để nối mạch sang Chương 4."),
    ("7:45", "Slide bản lề. Nói chậm đoạn “cơ hội cuối cùng”. Sau bước tạo "
             "token thì cấu trúc lưới mất, không can thiệp theo không gian "
             "được nữa."),
    ("8:45", "Chỉ đúng vị trí khối CBAM trên hình. Nhắc lại 1024 × 14 × 14."),
    ("10:00", "Nhấn: không phải đổi gì hết. Con số +1,18 triệu là câu trả "
              "lời cho câu hỏi “có tốn kém không”."),
    ("11:00", "Slide trả lời câu “tại sao bốn nhánh”. Hai trục nhị phân cho "
              "đúng bốn tổ hợp — không phải chọn bừa."),
    ("12:00", "Slide phòng thủ. Nói trước khi hội đồng kịp hỏi: chênh lệch "
              "không đến từ việc nhánh nào nhiều tham số hơn."),
    ("12:45", "Lướt nhanh. Nhấn “cùng một giao thức cho cả năm cấu hình”."),
    ("13:30", "Dừng lại ở dòng vàng. Đọc to hai con số 59,23 và 12,97. Rồi "
              "nói mức cải thiện +4,86 và −2,41."),
    ("14:45", "Slide quan trọng nhất. Chỉ vào điểm đỏ ở trên cao. Nói: nếu "
              "chọn theo recall thì đã chọn nhánh này, mà biên của nó tệ gấp "
              "hai lần rưỡi."),
    ("15:45", "Ba tầng thua một tầng. Kết quả phản trực giác, nên nói rõ: "
              "can thiệp nhiều hơn không đồng nghĩa tốt hơn."),
    ("16:30", "Slide đóng vòng lặp. Đọc lần lượt ba câu trả lời, đối chiếu "
              "ngược lại slide phút 2:30. Câu (ii) phải nói đúng chữ “thận "
              "trọng” — đừng khẳng định quá tay, vì đa tỷ lệ vẫn hơn ở "
              "Jaccard và RA nối tắt vẫn hơn ở recall."),
    ("17:30", "Chỉ vào một hai chỗ viền được khôi phục. Đừng mô tả từng ảnh."),
    ("18:00", "Nhấn ngay câu đỏ: đây là tham chiếu, không phải đo lại. Nói "
              "trước để hội đồng không bắt lỗi."),
    ("18:40", "Slide phòng thủ thứ hai. Tự nêu gan và động mạch chủ giảm. "
              "Nhấn: vì vậy chỉ kết luận trong phạm vi tuyến tụy."),
    ("19:15", "Đọc lướt hai cột. Phần nhược điểm nói thẳng, đừng né."),
    ("19:40", "Dừng ở slide này suốt phần hỏi đáp. Đọc ba ý. Nhắc bài báo "
              "IC3T 2026. Kết: “Em xin hết phần trình bày, kính mời quý "
              "Thầy Cô đặt câu hỏi.”"),
    ("—", "Chỉ mở nếu được hỏi nguồn."),
]
PL = ["Mở khi bị hỏi: Dice 59% có thấp không.",
      "Mở khi bị hỏi: CBAM hoạt động thế nào.",
      "Mở khi bị hỏi: sao chưa làm ablation tách thành phần.",
      "Mở khi bị hỏi: cấu hình máy, thời gian huấn luyện.",
      "Mở khi bị hỏi: kết quả các cơ quan khác.",
      "Mở khi bị hỏi: sao chỉ một bộ dữ liệu, sao không dùng 3D.",
      "Mở khi bị hỏi: hai nhánh reverse attention đặt ở đâu.",
      "Mở khi bị hỏi: HD95 là gì, sao cần bốn chỉ số.",
      "Mở khi bị hỏi về bài báo đã nộp ở hội nghị IC3T 2026."]

# Bỏ các slide gốc của Template.pptx, chỉ giữ slide vừa dựng
kt.xoa_slide_dau(pr, SO_SLIDE_MAU)

for i, sl in enumerate(pr.slides):
    if i < len(GHI_CHU):
        moc, txt = GHI_CHU[i]
        nd = f"[{moc}]  {txt}"
    elif i - len(GHI_CHU) < len(PL):
        nd = f"[PHỤ LỤC]  {PL[i - len(GHI_CHU)]}"
    else:
        nd = ""
    if nd:
        sl.notes_slide.notes_text_frame.text = nd

pr.save(RA)
print(f"Đã dựng {len(pr.slides._sldIdLst)} slide, có ghi chú người trình bày")
print("Lưu:", RA)
