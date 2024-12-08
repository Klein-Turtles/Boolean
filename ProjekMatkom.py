import tkinter as tk
from tkinter import filedialog, messagebox
import pytesseract
from PIL import Image
import cv2
import os
import json

STOCK_FILE = "stock_data.json"

initial_stock = {"1": True, "2": True, "3": True, "4": True, "5": True,
                 "6": True, "7": True, "8": True, "9": True, "10": True}

def read_stock():
    if os.path.exists(STOCK_FILE):
        with open(STOCK_FILE, "r") as f:
            return json.load(f)
    else:
        return initial_stock

def write_stock(stock):
    with open(STOCK_FILE, "w") as f:
        json.dump(stock, f)

stock = read_stock()

total_uang = 0

a = b = c = d = e = 0

def calculate_boolean(a, b, c, d, e):
    return (b and e) or (b and d) or (a and d) or (a and e) or (c and d) or (c and e) or (a and b and c)

pytesseract.pytesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def recognize_money(image_path):
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        _, gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(
            gray, 
            lang='eng', 
            config='--psm 6 tessedit_char_whitelist=0123456789.'
        )

        text = ''.join(filter(str.isdigit, text))

        if "50000" in text:
            return 50000
        elif "100000" in text:
            return 100000
        else:
            return None
    except Exception as e:
        return None

def show_interface():
    global stock, total_uang, a, b, c, d, e

    def on_pilih(nomor):
        global stock
        if stock[str(nomor)]:
            stock[str(nomor)] = False
            write_stock(stock)
            messagebox.showinfo("Berhasil!", f"Mystery Box Nomor {nomor} Dikeluarkan!")
            update_buttons()
            ask_restart()
        else:
            messagebox.showerror("Sudah Dipilih", f"Mystery Box Nomor {nomor} Sudah Dipilih!")

    def update_buttons():
        for i, btn in enumerate(buttons):
            nomor = str(i + 1)
            if not stock[nomor]:
                btn.config(state=tk.DISABLED)

    def ask_restart():
        global total_uang, a, b, c, d, e
        if sum(stock.values()) == 0:
            messagebox.showinfo("Stok Habis", "Semua Mystery Box Telah Dipilih!")
            root.quit()
        else:
            result = messagebox.askyesno("Beli Lagi", "Apakah Kamu Ingin Membeli Lagi?")
            if result:
                total_uang = 0
                a = b = c = d = e = 0
                proses_uang()
            else:
                root.quit()

    root = tk.Tk()
    root.title("Pilih MYstery Box")
    root.geometry("700x300")
    root.resizable(False, False)
    root.configure(bg="#E6E6FA")

    tk.Label(root, text="Pilih Nomor Mystery Box:", font=("Segoe UI", 16, "bold"), fg="#4B0082", bg="#E6E6FA").pack(pady=10)

    frame_buttons = tk.Frame(root, bg="#E6E6FA")
    frame_buttons.pack()

    buttons = []
    for i in range(1, 11):
        btn = tk.Button(
            frame_buttons,
            text=f"[ {i} ]",
            font=("Segoe UI", 12),
            width=5,
            height=2,
            command=lambda i=i: on_pilih(i),
            bg="#9370DB",
            fg="white",
            activebackground="#8A2BE2",
            relief="flat"
        )
        btn.grid(row=(i - 1) // 5, column=(i - 1) % 5, padx=5, pady=5)
        buttons.append(btn)

    update_buttons()
    root.mainloop()

def proses_uang():
    global total_uang, a, b, c, d, e

    def tambah_uang():
        global total_uang, a, b, c, d, e

        file_path = filedialog.askopenfilename(title="Pilih Gambar Uang", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            nominal = recognize_money(file_path)
            if nominal:
                if total_uang + nominal > 150000:
                    messagebox.showerror("Jumlah Uang Terlalu Banyak", "Tidak Bisa Memasukkan Uang Lebih Dari Rp. 150.000.")
                    return

                total_uang += nominal
                label_total_uang.config(text=f"Total Uang Yang Dimasukkan: Rp. {total_uang}")

                if nominal == 50000:
                    if a == 0:
                        a = 1
                    elif b == 0:
                        b = 1
                    elif c == 0:
                        c = 1
                elif nominal == 100000:
                    if d == 0:
                        d = 1
                    elif e == 0:
                        e = 1

                hasil_boolean = calculate_boolean(a, b, c, d, e)
                print(f"Hasil Aljabar Boolean: {hasil_boolean}")  # Cetak hasilnya di terminal

                if total_uang >= 150000:
                    messagebox.showinfo("Uang Cukup", "Uang Cukup Untuk Membeli Mystery Box!")
                    tambah_uang_button.config(state=tk.DISABLED)
                    show_interface()
                else:
                    messagebox.showinfo("Tambah Uang", "Silakan Tambah Uang Hingga Mencapai Rp. 150.000.")
            else:
                messagebox.showerror("Nominal Tidak Dikenali", "Nominal Uang Tidak Dikenali. Pastikan Gambar Jelas Dan Uang Valid.")
        else:
            messagebox.showwarning("Gambar Tidak Diupload", "Kamu Belum Mengunggah Gambar Uang.")

    root = tk.Tk()
    root.title("^^ Mesin Mystery Box ^^")
    root.geometry("700x300")
    root.resizable(False, False)
    root.configure(bg="#E6E6FA")

    tk.Label(root, text="Masukkan Uang Untuk Membeli Mystery Box.", font=("Segoe UI", 12), fg="#4B0082", bg="#E6E6FA").pack(pady=10)

    label_total_uang = tk.Label(root, text="Total Uang Yang Dimasukkan: Rp. 0", font=("Segoe UI", 12), bg="#E6E6FA", fg="#4B0082")
    label_total_uang.pack(pady=10)

    tambah_uang_button = tk.Button(root, text="Tambah Uang", font=("Segoe UI", 12), command=tambah_uang, bg="#9370DB", fg="white", activebackground="#8A2BE2")
    tambah_uang_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    proses_uang()
