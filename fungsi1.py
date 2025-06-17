import pandas as pd
import time
import os
import math
import re
from datetime import datetime
from halo import Halo
from tabulate import tabulate
from typing import List, Any

NAMA_PENGGUNA_ADMIN = "admin"
SANDI_ADMIN = "admin123"

def muat_data_csv(nama_file: str, kolom_default: list) -> pd.DataFrame:
    """Memuat data dari file CSV, atau membuat file baru jika tidak ditemukan atau kosong."""
    try:
        # Coba baca file. Jika kosong, akan menimbulkan error.
        df = pd.read_csv(nama_file)
        if df.empty:
            return pd.DataFrame(columns=kolom_default)
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # Jika file tidak ditemukan ATAU jika file ada tapi kosong (menyebabkan EmptyDataError)
        print(f"Info: Berkas '{nama_file}' tidak ditemukan atau kosong. Berkas akan disiapkan.")
        animasi_memuat(1)
        # Membuat DataFrame kosong dengan kolom yang ditentukan dan menyimpannya
        df_kosong = pd.DataFrame(columns=kolom_default)
        df_kosong.to_csv(nama_file, index=False)
        return df_kosong
    except Exception as e:
        print(f"Terjadi kesalahan tak terduga saat memuat berkas '{nama_file}': {e}")
        # Kembalikan DataFrame kosong agar program tidak berhenti
        return pd.DataFrame(columns=kolom_default)

def bersihkan_layar():
    """Membersihkan layar terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def animasi_memuat(durasi: int):
    """Menampilkan animasi memuat selama durasi tertentu."""
    spinner = Halo(text='Memuat...', spinner='dots')
    spinner.start()
    time.sleep(durasi)  
    spinner.stop()

def menu_utama():
    """Menampilkan menu utama aplikasi."""
    while True:
        bersihkan_layar()
        print("╔═══════════════════════════════════════╗")
        print("║     Sistem Informasi Data Apotek      ║")
        print("╠═══════════════════════════════════════╣")
        print("║  [1] Masuk sebagai Admin              ║")
        print("║  [2] Keluar                           ║")
        print("╚═══════════════════════════════════════╝")
        pilihan = input("Pilih menu (1/2): ").strip()
        
        if pilihan == "1":
            masuk_admin()
            # Setelah admin logout, menu_utama akan ditampilkan lagi oleh menu_admin.
            # Jadi break di sini agar tidak tumpang tindih.
            break 
        elif pilihan == "2":
            bersihkan_layar()
            print("Terima kasih telah menggunakan program ini.")
            time.sleep(2)
            break
        else:
            print("Pilihan tidak valid! Silakan pilih 1 atau 2.")
            time.sleep(2)

def masuk_admin():
    """Menangani proses masuk (login) admin."""
    bersihkan_layar()
    print("\n〓〓〓〓〓〓〓〓〓〓【 MASUK ADMIN 】〓〓〓〓〓〓〓〓〓〓")
    nama_pengguna = input("Nama Pengguna: ").strip()
    sandi = input("Sandi: ").strip()

    if nama_pengguna == NAMA_PENGGUNA_ADMIN and sandi == SANDI_ADMIN:
        animasi_memuat(1)
        print("Berhasil masuk!")
        time.sleep(1)
        menu_admin()
    else:
        print("Nama pengguna atau sandi salah!")
        animasi_memuat(2)
        menu_utama()

def menu_admin():
    """Menampilkan menu utama untuk admin."""
    while True:
        bersihkan_layar()
        print("╔═══════════════════════════════════════╗")
        print("║             Menu Admin                ║")
        print("╠═══════════════════════════════════════╣")
        print("║  [1] Tambah Data Obat                 ║")
        print("║  [2] Kelola Data Obat                 ║")
        print("║  [3] Cari Obat                        ║")
        print("║  [4] Urutkan Data Obat                ║")
        print("║  [5] Lakukan Pembelian                ║")
        print("║  [6] Lihat Riwayat Transaksi          ║")
        print("║  [7] Kembali ke Menu Utama            ║")
        print("╚═══════════════════════════════════════╝")
        pilihan = input("Silahkan pilih menu (1-7): ").strip()

        if pilihan == '1': 
            tambah_data_obat()
        elif pilihan == '2': 
            kelola_data_obat()
        elif pilihan == '3': 
            cari_data_obat()
        elif pilihan == '4': 
            urutkan_data_obat()
        elif pilihan == '5': 
            lakukan_pembelian()
        elif pilihan == '6': 
            lihat_riwayat_transaksi()
        elif pilihan == '7':
            print("Kembali ke menu utama...")
            animasi_memuat(1)
            menu_utama()
            break
        else:
            print("Pilihan tidak valid! Silakan pilih 1-7.")
            time.sleep(2)

def cari_lompat(daftar_data: List[dict], target: str, kunci: str) -> int:
    """Mencari data menggunakan algoritma Jump Search."""
    jumlah_data = len(daftar_data)
    if jumlah_data == 0: return -1
        
    langkah = int(math.sqrt(jumlah_data))
    indeks_sebelumnya = 0
    
    # Melompat untuk menemukan blok
    while str(daftar_data[min(langkah, jumlah_data) - 1].get(kunci, '')).lower() < target.lower():
        indeks_sebelumnya = langkah
        langkah += int(math.sqrt(jumlah_data))
        if indeks_sebelumnya >= jumlah_data: return -1
            
    # Pencarian linear di dalam blok
    for i in range(indeks_sebelumnya, min(langkah, jumlah_data)):
        if str(daftar_data[i].get(kunci, '')).lower() == target.lower(): return i
        
    return -1

def urutkan_cepat(data_list, key, ascending=True):
    """Mengurutkan data berdasarkan key tertentu menggunakan metode QuickSort."""
    if len(data_list) <= 1:
        return data_list

    pivot = data_list[0]
    pivot_key = str(pivot[key]).lower() if isinstance(pivot[key], str) else pivot[key]

    def ambil_kunci(item):
        return str(item[key]).lower() if isinstance(item[key], str) else item[key]

    # Mengganti list comprehension menjadi loop for biasa
    kiri = []
    kanan = []
    if ascending:
        for item in data_list[1:]:
            if ambil_kunci(item) <= pivot_key:
                kiri.append(item)
            else:
                kanan.append(item)
    else: # descending
        for item in data_list[1:]:
            if ambil_kunci(item) > pivot_key:
                kiri.append(item)
            else:
                kanan.append(item)

    return urutkan_cepat(kiri, key, ascending) + [pivot] + urutkan_cepat(kanan, key, ascending)

def urutkan_data_obat():
    """Menangani logika untuk mengurutkan data obat."""
    while True:
        bersihkan_layar()
        kolom_obat = ["Kode", "Nama", "Kategori", "Stok", "Harga", "Kadaluarsa", "Deskripsi"]
        data_obat_df = muat_data_csv("database_obat.csv", kolom_obat)
        if data_obat_df.empty:
            print("Data obat kosong, tidak ada yang bisa diurutkan."); input("\nTekan Enter..."); break
            
        print("╔═══════════════════════════════════╗")
        print("║       Menu Pengurutan Data        ║")
        print("╠═══════════════════════════════════╣")
        print("║  [1] Urutkan berdasarkan Nama     ║")
        print("║  [2] Urutkan berdasarkan Stok     ║")
        print("║  [3] Urutkan berdasarkan Harga    ║")
        print("║  [4] Kembali ke Menu Admin        ║")
        print("╚═══════════════════════════════════╝")

        pilihan = input("Pilih metode pengurutan (1-4): ").strip()
        if pilihan == "4": break

        kunci_urutan = ""
        if pilihan == "1": 
            kunci_urutan = "Nama"
        elif pilihan == "2": 
            kunci_urutan = "Stok"
        elif pilihan == "3": 
            kunci_urutan = "Harga"
        else: print("Pilihan tidak valid!"); time.sleep(2); continue

        pilihan_urutan = input("Urutkan secara menaik (y) atau menurun (n)? (y/n): ").lower().strip()
        if pilihan_urutan not in ['y', 'n']: print("Pilihan tidak valid!"); time.sleep(2); continue
        urutan_menaik = True if pilihan_urutan == 'y' else False
        
        data_terurut = urutkan_cepat(data_obat_df.to_dict('records'), kunci_urutan, urutan_menaik)
        
        bersihkan_layar()
        arah = "Menaik" if urutan_menaik else "Menurun"
        print(f"\n--- Data diurutkan berdasarkan {kunci_urutan} ({arah}) ---")
        
        df_tampil = pd.DataFrame(data_terurut)
        if 'Harga' in df_tampil.columns:
            harga_terformat = []
            for harga in df_tampil['Harga']:
                if pd.notna(harga):
                    harga_terformat.append(f"Rp{int(harga):,}".replace(",", "."))
                else:
                    harga_terformat.append("Rp0")
            df_tampil['Harga'] = harga_terformat
        print(tabulate(df_tampil, headers="keys", tablefmt="fancy_grid", showindex=False))
        
        input("\nTekan Enter untuk melanjutkan...")

# --- FUNGSI TAMBAHAN UNTUK FITUR BARU ---
def ekstrak_dosis(deskripsi: str) -> float:
    """Mengekstrak angka dosis dari teks deskripsi untuk keperluan pengurutan."""
    if not isinstance(deskripsi, str): return 0.0
    hasil = re.search(r'(\d+\.?\d*)', deskripsi)
    if hasil: return float(hasil.group(1))
    return 0.0

def menu_pengurutan_hasil_pencarian(df_hasil: pd.DataFrame):
    """Menampilkan menu untuk mengurutkan hasil pencarian."""
    if df_hasil.empty:
        print("\nTidak ada data yang cocok untuk diurutkan.")
        return

    df_urut = df_hasil.copy()
    
    dosis_list = []
    for nama_obat in df_urut['Nama']:
        dosis_list.append(ekstrak_dosis(nama_obat))
    df_urut['DosisNumerik'] = dosis_list

    while True:
        bersihkan_layar()
        print("\n--- Hasil Pencarian ---")
        
        df_tampil = df_urut.drop(columns=['DosisNumerik'])
        if 'Harga' in df_tampil.columns:
            harga_terformat = []
            for harga in df_tampil['Harga']:
                if pd.notna(harga):
                    harga_terformat.append(f"Rp{int(harga):,}".replace(",", "."))
                else:
                    harga_terformat.append("Rp0")
            df_tampil['Harga'] = harga_terformat
        print(tabulate(df_tampil, headers="keys", tablefmt="fancy_grid", showindex=False))
        
        print("\n--- Opsi Pengurutan Hasil ---")
        print("[1] Urutkan Harga (Termurah)")
        print("[2] Urutkan Harga (Termahal)")
        print("[3] Urutkan Stok (Tersedikit)")
        print("[4] Urutkan Stok (Terbanyak)")
        print("[5] Urutkan Dosis (Terkecil)")
        print("[6] Urutkan Dosis (Terbesar)")
        print("[0] Kembali ke Pencarian")
        
        pilihan = input("Pilih opsi pengurutan (0-6): ").strip()
        
        if pilihan == '1': 
            df_urut = df_urut.sort_values(by='Harga', ascending=True)
        elif pilihan == '2': 
            df_urut = df_urut.sort_values(by='Harga', ascending=False)
        elif pilihan == '3': 
            df_urut = df_urut.sort_values(by='Stok', ascending=True)
        elif pilihan == '4': 
            df_urut = df_urut.sort_values(by='Stok', ascending=False)
        elif pilihan == '5': 
            df_urut = df_urut.sort_values(by='DosisNumerik', ascending=True)
        elif pilihan == '6': 
            df_urut = df_urut.sort_values(by='DosisNumerik', ascending=False)
        elif pilihan == '0': 
            break
        else: 
            print("Pilihan tidak valid!"); time.sleep(1)

# --- FUNGSI UTAMA YANG DIMODIFIKASI ---
def cari_data_obat():
    """Menangani logika untuk mencari data obat dan menambahkan opsi pengurutan."""
    while True:
        bersihkan_layar()
        kolom_obat = ["Kode", "Nama", "Kategori", "Stok", "Harga", "Kadaluarsa", "Deskripsi"]
        data_obat_df = muat_data_csv("database_obat.csv", kolom_obat)
        
        print("╔═══════════════════════════════════╗")
        print("║         Menu Pencarian Obat       ║")
        print("╠═══════════════════════════════════╣")
        print("║  [1] Cari berdasarkan Nama        ║")
        print("║  [2] Cari berdasarkan Kode        ║")
        print("║  [3] Cari berdasarkan Kategori    ║")
        print("║  [4] Kembali ke Menu Admin        ║")
        print("╚═══════════════════════════════════╝")

        pilihan = input("Pilih metode pencarian (1-4): ").strip()
        if pilihan == "4": break

        kunci_pencarian, kata_kunci = "", ""
        if pilihan == "1": 
            kunci_pencarian, kata_kunci = "Nama", input("Masukkan nama obat: ")
        elif pilihan == "2": 
            kunci_pencarian, kata_kunci = "Kode", input("Masukkan kode obat: ")
        elif pilihan == "3": 
            kunci_pencarian, kata_kunci = "Kategori", input("Masukkan kategori obat: ")
        else: 
            print("Pilihan tidak valid!"); time.sleep(2); continue

        if not kata_kunci.strip(): print("Input pencarian tidak boleh kosong."); time.sleep(2); continue
        
        daftar_obat = data_obat_df.to_dict('records')
        
        hasil_pencarian = []
        if pilihan == "2": # Pencarian kode menggunakan jump search (membutuhkan data terurut)
            data_terurut_kode = sorted(daftar_obat, key=lambda x: str(x.get("Kode", '')).lower())
            indeks_hasil = cari_lompat(data_terurut_kode, kata_kunci, "Kode")
            if indeks_hasil != -1: hasil_pencarian.append(data_terurut_kode[indeks_hasil])
        else: # Pencarian nama/kategori menggunakan loop biasa
            for obat in daftar_obat:
                nilai_kolom = str(obat.get(kunci_pencarian, ''))
                if kata_kunci.lower() in nilai_kolom.lower():
                    hasil_pencarian.append(obat)
        
        bersihkan_layar()
        if hasil_pencarian:
            df_hasil = pd.DataFrame(hasil_pencarian)
            menu_pengurutan_hasil_pencarian(df_hasil)
        else:
            print(f"\nObat dengan {kunci_pencarian} mengandung '{kata_kunci}' tidak ditemukan.")
            input("\nTekan Enter untuk melanjutkan...")

def tambah_data_obat():
    """Menangani penambahan data obat baru."""
    bersihkan_layar()
    kolom_obat = ["Kode", "Nama", "Kategori", "Stok", "Harga", "Kadaluarsa", "Deskripsi"]
    data_obat_df = muat_data_csv("database_obat.csv", kolom_obat)
    
    print("\n--- Masukkan Data Obat Baru ---")
    
    kode_terakhir_str = "OBT000"
    if not data_obat_df.empty and "Kode" in data_obat_df.columns and not data_obat_df["Kode"].isnull().all():
        kode_valid = []
        for kode in data_obat_df["Kode"].dropna():
            if str(kode).startswith("OBT"):
                kode_valid.append(str(kode))
        if kode_valid:
            kode_terakhir_str = max(kode_valid)

    try:
        nomor_urut = int(kode_terakhir_str[3:]) + 1
    except (ValueError, IndexError):
        nomor_urut = len(data_obat_df) + 1
    kode_obat = f"OBT{nomor_urut:03d}"
    print(f"Kode Obat Baru (otomatis): {kode_obat}")

    while True:
        nama_obat = input("Nama Obat\t: ").strip()
        if nama_obat: break
        else: print("Nama obat tidak boleh kosong.")
    
    kategori = input("Kategori\t: ").strip()

    while True:
        stok_str = input("Stok\t\t: ").strip()
        try:
            stok = int(stok_str)
            if stok >= 0: break
            else: print("Stok tidak boleh negatif.")
        except ValueError:
            print("Stok harus berupa angka.")

    while True:
        harga_str = input("Harga\t\t: Rp. ").strip().replace('.', '').replace(',', '')
        try:
            harga = float(harga_str)
            if harga >= 0: break
            else: print("Harga tidak boleh negatif.")
        except ValueError:
            print("Harga harus berupa angka.")
    
    kadaluarsa = input("Kadaluarsa (YYYY-MM-DD)\t: ").strip() # Diubah agar konsisten
    deskripsi = input("Deskripsi\t: ").strip()

    data_baru = {"Kode": kode_obat, "Nama": nama_obat, "Kategori": kategori, "Stok": stok, "Harga": harga, "Kadaluarsa": kadaluarsa, "Deskripsi": deskripsi}
    df_baru = pd.DataFrame([data_baru])

    data_obat_df = pd.concat([data_obat_df, df_baru], ignore_index=True)
    data_obat_df.to_csv("database_obat.csv", index=False)
    
    bersihkan_layar()
    print("\n--- Data obat berhasil disimpan ---")
    
    df_tampil = df_baru.copy()
    if 'Harga' in df_tampil.columns:
        harga_terformat = []
        for harga in df_tampil['Harga']:
            if pd.notna(harga):
                harga_terformat.append(f"Rp{int(harga):,}".replace(",", "."))
            else:
                harga_terformat.append("Rp0")
        df_tampil['Harga'] = harga_terformat
    print(tabulate(df_tampil, headers="keys", tablefmt="fancy_grid", showindex=False))
    
    input("\nTekan Enter untuk kembali...")

def kelola_data_obat():
    """Menu untuk mengelola data obat (update, hapus)."""
    while True:
        bersihkan_layar()
        kolom_obat = ["Kode", "Nama", "Kategori", "Stok", "Harga", "Kadaluarsa", "Deskripsi"]
        data_obat_df = muat_data_csv("database_obat.csv", kolom_obat)
        
        print("╔═══════════════════════════════════╗")
        print("║         Menu Kelola Obat          ║")
        print("╠═══════════════════════════════════╣")
        print("║  [1] Tampilkan Semua Obat         ║")
        print("║  [2] Perbarui Data Obat           ║")
        print("║  [3] Hapus Data Obat              ║")
        print("║  [4] Kembali ke Menu Admin        ║")
        print("╚═══════════════════════════════════╝")

        pilihan = input("Silahkan pilih menu (1-4): ").strip()
        if pilihan == "1":
            bersihkan_layar()
            if data_obat_df.empty: 
                print("Data obat kosong.")
            else: 
                df_tampil = data_obat_df.copy()
                if 'Harga' in df_tampil.columns:
                    harga_terformat = []
                    for harga in df_tampil['Harga']:
                        if pd.notna(harga):
                            harga_terformat.append(f"Rp{int(harga):,}".replace(",", "."))
                        else:
                            harga_terformat.append("Rp0")
                    df_tampil['Harga'] = harga_terformat
                print("\n" + tabulate(df_tampil, headers="keys", tablefmt="fancy_grid", showindex=False))
            input("\nTekan Enter untuk kembali...")
        elif pilihan == "2": 
            perbarui_data_obat(data_obat_df)
        elif pilihan == "3": 
            hapus_data_obat(data_obat_df)
        elif pilihan == "4": 
            break
        else: 
            print("Pilihan tidak valid!"); time.sleep(2)

def perbarui_data_obat(data_obat_df):
    """Menangani proses pembaruan data obat."""
    bersihkan_layar()
    if data_obat_df.empty:
        print("Data obat kosong."); input("\nTekan Enter..."); return

    df_tampil = data_obat_df.copy()
    if 'Harga' in df_tampil.columns:
        harga_terformat = []
        for harga in df_tampil['Harga']:
            if pd.notna(harga):
                harga_terformat.append(f"Rp{int(harga):,}".replace(",", "."))
            else:
                harga_terformat.append("Rp0")
        df_tampil['Harga'] = harga_terformat
    print(tabulate(df_tampil, headers="keys", tablefmt="fancy_grid", showindex=False))
    
    kode_target = input("\nMasukkan KODE obat yang akan diperbarui: ").strip().upper()
    baris_target = data_obat_df[data_obat_df['Kode'].str.upper() == kode_target]

    if baris_target.empty:
        print(f"Kode obat '{kode_target}' tidak ditemukan."); time.sleep(2); return

    indeks_target = baris_target.index[0]
    
    print("\nData apa yang ingin diperbarui?")
    print("[1] Nama, [2] Kategori, [3] Stok, [4] Harga, [5] Kadaluarsa, [6] Deskripsi")
    pilihan_kolom = input("Pilih (1-6): ").strip()

    peta_kolom = {"1": "Nama", "2": "Kategori", "3": "Stok", "4": "Harga", "5": "Kadaluarsa", "6": "Deskripsi"}
    kolom_untuk_diperbarui = peta_kolom.get(pilihan_kolom)

    if not kolom_untuk_diperbarui:
        print("Pilihan tidak valid."); time.sleep(2); return
        
    nilai_baru_str = input(f"Masukkan {kolom_untuk_diperbarui} baru: ").strip()
    
    try:
        if kolom_untuk_diperbarui == "Stok":
            nilai_baru = int(nilai_baru_str)
        elif kolom_untuk_diperbarui == "Harga":
            nilai_baru = float(nilai_baru_str)
        else:
            nilai_baru = nilai_baru_str
    except ValueError:
        print("Input tidak valid untuk Stok atau Harga. Perubahan dibatalkan."); time.sleep(2); return

    data_obat_df.loc[indeks_target, kolom_untuk_diperbarui] = nilai_baru
    data_obat_df.to_csv("database_obat.csv", index=False)
    
    bersihkan_layar()
    print(f"\nData {kolom_untuk_diperbarui} untuk kode {kode_target} berhasil diperbarui.")
    
    df_tampil_update = data_obat_df.loc[[indeks_target]].copy()
    if 'Harga' in df_tampil_update.columns:
        harga_terformat_update = []
        for harga in df_tampil_update['Harga']:
            if pd.notna(harga):
                harga_terformat_update.append(f"Rp{int(harga):,}".replace(",", "."))
            else:
                harga_terformat_update.append("Rp0")
        df_tampil_update['Harga'] = harga_terformat_update
    print(tabulate(df_tampil_update, headers="keys", tablefmt="fancy_grid", showindex=False))
    
    input("\nTekan Enter untuk kembali...")

def hapus_data_obat(data_obat_df):
    """Menangani proses penghapusan data obat."""
    bersihkan_layar()
    if data_obat_df.empty:
        print("Data obat kosong."); input("\nTekan Enter..."); return

    df_tampil = data_obat_df.copy()
    if 'Harga' in df_tampil.columns:
        harga_terformat = []
        for harga in df_tampil['Harga']:
            if pd.notna(harga):
                harga_terformat.append(f"Rp{int(harga):,}".replace(",", "."))
            else:
                harga_terformat.append("Rp0")
        df_tampil['Harga'] = harga_terformat
    print(tabulate(df_tampil, headers="keys", tablefmt="fancy_grid", showindex=False))
    
    kode_target = input("\nMasukkan KODE obat yang akan dihapus: ").strip().upper()
    baris_target = data_obat_df[data_obat_df['Kode'].str.upper() == kode_target]

    if baris_target.empty:
        print(f"Kode obat '{kode_target}' tidak ditemukan."); time.sleep(2); return

    konfirmasi = input(f"Yakin ingin menghapus obat '{baris_target.iloc[0]['Nama']}'? (y/n): ").lower().strip()
    if konfirmasi == 'y':
        data_obat_df = data_obat_df[data_obat_df['Kode'].str.upper() != kode_target]
        data_obat_df.to_csv("database_obat.csv", index=False)
        print("Data berhasil dihapus.")
        animasi_memuat(1)
    else:
        print("Penghapusan dibatalkan.")
        time.sleep(2)

def buat_kode_transaksi():
    """Membuat kode transaksi baru secara otomatis."""
    try:
        kolom_riwayat = ["Kode Transaksi", "Tanggal Transaksi", "Nama Pembeli", "Kode Obat", "Nama Obat", "Jumlah", "Harga Satuan", "Total Harga", "Keterangan"]
        df_riwayat = muat_data_csv("riwayat_transaksi.csv", kolom_riwayat)
        if df_riwayat.empty or "Kode Transaksi" not in df_riwayat.columns: return "TRX001"
        kode_terakhir = df_riwayat["Kode Transaksi"].dropna().max()
        nomor_terakhir = int(kode_terakhir[3:])
        return f"TRX{nomor_terakhir + 1:03d}"
    except (ValueError, IndexError, TypeError):
        return f"TRX{len(df_riwayat) + 1:03d}"

def lakukan_pembelian():
    """Menangani logika untuk transaksi pembelian obat."""
    kolom_obat = ["Kode", "Nama", "Kategori", "Stok", "Harga", "Kadaluarsa", "Deskripsi"]
    data_obat_df = muat_data_csv("database_obat.csv", kolom_obat)
    if data_obat_df.empty:
        bersihkan_layar(); print("Data obat kosong."); input("\nTekan Enter..."); return

    while True:
        bersihkan_layar()
        print("\n--- Lakukan Pembelian Obat ---")
        nama_pembeli = input("Masukkan Nama Pembeli (atau 0 untuk batal): ").strip()
        if nama_pembeli == '0': break
        if not nama_pembeli:
            print("Nama pembeli tidak boleh kosong."); time.sleep(2); continue

        df_tampil = data_obat_df[['Kode', 'Nama', 'Stok', 'Harga']].copy()
        if 'Harga' in df_tampil.columns:
            harga_terformat = []
            for harga in df_tampil['Harga']:
                if pd.notna(harga):
                    harga_terformat.append(f"Rp{int(harga):,}".replace(",", "."))
                else:
                    harga_terformat.append("Rp0")
            df_tampil['Harga'] = harga_terformat
        print("\n" + tabulate(df_tampil, headers="keys", tablefmt="simple"))
        
        kode_target = input("\nMasukkan KODE obat yang dibeli: ").strip().upper()
        
        obat_terpilih = data_obat_df[data_obat_df['Kode'].str.upper() == kode_target]
        if obat_terpilih.empty:
            print("Kode tidak ditemukan."); time.sleep(2); continue
        
        obat = obat_terpilih.iloc[0]
        try:
            tanggal_kadaluarsa = datetime.strptime(obat['Kadaluarsa'], "%Y-%m-%d")
            if tanggal_kadaluarsa < datetime.now():
                print(f"Obat '{obat['Nama']}' sudah kedaluwarsa pada {obat['Kadaluarsa']}. Tidak bisa dibeli.")
                input("Tekan Enter untuk kembali..."); continue
        except (ValueError, TypeError):
             print(f"Format tanggal kadaluarsa untuk '{obat['Nama']}' tidak valid. Hubungi admin."); time.sleep(2); continue

        stok_tersedia = int(obat['Stok'])
        harga_satuan = float(obat['Harga'])
        print(f"Obat: {obat['Nama']}, Stok: {stok_tersedia}, Harga: Rp {harga_satuan:,.0f}")
        
        while True:
            jumlah_beli_str = input("Masukkan jumlah beli: ")
            try:
                jumlah_beli = int(jumlah_beli_str)
                if 0 < jumlah_beli <= stok_tersedia:
                    break
                elif jumlah_beli > stok_tersedia:
                    print("Stok tidak mencukupi.")
                else:
                    print("Jumlah harus lebih dari 0.")
            except ValueError:
                print("Jumlah harus berupa angka.")
            
        total_harga = harga_satuan * jumlah_beli
        print(f"Total harga: Rp {total_harga:,.0f}")
        
        konfirmasi = input("Lanjutkan pembayaran? (y/n): ").lower().strip()
        if konfirmasi == 'y':
            data_obat_df.loc[data_obat_df['Kode'].str.upper() == kode_target, 'Stok'] -= jumlah_beli
            data_obat_df.to_csv("database_obat.csv", index=False)
            
            kolom_riwayat = ["Kode Transaksi", "Tanggal Transaksi", "Nama Pembeli", "Kode Obat", "Nama Obat", "Jumlah", "Harga Satuan", "Total Harga", "Keterangan"]
            df_riwayat = muat_data_csv("riwayat_transaksi.csv", kolom_riwayat)

            # PERBAIKAN: Menambahkan field 'Keterangan' saat membuat transaksi baru
            transaksi_baru = {
                "Kode Transaksi": buat_kode_transaksi(), 
                "Tanggal Transaksi": datetime.now().strftime("%d-%m-%Y"), 
                "Nama Pembeli": nama_pembeli, 
                "Kode Obat": kode_target, 
                "Nama Obat": obat['Nama'], 
                "Jumlah": jumlah_beli, 
                "Harga Satuan": harga_satuan, 
                "Total Harga": total_harga,
                "Keterangan": "Pembelian" # Menambahkan nilai default
            }
            df_transaksi_baru = pd.DataFrame([transaksi_baru])
            df_riwayat = pd.concat([df_riwayat, df_transaksi_baru], ignore_index=True)
            df_riwayat.to_csv("riwayat_transaksi.csv", index=False)

            print("Pembelian berhasil dan stok telah diperbarui.")
            input("Tekan Enter untuk kembali..."); break
        else:
            print("Pembelian dibatalkan."); input("Tekan Enter..."); break

def lihat_riwayat_transaksi():
    """Menampilkan semua riwayat transaksi."""
    bersihkan_layar()
    kolom_riwayat = ["Kode Transaksi", "Tanggal Transaksi", "Nama Pembeli", "Kode Obat", "Nama Obat", "Jumlah", "Harga Satuan", "Total Harga", "Keterangan"]
    df_riwayat = muat_data_csv("riwayat_transaksi.csv", kolom_riwayat)

    if df_riwayat.empty:
        print("Belum ada riwayat transaksi.")
    else:
        print("\n--- Riwayat Transaksi ---")
        df_tampil = df_riwayat.copy()
        
        # PERBAIKAN: Mengganti nilai NaN menjadi string kosong sebelum ditampilkan
        df_tampil['Keterangan'] = df_tampil['Keterangan'].fillna('Pembelian')
        
        for kolom_harga in ["Harga Satuan", "Total Harga"]:
            if kolom_harga in df_tampil.columns:
                harga_terformat = []
                for harga in df_tampil[kolom_harga]:
                    if pd.notna(harga):
                        harga_terformat.append(f"Rp{int(harga):,}".replace(",", "."))
                    else:
                        harga_terformat.append("Rp0")
                df_tampil[kolom_harga] = harga_terformat
        
        print(tabulate(df_tampil, headers="keys", tablefmt="fancy_grid", showindex=False))
    
    input("\nTekan Enter untuk kembali...")

if __name__ == '__main__':
    """Fungsi utama yang akan dijalankan saat script dieksekusi."""
    kolom_obat = ["Kode", "Nama", "Kategori", "Stok", "Harga", "Kadaluarsa", "Deskripsi"]
    if not os.path.exists("database_obat.csv"):
        muat_data_csv("database_obat.csv", kolom_obat)

    kolom_riwayat = ["Kode Transaksi", "Tanggal Transaksi", "Nama Pembeli", "Kode Obat", "Nama Obat", "Jumlah", "Harga Satuan", "Total Harga", "Keterangan"]
    if not os.path.exists("riwayat_transaksi.csv"):
        muat_data_csv("riwayat_transaksi.csv", kolom_riwayat)
    
    menu_utama()
