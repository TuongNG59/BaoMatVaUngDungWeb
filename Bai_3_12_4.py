import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad


SALT_SIZE = 16   # 16 bytes Salt cho PBKDF2
IV_SIZE = 16     # 16 bytes IV cho AES-CBC
KEY_SIZE = 32    # 32 bytes = 256 bits Key
ITERATIONS = 100_000  # Số vòng lặp PBKDF2 tăng độ an toàn


def derive_key(password: str, salt: bytes) -> bytes:
    """Tạo khóa 256-bit từ mật khẩu và Salt bằng thuật toán PBKDF2"""
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS)


def encrypt_file(file_path: str, password: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError("File không tồn tại!")

    #Sinh Salt và IV ngẫu nhiên
    salt = get_random_bytes(SALT_SIZE)
    iv = get_random_bytes(IV_SIZE)

    #Tạo khóa AES từ Password + Salt
    key = derive_key(password, salt)

    #Đọc dữ liệu binary của file
    with open(file_path, "rb") as f:
        plaintext_data = f.read()

    #Mã hóa dữ liệu với Padding PKCS7
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext_data, AES.block_size))

    #Ghi theo cấu trúc: [16B Salt] + [16B IV] + [Ciphertext]
    output_path = file_path + ".enc"
    with open(output_path, "wb") as f:
        f.write(salt + iv + ciphertext)

    return output_path


def decrypt_file(file_path: str, password: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError("File không tồn tại!")

    #Đọc dữ liệu file đã mã hóa
    with open(file_path, "rb") as f:
        file_data = f.read()

    if len(file_data) < SALT_SIZE + IV_SIZE + AES.block_size:
        raise ValueError("File bị lỗi hoặc không đúng định dạng mã hóa!")

    #Tách Salt, IV và Ciphertext
    salt = file_data[:SALT_SIZE]
    iv = file_data[SALT_SIZE : SALT_SIZE + IV_SIZE]
    ciphertext = file_data[SALT_SIZE + IV_SIZE :]

    #Khôi phục khóa AES từ Password + Salt
    key = derive_key(password, salt)

    #Giải mã và Unpad
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    plaintext_data = unpad(decrypted_padded, AES.block_size)

    #Tạo tên file sau khi khôi phục
    if file_path.endswith(".enc"):
        output_path = file_path[:-4] + ".dec"
    else:
        output_path = file_path + ".dec"

    with open(output_path, "wb") as f:
        f.write(plaintext_data)

    return output_path




class FileCipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Mã hóa & Giải mã File (AES-256-CBC)")
        self.root.geometry("600x320")
        self.root.resizable(False, False)

        # Tiêu đề
        lbl_title = tk.Label(
            root, text="MÃ HÓA & GIẢI MÃ FILE BẢO MẬT", font=("Arial", 14, "bold"), fg="#1A237E"
        )
        lbl_title.pack(pady=15)

        #Khung chọn File
        frame_file = tk.Frame(root)
        frame_file.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_file, text="Đường dẫn File:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        self.txt_filepath = tk.Entry(frame_file, width=45, font=("Arial", 10))
        self.txt_filepath.grid(row=1, column=0, padx=(0, 10), pady=5)

        btn_browse = tk.Button(
            frame_file, text="Chọn File...", command=self.browse_file, bg="#E0E0E0", width=12
        )
        btn_browse.grid(row=1, column=1)

        #Khung nhập Password
        frame_pass = tk.Frame(root)
        frame_pass.pack(fill="x", padx=20, pady=10)

        tk.Label(frame_pass, text="Mật khẩu (Khóa):", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        self.txt_password = tk.Entry(frame_pass, width=45, font=("Arial", 10), show="*")
        self.txt_password.grid(row=1, column=0, padx=(0, 10), pady=5)

        #Khung Nút hành động
        frame_btn = tk.Frame(root)
        frame_btn.pack(pady=20)

        btn_encrypt = tk.Button(
            frame_btn,
            text="🔒 Mã hóa File",
            command=self.handle_encrypt,
            bg="#2E7D32",
            fg="white",
            font=("Arial", 11, "bold"),
            width=18,
            height=2,
        )
        btn_encrypt.pack(side="left", padx=15)

        btn_decrypt = tk.Button(
            frame_btn,
            text="🔓 Giải mã File",
            command=self.handle_decrypt,
            bg="#1565C0",
            fg="white",
            font=("Arial", 11, "bold"),
            width=18,
            height=2,
        )
        btn_decrypt.pack(side="left", padx=15)

        #Thanh trạng thái
        self.lbl_status = tk.Label(root, text="Sẵn sàng...", bd=1, relief="sunken", anchor="w")
        self.lbl_status.pack(side="bottom", fill="x")

    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.txt_filepath.delete(0, tk.END)
            self.txt_filepath.insert(0, filename)

    def handle_encrypt(self):
        file_path = self.txt_filepath.get().strip()
        password = self.txt_password.get()

        if not file_path or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn File và nhập Mật khẩu!")
            return

        try:
            self.lbl_status.config(text="Đang mã hóa file", fg="blue")
            self.root.update()

            out_file = encrypt_file(file_path, password)

            self.lbl_status.config(text=f"Đã mã hóa thành công: {out_file}", fg="green")
            messagebox.showinfo("Thành công", f"Đã tạo file mã hóa:\n{out_file}")
        except Exception as e:
            self.lbl_status.config(text="Mã hóa thất bại!", fg="red")
            messagebox.showerror("Lỗi mã hóa", str(e))

    def handle_decrypt(self):
        file_path = self.txt_filepath.get().strip()
        password = self.txt_password.get()

        if not file_path or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn File và nhập Mật khẩu!")
            return

        try:
            self.lbl_status.config(text="Đang giải mã file", fg="blue")
            self.root.update()

            out_file = decrypt_file(file_path, password)

            self.lbl_status.config(text=f"Đã giải mã thành công: {out_file}", fg="green")
            messagebox.showinfo("Thành công", f"Đã giải mã file ra:\n{out_file}")
        except ValueError:
            self.lbl_status.config(text="Giải mã thất bại!", fg="red")
            messagebox.showerror(
                "Lỗi giải mã", "Mật khẩu không chính xác hoặc File bị hư hỏng/thay đổi!"
            )
        except Exception as e:
            self.lbl_status.config(text="Lỗi hệ thống!", fg="red")
            messagebox.showerror("Lỗi", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = FileCipherApp(root)
    root.mainloop()