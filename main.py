import pandas as pd
import fungsi1 as fs

try:
    df = pd.read_csv("data_obat.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Kode", "Nama", "Kategori", "Stok", "Harga", "Tanggal_Kadaluarsa"])

print("Selamat datang di aplikasi kami!")
fs.menu_utama()