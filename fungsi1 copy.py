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

USN = "adminevent@gmail.com"
PW = "admin321"
login = True
rincian_acara = None
akun_user = None
riwayat_transaksi = None

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
# file_name = "akun_user.csv"

def loading_animation(speed):
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start()

    time.sleep(speed)  
    spinner.stop()

def menu_utama():
    print("╔═══════════════════════════════════╗")
    print("║  iTick : Anti ribet, Anti ruwet!  ║")
    print("╠═══════════════════════════════════╣")
    print("║  [1] Mendaftar                    ║")
    print("║  [2] Masuk                        ║")
    print("║  [3] Keluar                       ║")
    print("╚═══════════════════════════════════╝")
    while True:
        pilih = input("Pilih menu (1/2/3): ")
        
        match pilih:
            case "1":
                clear_terminal()
                register()
            case "2":
                clear_terminal()
                login_user()
            case "3":
                print("Terima kasih! Program telah selesai.")
                clear_terminal()
                break
            case _:
                print("Input tidak valid!. Silakan pilih 1, 2, atau 3.")
                loading_animation(3)
                clear_alert(2)
                continue

def simpan_akun(nama, nik, email, password, role):
    df_akun = pd.read_csv('akun_user.csv')
    
    rincian_baru = pd.DataFrame([{
        'Nama': nama, 
        'NIK': nik, 
        'Email': email, 
        'Password': password, 
        'Role': role
    }])
    
    df_akun = pd.concat([df_akun, rincian_baru], ignore_index=True)
    
    df_akun.to_csv('akun_user.csv', index=False)

def register():
    df=load_csv('akun_user.csv')
    print("〓〓〓〓〓〓〓〓〓〓【 REGISTER 】〓〓〓〓〓〓〓〓〓〓")
    while True:
        nama = input("Masukkan nama anda (input [x] untuk batal)\t: ").strip()
        if not nama:
            print("Nama tidak boleh kosong")
            loading_animation(5)
            clear_alert(2)
            continue
        if not all(Karakter.isalpha() or Karakter.isspace() for Karakter in nama):
            print("Nama harus berupa huruf")
            loading_animation(5)
            clear_alert(2)
            continue
        elif nama == "x":
            print("Pendaftaran dibatalkan")
            loading_animation(3)
            clear_terminal()
            return menu_utama()
        else:
            break
        
    df_akun = pd.read_csv('akun_user.csv')
    df_akun['NIK'] = df_akun['NIK'].astype(str)  

    while True:
        nik = input("Masukkan NIK anda (input [x] untuk batal)\t: ").strip()
        if not nik:
            print("Nik tidak boleh kosong")
            loading_animation(5)
            clear_alert(2)
            continue
        elif not nik.isdigit():
            print("NIK tidak boleh berisi huruf")
            loading_animation(5)
            clear_alert(2)
            continue
        elif len(nik) != 16:
            print("NIK harus berisi 16 digit angka")
            loading_animation(5)
            clear_alert(2)
            continue
        elif nik in df_akun['NIK'].values:
            print("NIK ini sudah terdaftar. Silahkan masukkan NIK baru.")
            loading_animation(5)
            clear_alert(2)
            continue
        elif nik == "x":
            print("Pendaftaran dibatalkan")
            loading_animation(3)
            clear_terminal()
            return menu_utama()
        else:
            break

    while True:
        email = input("Masukkan email anda (input [x] untuk batal)\t: ").lower().strip()
        
        if not email:
            print("Email tidak boleh kosong!")
            loading_animation(5)
            clear_alert(2)
            continue
        elif not email.endswith("@gmail.com"):
            print("Email harus menggunakan @gmail.com")
            loading_animation(5)
            clear_alert(2)
            continue
        elif email in df_akun['Email'].values:
            print(f"Email {email} sudah terdaftar, silakan masukkan email lain.")
            loading_animation(5)
            clear_alert(2)
            continue
        elif email == "x":
            print("Pendaftaran dibatalkan")
            loading_animation(3)
            clear_terminal()
            return menu_utama()
        else:
            break

    while True:
        password = input("Masukkan password kamu (input [x] untuk batal)\t: ").strip()
        if not password:
            print("Password tidak boleh kosong!")
            loading_animation(5)
            clear_alert(2)
            continue
        elif password == "x":
            print("Pendaftaran dibatalkan")
            loading_animation(3)
            clear_terminal()
            return menu_utama()
        else:
            break


    role = "User"
    clear_terminal()
    
    preview(nama, nik, email, password)
    print("[y] Konfirmasi\n[n] Ulang\n[x] Batalkan")
    while True:
        konfir = input('Cek kembali data anda!, Masukkan pilihan : ').lower().strip()
        
        if konfir == 'y':
            simpan_akun(nama, nik, email, password, role)
            print("Pendaftaran berhasil, Tunggu hingga diarahkan ke menu utama")
            loading_animation(5)
            clear_terminal()
            menu_utama(df)
            break
        elif konfir == 'n':
            loading_animation(5)
            clear_terminal()
            return register()
        elif konfir == "x":
            print("Pendaftaran dibatalkan")
            loading_animation(3)
            clear_terminal()
            return menu_utama()
        else:
            print("Input tidak valid!")
            loading_animation(5)
            clear_alert(2)
            continue

def preview(nama, nik, email, password):
    """Display a preview of the user data."""
    print("╔═════════════════════════════════════════╗")
    print("║                DATA AKUN                ║")
    print("╠═════════════════════════════════════════╣")
    print("  Nama\t\t:", nama)
    print("  NIK\t\t:", nik)
    print("  Email\t\t:", email)
    print("  Password\t:", password)
    print("╚═════════════════════════════════════════╝")

def cek_file(file):
    """Membaca file dan mengecek apakah file tersebut ada"""
    loading_animation()
    try:
        return pd.read_csv(f"{file}")
    except FileNotFoundError:
        print("File data base event tidak ditemukan. \nSilahkan periksa kembali nama dan lokasinya.")
        sys.exit()

def simpan_data(df):
    if not os.path.exists("rincian_acara.csv"):
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.to_csv("rincian_acara.csv", index=False, header=True)
    else:
        df.to_csv("rincian_acara.csv", index=False)

def dashboard_admin(df):
    clear_terminal()

    print("╔═══════════════════════════════════╗")
    print("║  iTick : Anti ribet, Anti ruwet!  ║")
    print("╠═══════════════════════════════════╣")
    print("║  [1] Membuat acara                ║")
    print("║  [2] Kelola acara                 ║")
    print("║  [3] Riwayat transaksi            ║")
    print("║  [4] Keluar                       ║")
    print("╚═══════════════════════════════════╝")

    while True:
        pil = input("Silahkan pilih menu (1/2/3/4) : ")

        match pil:
            case '1':
                clear_terminal()
                buat_acara()
            case '2':
                clear_terminal()
                kelola_acara(df)
            case '3':
                clear_terminal()
                riwayat_transaksi(df)
            case '4':
                print("Terimakasih telah menggunakan sistem ini!")
                loading_animation(5)
                clear_terminal()
                menu_utama(df)
            case _:
                print("Input tidak valid!. Silakan pilih 1, 2, 3, atau 4.")
                loading_animation(5)
                clear_alert(2)
                continue


def buat_acara():
    global kode_acara
    try:
        df = pd.read_csv("rincian_acara.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Kode", "Acara", "Guest Star", "Tempat", "Jadwal", "Harga Tiket", "Stok Tiket"])

    print("\n⩶⩶ Masukkan rincian acara ⩶⩶")
    kode_acara_terakhir = df["Kode"].max() if not df.empty else 110 
    kode_acara = kode_acara_terakhir + 1
    nama_acara = input("Acara\t\t: ")
    guest_star = input("Guest Star\t: ")
    tempat_acara = input("Tempat\t\t: ")
    jadwal_acara = input("Jadwal\t\t: ")
    harga_tiket = input("Harga Tiket\t: Rp. ")
    stok_tiket = int(input("Stok Tiket\t: "))

    pd.set_option('display.float_format', '{:,.2f}'.format)

    rincian_baru = pd.DataFrame([{
        "Kode": kode_acara,
        "Acara": nama_acara,
        "Guest Star": guest_star,
        "Tempat": tempat_acara,
        "Jadwal": jadwal_acara,
        "Harga Tiket": harga_tiket,
        "Stok Tiket": stok_tiket
            }])

    df = pd.concat([df, rincian_baru], ignore_index=True)
    simpan_data(df)  
    print(tabulate(rincian_baru, headers="keys", tablefmt="fancy_grid"))
    print("\n⩶⩶⩶ Rincian acara berhasil disimpan.⩶⩶⩶")

def kelola_acara():
    df = load_csv('rincian_acara.csv')
    print("╔═══════════════════════════════════╗")
    print("║         Menu Kelola Event         ║")
    print("╠═══════════════════════════════════╣")
    print("║  [1] Tampilkan jadwal acara       ║")
    print("║  [2] Pembaruan nama acara         ║")
    print("║  [3] Pembaruan guest star         ║")
    print("║  [4] Pembaruan tempat acara       ║")
    print("║  [5] Pembaruan jadwal acara       ║")
    print("║  [6] Pembaruan harga tiket        ║")
    print("║  [7] Pembaruan stok tiket         ║")
    print("║  [8] Keluar                       ║")
    print("╚═══════════════════════════════════╝")

    while True:
        pil = input("Silahkan pilih menu (1/2/dst) : ")

        match pil:
            case "1":
                clear_alert(13)
                pd.set_option('display.float_format', '{:,.2f}'.format)
                print("\n〓〓〓〓〓〓〓〓〓〓 Jadwal Acara 〓〓〓〓〓〓〓〓〓〓")
                print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
                kelola_acara(df)
            case "2":
                clear_alert(13)
                pd.set_option('display.float_format', '{:,.2f}'.format)
                print("\n〓〓〓〓〓〓〓〓〓〓 Pembaruan Nama Acara 〓〓〓〓〓〓〓〓〓〓")
                
                while True:
                    try:
                        kode_acara = int(input("Masukkan kode acara (input [0] untuk kembali)\t: "))
                        if kode_acara in df["Kode"].values:
                            nama_acara = input("Masukkan nama acara baru\t: ")
                            df.loc[df["Kode"] == kode_acara, "Acara"] = nama_acara
                            simpan_data(df)
                            print(f"\nGuest Star berhasil diperbarui menjadi {nama_acara}")
                            print("\nRincian baru setelah di update: ")
                            print(tabulate(df[df["Kode"] == kode_acara], headers="keys", tablefmt="fancy_grid"))
                            print("")
                            input("Tekan enter untuk kembali ke menu : ")
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        elif kode_acara == "0":
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        else:
                            print(f"Kode {kode_acara} tidak ditemukan.")
                            loading_animation(3)
                            clear_alert(2)
                            continue
                    except ValueError:
                        print("Input tidak valid!")
                        loading_animation(3)
                        clear_alert(2)
                        continue

            case "3":
                clear_alert(13)
                pd.set_option('display.float_format', '{:,.2f}'.format)
                print("\n〓〓〓〓〓〓〓〓〓〓 Pembaruan Guest Star 〓〓〓〓〓〓〓〓〓〓")

                while True:
                    try:
                        kode_acara = int(input("Masukkan kode acara (input [0] untuk kembali)\t: "))
                        if kode_acara in df["Kode"].values:
                            update_gs = input("Masukkan guest star baru\t: ")
                            df.loc[df["Kode"] == kode_acara, "Guest Star"] = update_gs
                            simpan_data(df)
                            print(f"\nGuest Star berhasil diperbarui menjadi {update_gs}")
                            print("\nRincian baru setelah di update: ")
                            print(tabulate(df[df["Kode"] == kode_acara], headers="keys", tablefmt="fancy_grid"))
                            print("")
                            input("Tekan enter untuk kembali ke menu : ")
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        elif kode_acara == 0:
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        else:
                            print(f"Kode {kode_acara} tidak ditemukan.")
                            loading_animation(3)
                            clear_alert(2)
                            continue
                    except ValueError:
                        print("Input tidak valid!")
                        loading_animation(3)
                        clear_alert(2)
                        continue

            case "4":
                clear_alert(13)
                pd.set_option('display.float_format', '{:,.2f}'.format)
                print("\n〓〓〓〓〓〓〓〓〓〓 Pembaruan Tempat Acara 〓〓〓〓〓〓〓〓〓〓")

                while True:
                    try:
                        kode_acara = int(input("Masukkan kode acara (input [0] untuk kembali)\t: "))
                        if kode_acara in df["Kode"].values:
                            update_tempat = input("Masukkan tempat baru\t: ")
                            df.loc[df["Kode"] == kode_acara, "Tempat"] = update_tempat
                            simpan_data(df)
                            print(f"\nTempat acara berhasil diperbarui menjadi {update_tempat}")
                            print("\nRincian baru setelah di update: ")
                            print(tabulate(df[df["Kode"] == kode_acara], headers="keys", tablefmt="fancy_grid"))
                            print("")
                            input("Tekan enter untuk kembali ke menu : ")
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        elif kode_acara == 0:
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        else:
                            print(f"Kode {kode_acara} tidak ditemukan.")
                            loading_animation(3)
                            clear_alert(2)
                            continue
                    except ValueError:
                        print("Input tidak valid!")
                        loading_animation(3)
                        clear_alert(2)
                        continue

            case "5":
                clear_alert(13)
                pd.set_option('display.float_format', '{:,.2f}'.format)
                print("\n〓〓〓〓〓〓〓〓〓〓 Pembaruan Jadwal Acara 〓〓〓〓〓〓〓〓〓〓")

                while True:
                    try:
                        kode_acara = int(input("Masukkan kode acara (input [0] untuk kembali)\t: "))
                        if kode_acara in df["Kode"].values:
                            update_jadwal = input("Masukkan jadwal baru\t: ")
                            df.loc[df["Kode"] == kode_acara, "Jadwal"] = update_jadwal
                            simpan_data(df)
                            print(f"\nJadwal acara berhasil diperbarui menjadi {update_jadwal}")
                            print("\nRincian baru setelah di update: ")
                            print(tabulate(df[df["Kode"] == kode_acara], headers="keys", tablefmt="fancy_grid"))
                            print("")
                            input("Tekan enter untuk kembali ke menu : ")
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        elif kode_acara == 0:
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        else:
                            print(f"Kode {kode_acara} tidak ditemukan.")
                            loading_animation(3)
                            clear_alert(2)
                            continue
                    except ValueError:
                        print("Input tidak valid!")
                        loading_animation(3)
                        clear_alert(2)
                        continue

            case "6":
                clear_alert(13)
                pd.set_option('display.float_format', '{:,.2f}'.format)
                print("\n〓〓〓〓〓〓〓〓〓〓 Pembaruan Harga Tiket 〓〓〓〓〓〓〓〓〓〓")

                while True:
                    try:
                        kode_acara = int(input("Masukkan kode acara (input [0] untuk kembali)\t: "))
                        if kode_acara in df["Kode"].values:
                            update_harga = input("Masukkan harga tiket\t: ")
                            df.loc[df["Kode"] == kode_acara, "Harga Tiket"] = update_harga
                            simpan_data(df)
                            print(f"\nHarga tiket berhasil diperbarui menjadi {update_harga}")
                            print("\nRincian baru setelah di update: ")
                            print(tabulate(df[df["Kode"] == kode_acara], headers="keys", tablefmt="fancy_grid"))
                            print("")
                            input("Tekan enter untuk kembali ke menu : ")
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        elif kode_acara == 0:
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        else:
                            print(f"Kode {kode_acara} tidak ditemukan.")
                            loading_animation(3)
                            clear_alert(2)
                            continue
                    except ValueError:
                        print("Input tidak valid!")
                        loading_animation(3)
                        clear_alert(2)
                        continue

            case "7":
                clear_alert(13)
                pd.set_option('display.float_format', '{:,.2f}'.format)
                print("\n〓〓〓〓〓〓〓〓〓〓 Pembaruan Stok Tiket 〓〓〓〓〓〓〓〓〓〓")
                while True:
                    try:
                        kode_acara = int(input("Masukkan kode acara (input [0] untuk kembali)\t: "))
                        if kode_acara in df["Kode"].values:
                            update_stok = int(input("Masukkan stok baru\t: "))
                            df.loc[df["Kode"] == kode_acara, "Stok Tiket"] = update_stok
                            simpan_data(df)
                            print(f"\nStok tiket berhasil diperbarui menjadi {update_stok}")
                            print("\nRincian baru setelah di update: ")
                            print(tabulate(df[df["Kode"] == kode_acara], headers="keys", tablefmt="fancy_grid"))
                            print("")
                            input("Tekan enter untuk kembali ke menu : ")
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        elif kode_acara == 0:
                            loading_animation(2)
                            clear_terminal()
                            return kelola_acara(df)
                        else:
                            print(f"Kode {kode_acara} tidak ditemukan.")
                            loading_animation(3)
                            clear_alert(2)
                            continue
                    except ValueError:
                        print("Input tidak valid!")
                        loading_animation(3)
                        clear_alert(2)
                        continue
            case "8":
                print("Terima kasih!")
                clear_terminal()
                dashboard_admin()
            case _:
                print("Input tidak valid!. Silakan pilih 1, 2, 3, dst.")
                loading_animation(5)
                clear_alert(2)
                continue

def login_user():
    login = True
    global email_login
    df=load_csv('akun_user')
    while login:
        print("\n〓〓〓〓〓〓〓〓〓〓【 LOGIN 】〓〓〓〓〓〓〓〓〓〓")
        email_login = input("Masukkan email\t\t: ")
        password_login = input("Masukkan password\t: ")

        with open("akun_user.csv", "r") as file:
            reader = csv.DictReader(file)
            valid = any(row["Email"] == email_login and row["Password"] == password_login for row in reader)
        if valid:
                loading_animation(3)
                print("〖 Login berhasil!. Halo, selamat datang! 〗")
                dashboard_user()
                break
        elif email_login == USN and password_login == PW:
                loading_animation(3)
                print("〖 Login berhasil!. Halo admin! 〗")
                dashboard_admin()
        else:
                loading_animation(3)
                print("⟪ Email atau password salah! ⟫")

def tampilkan_acara():
        df = pd.read_csv("rincian_acara.csv")
        pd.set_option('display.float_format', '{:,.2f}'.format)
        print("\n〓〓〓〓〓〓〓〓〓〓 Daftar Acara 〓〓〓〓〓〓〓〓〓〓")
        print(tabulate(df, headers="keys", tablefmt="fancy_grid", showindex=False))
        
def dashboard_user(df):
    global email_login
    global acara_bulan_ini
    df = pd.read_csv("rincian_acara.csv")
    clear_terminal()

    print("╔═════════════════════════════════╗")
    print("║           Daftar Menu           ║")
    print("╠═════════════════════════════════╣")
    print("║  [1] Tampilkan Semua Acara      ║")
    print("║  [2] Pesan Tiket                ║")
    print("║  [3] Cek Kalender               ║")
    print("║  [4] Batalkan Tiket             ║")
    print("║  [5] Riwayat Transaksi          ║")
    print("║  [6] Keluar                     ║")
    print("╚═════════════════════════════════╝")
    while True:       
        pil = input("\nMasukkan pilihan anda (1-6): ")
        match pil:
            case "1":
                tampilkan_acara()
                input("Tekan enter untuk kembali ke menu: ")
                clear_terminal()
                dashboard_user(df)
            case "2":
                clear_terminal()
                pesan_tiket()
            case "3":
                clear_terminal()
                tahun = input("Masukkan tahun (kosongkan untuk tahun ini): ") or None
                bulan = input("Masukkan bulan (kosongkan untuk bulan ini): ") or None
                acara_bulan_ini(df, tahun=int(tahun) if tahun else None, bulan=int(bulan) if bulan else None)
            case "4":
                clear_terminal()
                batalkan_tiket(df)
            case "5":
                clear_terminal()
                cek_transaksi()
            case "6":
                print("Terima kasih telah menggunakan sistem!.")
                clear_terminal()
                menu_utama(df)
                break
            case _:
                print("Input tidak valid!. Silahkan pilih 1, 2, dst.")
                loading_animation(5)
                clear_alert(2)
                continue

def pesan_tiket():
    global email_login

    try:
        riwayat_transaksi = pd.read_csv("riwayat_transaksi.csv")
    except FileNotFoundError:
        riwayat_transaksi = pd.DataFrame(columns=["Nomor Resi", "UserID", "Acara"])

    try:
        rincian_acara = pd.read_csv("rincian_acara.csv")
    except FileNotFoundError:
        print("File rincian acara tidak ditemukan!")
        return
    
    print(f"\n{'='*41} Daftar Acara {'='*41}\n")
    df = pd.read_csv('rincian_acara.csv')
    df_pembelian = pd.read_csv('riwayat_transaksi.csv')
    headers = ["Kode", "Nama", "Guest Star", "Tempat", "Jadwal", "Harga Tiket", "Stok Tiket"]
    print(tabulate(df, headers=headers, tablefmt="fancy_grid"))
    
    pilih_acara = int(input("\nMasukkan kode pilihan kamu: "))
    if pilih_acara in df['Kode'].values:
            acara_dipilih = df[df["Kode"] == pilih_acara].iloc[0]
            stok_tiket = acara_dipilih["Stok Tiket"]
            tanggal_acara = acara_dipilih["Jadwal"]

            tanggal_acara_datetime = datetime.strptime(tanggal_acara, "%d-%m-%Y")
            today = datetime.now()

            if today > tanggal_acara_datetime:
                print("⟪ Tiket tidak dapat dipesan karena acara sudah berlangsung. ⟫")
                return

            if df_pembelian[df_pembelian['UserID'] == email_login].empty:
                print("⟪ Anda belum membeli tiket untuk acara ini. ⟫")
            else:
                print(f"⟪ Anda sudah membeli tiket untuk acara ini. ⟫")
                return
                 
            if stok_tiket <= 0:
                 print("=== \nTiket habis. ===")
            else:
                 if df_pembelian[df_pembelian['UserID'] == email_login].empty:
                    df_pembelian.to_csv('riwayat_transaksi.csv', index=False) 
                    print(f"\n{'='*30} Detail Pesanan {'='*30}\n")

                    for kolom, nilai in acara_dipilih.items():
                        if kolom != "Stok Tiket":
                            print(f"{kolom}: {nilai}")
    else:
            print("⟪ Kode acara tidak ditemukan. ⟫")
        
    transaksi_user = riwayat_transaksi[riwayat_transaksi["UserID"] == email_login]
    if not transaksi_user[transaksi_user["UserID"] == pilih_acara].empty:
        print("⟪ Anda sudah membeli tiket dengan kode ini! ⟫")
        return

    konfirmasi = input("Apakah anda yakin ingin membeli tiket?(y/n): ")
    if konfirmasi == "y":
        rincian_acara.loc[rincian_acara["Kode"] == pilih_acara, "Stok Tiket"] -= 1
        metode_pembayaran()

    rincian_acara.to_csv("rincian_acara.csv", index=False)
    riwayat_transaksi.to_csv("riwayat_transaksi.csv", index=False)
    clear_terminal

def metode_pembayaran():
        global email_login
        global nomor_resi
        global transaksi_baru
        while True:
                print(f"\n{'='*30} Pilih metode pembayaran {'='*30}")
                print("[1] Cash\n[2] Transfer")
                metode_pembayaran = int(input("Masukkan nomor pilihan kamu: "))
                if metode_pembayaran == 1:
                    print("╔═══════════════════════════════════════════════════════════════╗")
                    print("║     Anda bisa melakukan pembayaran sambil penukaran tiket.    ║")
                    print("║   Kode tiket anda akan diberikan setelah pembayaran langsung  ║")
                    print("╚═══════════════════════════════════════════════════════════════╝")
                    return
                elif metode_pembayaran == 2:
                    try:
                        riwayat_transaksi = pd.read_csv("riwayat_transaksi.csv")
                    except FileNotFoundError:
                        riwayat_transaksi = pd.DataFrame(columns=["UserID", "Acara", "Nomor Resi", "Tanggal", "Jumlah Bayar", "Status"])
                        riwayat_transaksi.to_csv("riwayat_transaksi.csv", index=False)
                    
                    try:
                        back = input("Input [0] untuk membatalkan atau [1] untuk input kode acara untuk melakukan transaksi: ")
                        if back == '1':
                             kode_acara = int(input("Masukkan kode acara\t: "))
                        elif back == '0':
                             return pesan_tiket()
                        else:
                             print("=== Inputan salah! ===")
                             clear_alert(2)
                    except ValueError:
                         print("\n⟪ Kode acara tidak ditemukan. ⟫")
                         return
                    
                    df = pd.read_csv("rincian_acara.csv")

                    if kode_acara in df["Kode"].values:
                        harga_tiket = df.loc[df["Kode"] == kode_acara, "Harga Tiket"].values[0]
                        print(f"\nSilahkan melakukan pembayaran melalui Virtual Account dengan kode [111154958498] dengan nominal {harga_tiket}")
                        konfirmasi = input("Ketik 'bayar' jika sudah melakukan pembayaran: ").strip().lower()
                        
                        if konfirmasi == "bayar":
                            nama_acara = df.loc[df["Kode"] == kode_acara, "Acara"].values[0]
                            nomor_resi = f"{random.randint(1000000000, 9999999999)}"
                            tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                            harga_tiket = df.loc[df["Kode"] == kode_acara, "Harga Tiket"].values[0]
                            status = "Berhasil"
                
                            transaksi_baru = {
                                "UserID": email_login,
                                "Acara": nama_acara,
                                "Nomor Resi": nomor_resi,
                                "Tanggal": tanggal,
                                "Jumlah Bayar": harga_tiket,
                                "Status": status,
                            }
                            riwayat_transaksi = pd.concat([riwayat_transaksi, pd.DataFrame([transaksi_baru])])
                            df.loc[df["Kode"] == kode_acara, "Stok Tiket"] -= 1
                            df.to_csv("rincian_acara.csv", index=False)
                            riwayat_transaksi.to_csv("riwayat_transaksi.csv", index=False)
                            print("\n⟪ Pembayaran berhasil diproses. ⟫")
                            input("\nTekan Enter untuk kembali ke menu utama...")
                            return dashboard_user(df)
                        else:
                            print("\n⟪ Pembayaran belum dikonfirmasi. ⟫")    
                else:
                    print("\n⟪ Pilihan tidak valid. Coba lagi. ⟫")

def acara_bulan_ini(df, tahun=None, bulan=None):
    try:
        df = pd.read_csv("rincian_acara.csv")
    except FileNotFoundError:
        print("File 'rincian_acara.csv' tidak ditemukan.")
        return
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    tahun = tahun or current_year
    bulan = bulan or current_month
    
    print(f"\nKalender bulan {bulan} tahun {tahun}:\n")
    print(calendar.month(tahun,bulan))

    try:
        df["Jadwal"] = pd.to_datetime(df["Jadwal"], errors="coerce")
    except KeyError:
        print("\nKolom 'Jadwal' tidak ditemukan pada data.")
        return

    acara_bulan = df[(df["Jadwal"].dt.year == tahun) & 
                     (df["Jadwal"].dt.month == bulan)]

    if not acara_bulan.empty:
        print(f"\nDaftar acara pada bulan {bulan} tahun {tahun}:\n")
        print(tabulate(acara_bulan, headers="keys", tablefmt="fancy_grid"))
    else:
        print(f"\n⟪ Tidak ada acara yang tersedia pada bulan {bulan} tahun {tahun}. ⟫\n")

    print("\n[1] Kembali ke Menu Utama")
    clear_alert(3)

def batalkan_tiket(df):
    global email_login
 
    try:
        riwayat_transaksi = pd.read_csv("riwayat_transaksi.csv")
    except FileNotFoundError:
        print("Belum ada riwayat transaksi!")
        loading_animation()
        return

    try:
        rincian_acara = pd.read_csv("rincian_acara.csv")
    except FileNotFoundError:
        print("File rincian acara tidak ditemukan!")
        return
    
    riwayat_transaksi['Nomor Resi'] = riwayat_transaksi['Nomor Resi'].astype(str)
    transaksi_user = riwayat_transaksi[riwayat_transaksi["UserID"] == email_login]
    
    print("╔══════════════════════════════════════════════════════╗")
    print("║                   Riwayat Transaksi                  ║")
    print("╠══════════════════════════════════════════════════════╣")
    for index, transaksi in transaksi_user.iterrows():
        print(f"   {index+1}.   Nomor Resi: {transaksi['Nomor Resi']} - Acara: {transaksi['Acara']}")
    print("╚══════════════════════════════════════════════════════╝")

    while True:
        try:
            batal = input("Apakah anda yakin ingin membatalkan tiket? (ketik 'batal' untuk membatalkan atau ketik '0' untuk kembali): ").strip()
            if batal == 'batal':
                resi_dibatal = input("Masukkan nomor resi yang ingin dibatalkan: ").strip()
                transaksi_batal = riwayat_transaksi[riwayat_transaksi["Nomor Resi"].str.lower() == resi_dibatal.lower()]
                acara_batal = transaksi_batal["Acara"].values[0]
                jadwal_acara = rincian_acara[rincian_acara["Acara"].str.lower() == acara_batal.lower()]
                
                if transaksi_batal.empty:
                    print(f"⟪ Transaksi dengan nomor resi '{resi_dibatal}' tidak ditemukan. Pastikan nomor resi yang dimasukkan benar. ⟫")
                else:
                # Ambil nama acara dan tanggal
                    acara_dibatal = acara_batal.lower()
                    jadwal_acara = rincian_acara[rincian_acara["Acara"].str.lower() == acara_dibatal]
                    
                    if jadwal_acara.empty:
                        print(f"⟪ Acara '{acara_batal}' tidak ditemukan dalam rincian acara. ⟫")
                    else:
                        tanggal_acara = jadwal_acara["Jadwal"].values[0]
                        try:
                            tanggal_acara_dt = datetime.strptime(tanggal_acara, '%d-%m-%Y')  
                            tanggal_sekarang = datetime.now()

                            selisih_hari = (tanggal_acara_dt - tanggal_sekarang).days
                            if selisih_hari < 2:
                                print("⟪ Pembatalan tiket tidak dapat dilakukan, karena sudah kurang dari 2 hari sebelum acara. ⟫")
                            else:
                                kode_acara_batal = jadwal_acara["Kode"].values[0]
                                riwayat_transaksi = riwayat_transaksi[riwayat_transaksi["Nomor Resi"] != resi_dibatal].reset_index(drop=True)
                                rincian_acara.loc[rincian_acara["Kode"] == kode_acara_batal, "Stok Tiket"] += 1

                                rincian_acara.to_csv("rincian_acara.csv", index=False)
                                riwayat_transaksi.to_csv("riwayat_transaksi.csv", index=False)

                                print("\n⟪ Tiket berhasil dibatalkan dan stok telah diperbarui. ⟫")
                                dashboard_user(df) 
                                break
                        except ValueError:
                            print(f"⟪ Format tanggal '{tanggal_acara}' pada acara '{acara_batal}' tidak valid. ⟫")
            elif batal == '0':
                return
        except ValueError:
            print("=== Typo! ===")

def cek_transaksi():
    global email_login

    try:
        riwayat_transaksi = pd.read_csv("riwayat_transaksi.csv")
    except FileNotFoundError:
        print("Belum ada riwayat transaksi!")
        loading_animation()
        return
    
    transaksi_user = riwayat_transaksi[riwayat_transaksi["UserID"] == email_login]

    if transaksi_user.empty:
        print("Belum ada riwayat transaksi!")
        loading_animation()
        return
    for index, transaksi in transaksi_user.iterrows():
         
        print("╔═════════════════════════════════════════╗")
        print("║            Riwayat Transaksi            ║")
        print("╠═════════════════════════════════════════╣")
        print(f"    Nomor Resi      : {transaksi["Nomor Resi"]}")
        print(f"    Acara           : {transaksi["Acara"]}")
        print(f"    Waktu Transaksi : {transaksi["Tanggal"]}")
        print(f"    Status          : {transaksi["Status"]}")
        print("╚═════════════════════════════════════════╝")

    print("\n[0] Kembali ke Menu Utama")
    while True:
        try:
            pilihan = input("Masukkan pilihan: ")
            if pilihan == '0':
                return
            else:
                print("Pilihan tidak valid!")
        except Exception:
            print("Terjadi kesalahan!")

def riwayat_transaksi(df):
    global transaksi_baru

    while True:
        nama_acara = input("Masukkan nama acara anda: ")
        
        try:
            df = pd.read_csv('riwayat_transaksi.csv')

            if "Acara" not in df.columns:
                print("Kolom 'Acara' tidak ditemukan dalam file CSV.")
            else:
                transaksi_baru = df[df["Acara"].str.lower() == nama_acara.lower()]

            if transaksi_baru.empty:
                print(f"Belum ada transaksi dengan nama acara {nama_acara}")
                input("Tekan enter untuk kembali : ")
                clear_terminal()
                dashboard_admin(df)
                break
            else:
                headers = ["UserID", "Nomor Resi","Kode", "Acara", "Tanggal", "Jumlah Bayar", "Status"]
                print(f"\n{'='*41} Transaksi Berdasarkan Acara {'='*41}\n")
                print(tabulate(transaksi_baru, headers=headers, tablefmt="fancy_grid"))
                input("Tekan enter untuk kembali : ")
                clear_terminal()
                dashboard_admin(df)
                break
        except ValueError:
            print("File data tidak ditemukan.")
            loading_animation(5)
            clear_terminal()
            dashboard_admin(df)
            break