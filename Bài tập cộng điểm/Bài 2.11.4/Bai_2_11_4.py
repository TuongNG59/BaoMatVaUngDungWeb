import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from collections import Counter

#Giao diện GUI
root = tk.Tk()
root.title("Chương trình Hỗ trợ phá mã thay thế đơn bảng")
root.geometry("1050x600")

#Khung nhập văn bản mã hóa
tk.Label(root, text="Văn bản mã hóa", font=("Arial", 10, "bold")).grid(row=0, column=0, pady=(10,0))
txt = tk.Text(root, height=10, width=40, font=("Consolas", 11))
txt.grid(row=1, column=0, rowspan=2, padx=10)

#Khung xuất văn bản giải mã
tk.Label(root, text="Văn bản giải mã", font=("Arial", 10, "bold")).grid(row=3, column=0, pady=(10,0))
result = tk.Text(root, height=10, width=40, font=("Consolas", 11), bg="#f4f4f4")
result.grid(row=4, column=0, padx=10)

# Gợi ý tần suất tiếng Anh chuẩn
chu_xep_hang = "Thứ tự chuẩn (Tiếng Anh): E > T > A > O > I > N > S > H > R > D > L > U > C > M > F > W > Y > G > P > B > V > K > X > J > Q > Z"
lbl_ti_le = tk.Label(root, text=chu_xep_hang, wraplength=350, justify="left", font=("Arial", 10, "italic"), fg="blue")
lbl_ti_le.grid(row=6, column=0, sticky="w", padx=10, pady=10)

#Tạo các bảng thống kê
#Bảng chữ cái
bang = ttk.Treeview(root, columns=("Chu", "TanSo", "Thay"), show="headings", height=18)
bang.heading("Chu", text="Chữ")
bang.heading("TanSo", text="Tần số")
bang.heading("Thay", text="Thay thế")
bang.column("Chu", width=60, anchor="center")
bang.column("TanSo", width=60, anchor="center")
bang.column("Thay", width=80, anchor="center")
bang.grid(row=1, column=1, rowspan=4, padx=(10,5))

#Bảng digram (Cặp 2)
digram = ttk.Treeview(root, columns=("Cap", "TanSo"), show="headings", height=18)
digram.heading("Cap", text="Digram")
digram.heading("TanSo", text="Tần số")
digram.column("Cap", width=70, anchor="center")
digram.column("TanSo", width=60, anchor="center")
digram.grid(row=1, column=2, rowspan=4, padx=5)

#Bảng trigram (Cặp 3)
trigram = ttk.Treeview(root, columns=("BoBa", "TanSo"), show="headings", height=18)
trigram.heading("BoBa", text="Trigram")
trigram.heading("TanSo", text="Tần số")
trigram.column("BoBa", width=80, anchor="center")
trigram.column("TanSo", width=60, anchor="center")
trigram.grid(row=1, column=3, rowspan=4, padx=5)


#HÀM XỬ LÝ
def thong_ke():
    van_ban = txt.get("1.0", "end-1c").upper()
    van_ban_chi_chu = "".join(chu for chu in van_ban if "A" <= chu <= "Z")

    #Xóa dữ liệu cũ trong 3 bảng
    for b in (bang, digram, trigram):
        for dong in b.get_children():
            b.delete(dong)

    if not van_ban_chi_chu:
        giai_ma()
        return

    #Tần suất chuẩn để tự động gợi ý
    english_freq = "ETAOINSHRDLCUMWFGYPBVKXJQZ"
    
    #Thống kê chữ cái và tự động gợi ý
    dem_chu = Counter(van_ban_chi_chu)
    for i, (chu, so_lan) in enumerate(dem_chu.most_common()):
        thay_the_goi_y = english_freq[i] if i < len(english_freq) else ""
        bang.insert("", "end", values=(chu, so_lan, thay_the_goi_y))

    #Thống kê digram
    dem_cap = Counter(van_ban_chi_chu[i:i+2] for i in range(len(van_ban_chi_chu) - 1))
    for cap, so_lan in dem_cap.most_common():
        digram.insert("", "end", values=(cap, so_lan))

    #Thống kê trigram
    dem_bo_ba = Counter(van_ban_chi_chu[i:i+3] for i in range(len(van_ban_chi_chu) - 2))
    for bo_ba, so_lan in dem_bo_ba.most_common():
        trigram.insert("", "end", values=(bo_ba, so_lan))

    #Giải mã ngay lập tức dựa trên bảng gợi ý
    giai_ma()


def giai_ma():
    van_ban = txt.get("1.0", "end-1c").upper()
    bang_thay = {}

    #Lấy dữ liệu từ bảng ánh xạ
    for dong in bang.get_children():
        gia_tri = bang.item(dong, "values")
        chu_ma = gia_tri[0]
        chu_giai_ma = gia_tri[2].strip().upper()
        if chu_giai_ma:
            bang_thay[chu_ma] = chu_giai_ma[0]

    ket_qua = ""
    for chu in van_ban:
        if "A" <= chu <= "Z":
            if chu in bang_thay:
                ket_qua += bang_thay[chu]
            else:
                ket_qua += "-"  # Để lại dấu gạch ngang cho ký tự chưa biết
        else:
            ket_qua += chu

    result.delete("1.0", "end")
    result.insert("1.0", ket_qua)


def sua_chu(event):
    item = bang.identify_row(event.y)
    cot = bang.identify_column(event.x)

    if not item or cot != "#3":
        return

    vi_tri = bang.bbox(item, cot)
    if not vi_tri:
        return

    x, y, w, h = vi_tri
    o_nhap = tk.Entry(bang, justify="center", font=("Arial", 11, "bold"), fg="red")
    o_nhap.place(x=x, y=y, width=w, height=h)
    o_nhap.insert(0, bang.set(item, "Thay"))
    o_nhap.focus_set()

    def luu(event=None):
        if not o_nhap.winfo_exists():
            return

        chu_moi = o_nhap.get().strip().upper()[:1]
        
        #Kiểm tra trùng lặp
        if chu_moi:
            for dong in bang.get_children():
                if dong != item:
                    gia_tri = bang.item(dong, "values")
                    chu_hien_tai = gia_tri[2].strip().upper()
                    if chu_hien_tai == chu_moi:
                        messagebox.showwarning("Cảnh báo", f"Chữ '{chu_moi}' đã được gán cho ký tự '{gia_tri[0]}'\nChọn chữ khác.")
                        o_nhap.destroy()
                        return
        # ---------------------------------------------

        bang.set(item, "Thay", chu_moi)
        o_nhap.destroy()
        giai_ma()

    o_nhap.bind("<Return>", luu)
    o_nhap.bind("<FocusOut>", luu)

bang.bind("<Double-Button-1>", sua_chu)

frame_btn = tk.Frame(root)
frame_btn.grid(row=5, column=1, columnspan=3, pady=10)

tk.Button(frame_btn, text="Phân tích & Tự động Gợi ý", command=thong_ke, font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", width=25).pack(side=tk.LEFT, padx=10)
tk.Button(frame_btn, text="Cập nhật Giải mã", command=giai_ma, font=("Arial", 10, "bold"), bg="#2196F3", fg="white", width=20).pack(side=tk.LEFT, padx=10)

root.mainloop()