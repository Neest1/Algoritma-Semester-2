import pandas as pd
import calendar
import time
import sys
import random
from datetime import datetime
import os
import csv
from halo import Halo
from tabulate import tabulate
import numpy as np
from typing import List, Any


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def load_csv(file_name):
    try:
        return pd.read_csv(file_name)
    except FileNotFoundError:
        print(f"File '{file_name}' tidak ditemukan. Cek kembali file!.")

def clear_alert(n=1):
    for _ in range(n):
        print("\033[F\033[K", end='')

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(speed):
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start()
    time.sleep(speed)  
    spinner.stop()

def menu_utama():
    print("╔═══════════════════════════════════════╗")
    print("║     Sistem Informasi Data Apotek      ║")
    print("╠═══════════════════════════════════════╣")
    print("║  [1] Login Admin                      ║")
    print("║  [2] Keluar                           ║")
    print("╚═══════════════════════════════════════╝")
    while True:
        pilih = input("Pilih menu (1/2): ")
        
        match pilih:
            case "1":
                clear_terminal()
                login_admin()
            case "2":
                print("Terima kasih! Program telah selesai.")
                clear_terminal()
                break
            case _:
                print("Input tidak valid!. Silakan pilih 1 atau 2.")
                loading_animation(3)
                clear_alert(2)
                continue

def login_admin():
    print("\n〓〓〓〓〓〓〓〓〓〓【 LOGIN ADMIN 】〓〓〓〓〓〓〓〓〓〓")
    username = input("Username: ")
    password = input("Password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        loading_animation(2)
        print("Login berhasil!")
        dashboard_admin()
    else:
        print("Username atau password salah!")
        loading_animation(2)
        clear_terminal()
        menu_utama()

def dashboard_admin():
    clear_terminal()
    print("╔═══════════════════════════════════════╗")
    print("║        Menu Admin Apotek              ║")
    print("╠═══════════════════════════════════════╣")
    print("║  [1] Tambah Data Obat                 ║")
    print("║  [2] Kelola Data Obat                 ║")
    print("║  [3] Cari Obat                        ║")
    print("║  [4] Urutkan Data Obat                ║")
    print("║  [5] Pembelian Obat                   ║")
    print("║  [6] Riwayat Transaksi                ║")
    print("║  [7] Keluar                           ║")
    print("╚═══════════════════════════════════════╝")
    while True:
        pil = input("Silahkan pilih menu (1-6) : ")
        match pil:
            case '1':
                clear_terminal()
                tambah_obat()
            case '2':
                clear_terminal()
                kelola_obat()
            case '3':
                clear_terminal()
                menu_pencarian()
            case '4':
                clear_terminal()
                menu_pengurutan()
            case '5':
                clear_terminal()
                pembelian_obat()
            case '6':
                clear_terminal()
                riwayat_transaksi()
            case '7':
                print("Terimakasih telah menggunakan sistem ini!")
                loading_animation(2)
                clear_terminal()
                menu_utama()
            case _:
                print("Input tidak valid!. Silakan pilih 1-6.")
                loading_animation(3)
                clear_alert(2)
                continue

# Binary Search implementation for medicine search
def binary_search(arr: List[Any], target: str, key: str) -> int:
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        mid_val = str(arr[mid][key]).lower()
        target = str(target).lower()
        
        if mid_val == target:
            return mid
        elif mid_val < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def quick_sort(arr: List[dict], key: str, ascending: bool = True):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    pivot_val = str(pivot[key]) if isinstance(pivot[key], str) else pivot[key]
    
    left = [x for x in arr if (str(x[key]) if isinstance(x[key], str) else x[key]) < pivot_val]
    middle = [x for x in arr if (str(x[key]) if isinstance(x[key], str) else x[key]) == pivot_val]
    right = [x for x in arr if (str(x[key]) if isinstance(x[key], str) else x[key]) > pivot_val]
    
    result = quick_sort(left, key, ascending) + middle + quick_sort(right, key, ascending)
    return result if ascending else result[::-1]

def menu_pencarian():
    try:
        df = pd.read_csv("data_obat.csv")
        print("╔═══════════════════════════════════╗")
        print("║         Menu Pencarian Obat       ║")
        print("╠═══════════════════════════════════╣")
        print("║  [1] Cari berdasarkan nama        ║")
        print("║  [2] Cari berdasarkan kode        ║")
        print("║  [3] Cari berdasarkan kategori    ║")
        print("║  [4] Kembali                      ║")
        print("╚═══════════════════════════════════╝")

        while True:
            pilihan = input("Pilih metode pencarian (1-4): ")
            if pilihan == "4":
                clear_terminal()
                return dashboard_admin()

            search_key = ""
            if pilihan == "1":
                search_key = "Nama"
                query = input("Masukkan nama obat: ")
            elif pilihan == "2":
                search_key = "Kode"
                query = input("Masukkan kode obat: ")
            elif pilihan == "3":
                search_key = "Kategori"
                query = input("Masukkan kategori obat: ")
            else:
                print("Pilihan tidak valid!")
                continue

            
            data = df.to_dict('records')
            
            
            sorted_data = quick_sort(data, search_key)
            
            
            result_idx = binary_search(sorted_data, query, search_key)
            
            if result_idx != -1:
                result = pd.DataFrame([sorted_data[result_idx]])
                print("\nHasil Pencarian:")
                print(tabulate(result, headers="keys", tablefmt="fancy_grid"))
            else:
                print(f"\nData dengan {search_key}: {query} tidak ditemukan!")
            
            input("\nTekan enter untuk melakukan pencarian lain: ")
            clear_terminal()
            return menu_pencarian()

    except FileNotFoundError:
        print("File data obat tidak ditemukan!")
        return

def menu_pengurutan():
    try:
        df = pd.read_csv("data_obat.csv")
        print("╔═══════════════════════════════════╗")
        print("║       Menu Pengurutan Data        ║")
        print("╠═══════════════════════════════════╣")
        print("║  [1] Urutkan berdasarkan nama     ║")
        print("║  [2] Urutkan berdasarkan stok     ║")
        print("║  [3] Urutkan berdasarkan harga    ║")
        print("║  [4] Urutkan berdasarkan kategori ║")
        print("║  [5] Kembali                      ║")
        print("╚═══════════════════════════════════╝")

        while True:
            pilihan = input("Pilih metode pengurutan (1-5): ")
            if pilihan == "5":
                clear_terminal()
                return dashboard_admin()

            sort_key = ""
            if pilihan == "1":
                sort_key = "Nama"
            elif pilihan == "2":
                sort_key = "Stok"
            elif pilihan == "3":
                sort_key = "Harga"
            elif pilihan == "4":
                sort_key = "Kategori"
            else:
                print("Pilihan tidak valid!")
                continue

           
            asc = input("Urutkan secara ascending? (y/n): ").lower() == 'y'
            
            
            data = df.to_dict('records')
            
            
            sorted_data = quick_sort(data, sort_key, asc)
            
            
            result_df = pd.DataFrame(sorted_data)
            
            print(f"\nData setelah diurutkan berdasarkan {sort_key}:")
            print(tabulate(result_df, headers="keys", tablefmt="fancy_grid"))
            
            input("\nTekan enter untuk melakukan pengurutan lain: ")
            clear_terminal()
            return menu_pengurutan()

    except FileNotFoundError:
        print("File data obat tidak ditemukan!")
        return

def tambah_obat():
    try:
        df = pd.read_csv("data_obat.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Kode", "Nama", "Kategori", "Stok", "Harga", "Kadaluarsa", "Deskripsi"])

    print("\n⩶⩶ Masukkan Data Obat Baru ⩶⩶")
    kode_terakhir = df["Kode"].max() if not df.empty else "OBT000"
    nomor_urut = int(kode_terakhir[3:]) + 1 if kode_terakhir else 1
    kode_obat = f"OBT{nomor_urut:03d}"
    
    while True:
        try:
            nama_obat = input("Nama Obat\t: ")
            if not nama_obat:
                print("Nama obat tidak boleh kosong!")
                continue
            
            kategori = input("Kategori\t: ")
            if not kategori:
                print("Kategori tidak boleh kosong!")
                continue
            
            stok = int(input("Stok\t\t: "))
            if stok < 0:
                print("Stok tidak boleh negatif!")
                continue
            
            harga = float(input("Harga\t\t: Rp. "))
            if harga < 0:
                print("Harga tidak boleh negatif!")
                continue
            
            while True:
                kadaluarsa = input("Kadaluarsa (DD-MM-YYYY)\t: ")
                try:
                    datetime.strptime(kadaluarsa, '%d-%m-%Y')
                    break
                except ValueError:
                    print("Format tanggal salah! Gunakan format DD-MM-YYYY")
                    continue
            
            deskripsi = input("Deskripsi\t: ")
            if not deskripsi:
                print("Deskripsi tidak boleh kosong!")
                continue
            
            break
        except ValueError:
            print("Input tidak valid! Pastikan stok dan harga berupa angka.")
            continue

    obat_baru = pd.DataFrame([{
        "Kode": kode_obat,
        "Nama": nama_obat,
        "Kategori": kategori,
        "Stok": stok,
        "Harga": harga,
        "Kadaluarsa": kadaluarsa,
        "Deskripsi": deskripsi
    }])

    df = pd.concat([df, obat_baru], ignore_index=True)
    df.to_csv("data_obat.csv", index=False)
    print("\nData obat yang ditambahkan:")
    print(tabulate(obat_baru, headers="keys", tablefmt="fancy_grid"))
    print("\n⩶⩶⩶ Data obat berhasil disimpan ⩶⩶⩶")
    
    input("\nTekan enter untuk kembali ke menu: ")
    clear_terminal()
    return dashboard_admin()

def kelola_obat():
    try:
        df = pd.read_csv('data_obat.csv')
        print("╔═══════════════════════════════════╗")
        print("║         Menu Kelola Obat          ║")
        print("╠═══════════════════════════════════╣")
        print("║  [1] Tampilkan semua obat         ║")
        print("║  [2] Update nama obat             ║")
        print("║  [3] Update kategori              ║")
        print("║  [4] Update stok                  ║")
        print("║  [5] Update harga                 ║")
        print("║  [6] Update kadaluarsa            ║")
        print("║  [7] Update deskripsi             ║")
        print("║  [8] Hapus data obat              ║")
        print("║  [9] Kembali                      ║")
        print("╚═══════════════════════════════════╝")

        while True:
            pil = input("Silahkan pilih menu (1-9): ")
            match pil:
                case "1":
                    tampilkan_obat()
                    input("\nTekan enter untuk kembali ke menu: ")
                    clear_terminal()
                    kelola_obat()
                case "2":
                    update_data_obat("Nama")
                case "3":
                    update_data_obat("Kategori")
                case "4":
                    update_data_obat("Stok")
                case "5":
                    update_data_obat("Harga")
                case "6":
                    update_data_obat("Kadaluarsa")
                case "7":
                    update_data_obat("Deskripsi")
                case "8":
                    hapus_obat()
                case "9":
                    clear_terminal()
                    dashboard_admin()
                case _:
                    print("Input tidak valid! Silakan pilih 1-9.")
                    loading_animation(3)
                    clear_alert(2)
    except FileNotFoundError:
        print("File data obat tidak ditemukan!")
        df = pd.DataFrame(columns=["Kode", "Nama", "Kategori", "Stok", "Harga", "Kadaluarsa", "Deskripsi"])
        df.to_csv("data_obat.csv", index=False)
        return kelola_obat()

def update_data_obat(field):
    try:
        df = pd.read_csv("data_obat.csv")
        print(f"\n〓〓〓〓〓〓〓〓〓〓 Update {field} Obat 〓〓〓〓〓〓〓〓〓〓")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
        
        while True:
            kode_obat = input("\nMasukkan kode obat (input [0] untuk kembali): ")
            if kode_obat == "0":
                clear_terminal()
                return kelola_obat()
            
            if kode_obat in df["Kode"].values:
                try:
                    if field in ["Stok", "Harga"]:
                        nilai_baru = float(input(f"Masukkan {field} baru: "))
                        if nilai_baru < 0:
                            print(f"{field} tidak boleh negatif!")
                            continue
                    elif field == "Kadaluarsa":
                        while True:
                            nilai_baru = input(f"Masukkan {field} baru (DD-MM-YYYY): ")
                            try:
                                datetime.strptime(nilai_baru, '%d-%m-%Y')
                                break
                            except ValueError:
                                print("Format tanggal salah! Gunakan format DD-MM-YYYY")
                                continue
                    else:
                        nilai_baru = input(f"Masukkan {field} baru: ")
                        if not nilai_baru:
                            print(f"{field} tidak boleh kosong!")
                            continue
                    
                    df.loc[df["Kode"] == kode_obat, field] = nilai_baru
                    df.to_csv("data_obat.csv", index=False)
                    print(f"\n{field} berhasil diperbarui")
                    print("\nData setelah diperbarui:")
                    print(tabulate(df[df["Kode"] == kode_obat], headers="keys", tablefmt="fancy_grid"))
                    input("\nTekan enter untuk kembali ke menu: ")
                    clear_terminal()
                    return kelola_obat()
                except ValueError:
                    print("Input tidak valid!")
                    continue
            else:
                print(f"Kode obat {kode_obat} tidak ditemukan")
                loading_animation(3)
                clear_alert(2)
    except FileNotFoundError:
        print("File data obat tidak ditemukan!")
        return

def hapus_obat():
    try:
        df = pd.read_csv("data_obat.csv")
        print("\n〓〓〓〓〓〓〓〓〓〓 Hapus Data Obat 〓〓〓〓〓〓〓〓〓〓")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
        
        while True:
            kode_obat = input("\nMasukkan kode obat yang akan dihapus (input [0] untuk batal): ")
            if kode_obat == "0":
                clear_terminal()
                return kelola_obat()
            
            if kode_obat in df["Kode"].values:
                konfirmasi = input("Anda yakin ingin menghapus data ini? (y/n): ").lower()
                if konfirmasi == 'y':
                    df = df[df["Kode"] != kode_obat]
                    df.to_csv("data_obat.csv", index=False)
                    print("\nData obat berhasil dihapus")
                    input("\nTekan enter untuk kembali ke menu: ")
                    clear_terminal()
                    return kelola_obat()
                else:
                    print("Penghapusan dibatalkan")
                    loading_animation(3)
                    clear_terminal()
                    return kelola_obat()
            else:
                print(f"Kode obat {kode_obat} tidak ditemukan")
                loading_animation(3)
                clear_alert(2)
    except FileNotFoundError:
        print("File data obat tidak ditemukan!")
        return

def tampilkan_obat():
    try:
        df = pd.read_csv("data_obat.csv")
        pd.set_option('display.float_format', '{:,.2f}'.format)
        print("\n〓〓〓〓〓〓〓〓〓〓 Daftar Obat 〓〓〓〓〓〓〓〓〓〓")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
    except FileNotFoundError:
        print("File data obat tidak ditemukan!")
        return
    
def generate_kode_transaksi():
    try:
        df = pd.read_csv("riwayat_transaksi.csv")
        last_kode = df["Kode Transaksi"].iloc[-1]
        nomor = int(last_kode.replace("TRX", "")) + 1
        return f"TRX{nomor:03}"
    except:
        return "TRX001"

def pembelian_obat():
    df_obat = pd.read_csv("data_obat.csv")
    df_obat["Nama"] = df_obat["Nama"].astype(str)

    nama_cari = input("Masukkan nama obat yang ingin dicari : ").strip().lower()

    hasil = df_obat[df_obat["Nama"].str.lower().str.contains(nama_cari)].copy()

    if hasil.empty:
        print("Tidak ditemukan obat dengan nama tersebut.")
        input("\nTekan enter untuk kembali ke menu: ")
        clear_terminal()
        return dashboard_admin()
    

    hasil = hasil.sort_values(by="Stok", ascending=False)
    hasil_reset = hasil.reset_index(drop=True)
    hasil_reset.index += 1

    print("\n〓〓〓〓〓〓〓〓〓〓 Hasil Pencarian Obat 〓〓〓〓〓〓〓〓〓〓")
    print(tabulate(hasil_reset[["Nama", "Kode", "Stok", "Harga"]], headers="keys", tablefmt="fancy_grid"))

    kode_obat = input("Masukkan KODE OBAT yang ingin dibeli: ").strip().upper()
    if kode_obat not in hasil["Kode"].values:
        print("Kode obat tidak sesuai dengan hasil pencarian.")
        input("\nTekan enter untuk kembali ke menu: ")
        clear_terminal()
        return dashboard_admin()

    obat_dipilih = hasil[hasil["Kode"] == kode_obat].iloc[0]
    
    try:
        jumlah = int(input(f"Masukkan jumlah (Stok tersedia {obat_dipilih['Stok']}): "))
        if jumlah <= 0 or jumlah > obat_dipilih["Stok"]:
            print("Jumlah tidak valid.")
            return
    except ValueError:
        print("Input jumlah harus berupa angka.")
        return

    total_harga = obat_dipilih["Harga"] * jumlah

    print(f"\n Total yang harus dibayar: Rp{obat_dipilih['Harga']:.2f} x {jumlah} = Rp{total_harga:.2f}")

    
    try:
        df_riwayat = pd.read_csv("riwayat_transaksi.csv")
    except FileNotFoundError:
        df_riwayat = pd.DataFrame(columns=["Kode Transaksi", "Kode Obat", "Nama Obat", "Jumlah", "Tanggal Transaksi", "Harga Satuan", "Total Harga", "Keterangan"])

    nomor_terakhir = 0
    if not df_riwayat.empty:
        nomor_terakhir = int(df_riwayat["Kode Transaksi"].str.extract(r'(\d+)').dropna().astype(int).max().iloc[0])

    kode_transaksi = f"TRX{nomor_terakhir+1:03}"
    tanggal = datetime.now().strftime("%Y-%m-%d")

    data = {
        "Kode Transaksi": [kode_transaksi],
        "Kode Obat": [obat_dipilih["Kode"]],
        "Nama Obat": [obat_dipilih["Nama"]],
        "Jumlah": [jumlah],
        "Tanggal Transaksi": [tanggal],
        "Harga Satuan": [obat_dipilih["Harga"]],
        "Total Harga": [total_harga],
        "Keterangan": ["Pembelian"]
    }

    df_riwayat = pd.concat([df_riwayat, pd.DataFrame(data)], ignore_index=True)
    df_riwayat.to_csv("riwayat_transaksi.csv", index=False)

   
    df_obat.loc[df_obat["Kode"] == kode_obat, "Stok"] -= jumlah
    df_obat.to_csv("data_obat.csv", index=False)

    print("\n Transaksi berhasil disimpan.")
    input("\nTekan enter untuk kembali ke menu: ")
    clear_terminal()
    return dashboard_admin()

def riwayat_transaksi():
    try:
        df_transaksi = pd.read_csv("riwayat_transaksi.csv")
        print("\n〓〓〓〓〓〓〓〓〓〓 Riwayat Transaksi 〓〓〓〓〓〓〓〓〓〓")
        print(tabulate(df_transaksi, headers="keys", tablefmt="fancy_grid"))
        input("\nTekan enter untuk kembali ke menu: ")
        clear_terminal()
        return dashboard_admin()
    except FileNotFoundError:
        print("Belum ada riwayat transaksi!")
        loading_animation(3)
        return dashboard_admin()
