# -*- coding: utf-8 -*-
"""Vẽ ba hình mới cho bộ slide bảo vệ, ở đúng kích thước sẽ đặt lên slide.

Vẽ đúng cỡ thật (figsize = kích thước đặt trên slide) nên fontsize trong
matplotlib chính là cỡ chữ điểm nhìn thấy khi chiếu — không bị co lại.

    python slides/ve_hinh.py
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

NAVY = "#1F4E79"
XANH = "#2E75B6"
THAN = "#2D2D2D"
XAM = "#777777"
DO = "#C00000"
VANG = "#FFF2CC"
LUOI = "#E2E8F0"

RA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hinh")
os.makedirs(RA, exist_ok=True)

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 15,
    "axes.edgecolor": XAM,
    "axes.labelcolor": THAN,
    "text.color": THAN,
    "xtick.color": THAN,
    "ytick.color": THAN,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "figure.facecolor": "white",
})


def hinh1_tam_co_quan():
    """Dice của TransUNet trên tám cơ quan — làm nổi tuyến tụy."""
    # Bảng 4.5, cột Dice TransUNet
    du = [("Gan", 94.34), ("Động mạch chủ", 87.45), ("Lách", 85.69),
          ("Thận trái", 81.32), ("Thận phải", 78.23), ("Dạ dày", 74.54),
          ("Tuyến tụy", 54.37), ("Túi mật", 50.32)]
    ten = [d[0] for d in du]
    gt = [d[1] for d in du]
    mau = [XANH if t != "Tuyến tụy" else DO for t in ten]

    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    thanh = ax.barh(range(len(ten)), gt, color=mau, height=0.68)
    ax.set_yticks(range(len(ten)))
    ax.set_yticklabels(ten, fontsize=15)
    ax.invert_yaxis()
    ax.set_xlim(0, 108)
    ax.set_xlabel("Dice (%)", fontsize=15, color=XAM)
    ax.tick_params(axis="x", labelsize=13, colors=XAM)
    ax.xaxis.grid(True, color=LUOI, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(XAM)

    for i, (b, v) in enumerate(zip(thanh, gt)):
        dam = ten[i] == "Tuyến tụy"
        ax.text(v + 1.8, b.get_y() + b.get_height() / 2,
                f"{v:.2f}".replace(".", ","),
                va="center", fontsize=14 if dam else 13,
                color=DO if dam else THAN,
                fontweight="bold" if dam else "normal")

    # nhãn tô đậm cho tuyến tụy
    ax.get_yticklabels()[6].set_color(DO)
    ax.get_yticklabels()[6].set_fontweight("bold")

    # Không vẽ mũi tên so sánh trên biểu đồ: nó đè lên nhãn của túi mật.
    # Phần so sánh tụy ↔ gan để ở cột diễn giải bên phải slide.

    fig.savefig(os.path.join(RA, "moi_1_tam_co_quan.png"))
    plt.close(fig)
    print("  ✓ moi_1_tam_co_quan.png")


def hinh2_danh_doi():
    """Dice × HD95 — năm cấu hình. Chữ thập tại TransUNet chia bốn góc phần tư."""
    G_DICE, G_HD = 54.37, 15.38      # mốc TransUNet, Bảng 4.3
    X0, X1, Y0, Y1 = 53.2, 60.8, 4.0, 35.5

    fig, ax = plt.subplots(figsize=(7.4, 4.6))

    # góc phần tư tốt hơn TransUNet ở CẢ HAI chỉ số
    ax.add_patch(plt.Rectangle((G_DICE, Y0), X1 - G_DICE, G_HD - Y0,
                               facecolor=VANG, edgecolor="none", zorder=0))
    ax.axvline(G_DICE, color=XAM, lw=1.1, ls="--", zorder=1)
    ax.axhline(G_HD, color=XAM, lw=1.1, ls="--", zorder=1)
    ax.text(54.55, 4.5, "tốt hơn TransUNet\nở cả hai chỉ số", ha="left",
            va="bottom", fontsize=12.5, color="#7A5200", fontweight="bold",
            linespacing=1.4, zorder=2)

    for dice, hd, mau, cỡ in [(G_DICE, G_HD, XAM, 170),
                              (58.93, 13.20, XANH, 170),
                              (55.95, 13.13, XANH, 170),
                              (58.32, 32.17, DO, 190),
                              (59.23, 12.97, NAVY, 330)]:
        ax.scatter(dice, hd, s=cỡ, color=mau, zorder=6,
                   edgecolors="white", linewidths=2)

    # nhãn: mỗi đường dẫn đi về một phía riêng, không cắt nhau
    ax.annotate("TransUNet", (G_DICE, G_HD), (53.5, 18.4), fontsize=14,
                color=XAM, ha="left",
                arrowprops=dict(arrowstyle="-", color=XAM, lw=1))
    ax.annotate("CBAM + RA trên nhánh nối tắt\nrecall cao nhất, biên tệ nhất",
                (58.32, 32.17), (53.5, 27.4), fontsize=13.5, color=DO,
                fontweight="bold", ha="left", linespacing=1.4,
                arrowprops=dict(arrowstyle="-", color=DO, lw=1.2))
    ax.annotate("CBAM đa tỷ lệ", (58.93, 13.20), (57.4, 20.4), fontsize=13.5,
                color=XANH, ha="center",
                arrowprops=dict(arrowstyle="-", color=XANH, lw=1))
    ax.annotate("CBAM + RA sau nối", (55.95, 13.13), (53.5, 9.2), fontsize=13.5,
                color=XANH, ha="left",
                arrowprops=dict(arrowstyle="-", color=XANH, lw=1))
    ax.annotate("CBAM trước bước tạo token\nĐỀ XUẤT", (59.23, 12.97),
                (57.9, 6.6), fontsize=14, color=NAVY, fontweight="bold",
                ha="center", linespacing=1.4,
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=1.4))

    ax.set_xlabel("Dice (%)  —  cao hơn là tốt hơn", fontsize=14.5, color=XAM)
    ax.set_ylabel("HD95 (mm)  —  thấp hơn là tốt hơn", fontsize=14.5, color=XAM)
    ax.set_xlim(X0, X1)
    ax.set_ylim(Y0, Y1)
    ax.tick_params(labelsize=13, colors=XAM)
    ax.grid(True, color=LUOI, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    fig.savefig(os.path.join(RA, "moi_2_danh_doi.png"))
    plt.close(fig)
    print("  ✓ moi_2_danh_doi.png")


def hinh3_ma_tran():
    """Ma trận 2×2 định vị bốn nhánh theo hai trục nhị phân."""
    fig, ax = plt.subplots(figsize=(7.9, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.9)
    ax.axis("off")

    # cột: (dòng đậm, dòng phụ)
    cot = [("TRƯỚC bước tạo token", "còn là lưới hai chiều"),
           ("SAU bước tạo token", "đã thành chuỗi token")]
    hang = ["Can thiệp\nHẸP", "Can thiệp\nRỘNG"]

    o = [
        # (cột, hàng, nhãn, mô tả, có phải nhánh đề xuất)
        (0, 0, "Nhánh 2 — ĐỀ XUẤT", "CBAM trên tầng ẩn 1/16", True),
        (1, 0, "Nhánh 3", "RA trên nhánh nối tắt 1/8\ntrước khi hợp nhất", False),
        (0, 1, "Nhánh 1", "CBAM đa tỷ lệ\n1/8 · 1/4 · 1/2", False),
        (1, 1, "Nhánh 4", "RA sau phép nối đầu\nsau khi hợp nhất", False),
    ]

    x0, y0, w, h, dx, dy = 1.75, 0.30, 3.95, 2.45, 4.25, 2.65

    for c in range(2):
        cx = x0 + c * dx + w / 2
        ax.text(cx, y0 + dy + h + 0.92, cot[c][0], ha="center", va="center",
                fontsize=14, color=NAVY, fontweight="bold")
        ax.text(cx, y0 + dy + h + 0.42, cot[c][1], ha="center", va="center",
                fontsize=12.5, color=XAM)
    for r in range(2):
        ax.text(x0 - 0.28, y0 + (1 - r) * dy + h / 2, hang[r],
                ha="right", va="center", fontsize=13.5, color=NAVY,
                fontweight="bold", linespacing=1.5)

    for c, r, nhan, mo_ta, dx_ in o:
        px, py = x0 + c * dx, y0 + (1 - r) * dy
        ax.add_patch(FancyBboxPatch(
            (px, py), w, h, boxstyle="round,pad=0.05",
            facecolor=VANG if dx_ else "#F4F7FB",
            edgecolor=NAVY if dx_ else "#C8D6E5",
            linewidth=2.4 if dx_ else 1.2))
        ax.text(px + w / 2, py + h * 0.70, nhan, ha="center", va="center",
                fontsize=14.5, color=NAVY if dx_ else THAN, fontweight="bold")
        ax.text(px + w / 2, py + h * 0.30, mo_ta, ha="center", va="center",
                fontsize=13, color=THAN, linespacing=1.5)

    fig.savefig(os.path.join(RA, "moi_3_ma_tran.png"))
    plt.close(fig)
    print("  ✓ moi_3_ma_tran.png")


if __name__ == "__main__":
    print("Vẽ hình cho slide:")
    hinh1_tam_co_quan()
    hinh2_danh_doi()
    hinh3_ma_tran()
    print("Xong, lưu ở slides/hinh/")
