import pandas as pd
import fungsi1 as fs

try:
    df = pd.read_csv("rincian_acara.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Kode", "Acara", "Guest Star", "Tempat", "Jadwal", "Harga Tiket", "Stok Tiket"])

print("Selamat datang di aplikasi kami!")
fs.menu_utama(df)