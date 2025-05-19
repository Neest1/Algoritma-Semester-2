import pandas as pd
import calendar
from datetime import datetime
import sys
from halo import Halo
import time
import os

# Variabel global
database_event = None
riwayat_transaksi = None

def clear_alert(n=1):
    for _ in range(n):
        # Gerakkan kursor ke atas satu baris, lalu hapus baris
        print("\033[F\033[K", end='')
        
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation():
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start()

    time.sleep(3)  # Simulasi pekerjaan
    spinner.stop()

def cek_file(file):
    """Membaca file dan mengecek apakah file tersebut ada"""
    loading_animation()
    try:
        return pd.read_csv(f"{file}")
    except FileNotFoundError:
        print("File data base event tidak ditemukan. \nSilahkan periksa kembali nama dan lokasinya.")
        sys.exit()

def simpan_database_event():
    """Menyimpan perubahan stok tiket ke file CSV database_event"""
    database_event.to_csv('database_event.csv', index=False)

def cek_file_riwayat(file):
    """Membaca file dan mengecek apakah file tersebut ada"""
    loading_animation()
    try:
        return pd.read_csv(file)
    except FileNotFoundError:
        print("File riwayat transaksi tidak ditemukan. \nSilahkan periksa kembali nama dan lokasinya.")
        sys.exit()

def simpan_riwayat_transaksi(detail_pesanan):
    """Menambahkan transaksi baru ke riwayat_transaksi DataFrame dan menyimpannya ke file CSV"""
    global riwayat_transaksi
    # Tambahkan transaksi baru ke DataFrame global
    riwayat_transaksi = pd.concat([riwayat_transaksi, pd.DataFrame([detail_pesanan])], ignore_index=True)
    
    # Simpan kembali ke file
    riwayat_transaksi.to_csv('riwayat_transaksi.csv', index=False)

def dashboard():
    while True:
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

        try:
            pilihan = int(input("Masukkan pilihan Anda (1-6): "))
            match pilihan:
                case 1:
                    daftar_event()
                    input("Tekan enter untuk kembali ke menu :")
                case 2:
                    pesan_ticket()
                case 3:
                    tahun = input("Masukkan tahun (kosongkan untuk tahun ini): ") or None
                    bulan = input("Masukkan bulan (kosongkan untuk bulan ini): ") or None
                    cek_kalender(tahun=int(tahun) if tahun else None, bulan=int(bulan) if bulan else None)
                case 4:
                    batalkan_tiket()
                case 5:
                    tampilkan_riwayat_transaksi()
                case 6:
                    print("Terima kasih telah menggunakan sistem!")
                    break
                case _:
                    print("Pilihan tidak valid!")
                    loading_animation()
                    clear_alert(2)
        except ValueError:
            print("Masukkan harus berupa angka!")
            loading_animation()
            clear_alert(2)


def daftar_event():
    """Menampilkan semua acara yang tersedia"""
    print("╔═════════════════════════════════════════╗")
    print("║               Daftar Event              ║")
    print("╠═════════════════════════════════════════╣")
    for index, event in database_event.iterrows():
        print(f"   [{index+1}] {event['nama_event']}")
        print(f"       Guest Stars: {event['guest_stars']}")
        print(f"       Tempat: {event['tempat']}")
        print(f"       Jadwal: {event['jadwal']}")
        print(f"       Harga Tiket: Rp {event['harga']:,}")
        print(f"       Stok Tiket: {event['stock_ticket']}\n")
    print("╚═════════════════════════════════════════╝")

def pilih_acara():
    """Memilih acara untuk dipesan"""
    daftar_event()
    print("")
    while True:
        pilihan = input("Masukkan nomor ticket yang ingin dibeli (atau tekan x untuk kembali): ")
        match pilihan:
            case "x":
                return None
            case _ if pilihan.isdigit():
                ticket_terpilih = int(pilihan) - 1

                if 0 <= ticket_terpilih < len(database_event):
                    event = database_event.iloc[ticket_terpilih]
                    
                    if event['stock_ticket'] >= 0 :
                        while True:
                            jumlah_ticket = input("Masukkan jumlah ticket: ")
                            match jumlah_ticket:
                                case _ if jumlah_ticket.isdigit():
                                    jumlah = int(jumlah_ticket)

                                    if 0 < jumlah <= event['stock_ticket']:
                                        return nota_sementara(event, jumlah)
                                    else :
                                        print ("Jumlah ticket tidak valid!")
                                        loading_animation()
                                        clear_alert(2)
                                        continue

                                case _ :
                                    print("Input tidak valid!")
                                    loading_animation()
                                    clear_alert(2)
                                    continue

                    else :
                        print("Maaf, ticket untuk event ini sudah terjual habis")
                        print("Silahkan pilih event yang lainnya")
                        loading_animation()
                        clear_alert(3)
                        continue

                else :
                    print("Nomor event tidak terdaftar!")
                    loading_animation()
                    clear_alert(2)
                    continue

            case _:
                print("Input tidak valid!")
                loading_animation()
                clear_alert(3)
                continue

def nota_sementara(event, jumlah):
    '''Nota sementara dan proses pembayaran'''
    clear_terminal()
    total = event['harga'] * jumlah
    print("╔═════════════════════════════════════════╗")
    print("║            Rincian Pembelian            ║")
    print("╠═════════════════════════════════════════╣")
    print(f"  Ticket        : {event['nama_event']}")
    print(f"  Guest Stars   : {event['guest_stars']}")
    print(f"  Tempat        : {event['tempat']}")
    print(f"  Jadwal        : {event['jadwal']}")
    print(f"  Jumlah ticket : {jumlah}")
    print(f"  Total         : {total}")
    print("╚═════════════════════════════════════════╝")
    print("")
    print("[1] Lanjut Bayar")
    print("[2] Kembali")
    while True:
        pilihan = input("Masukkan pilihan (1/2): ")
        match pilihan:
            case "1":
                return proses_pembayaran(event, jumlah)
            case "2":
                loading_animation()
                clear_terminal()
                return pilih_acara()
            case _:
                print("Input tidak valid!")
                loading_animation()
                clear_alert(2)
                continue

def proses_pembayaran(event, jumlah):
    clear_terminal()
    print("╔═══════════════════════════╗")
    print("║     Metode Pembayaran     ║")
    print("╠═══════════════════════════╣")
    print("║  [1] Transfer Bank        ║")
    print("║  [2] E-Wallet             ║")
    print("║  [3] Kartu Kredit         ║")
    print("╚═══════════════════════════╝")

    while True:
        metode_input = input("Pilih metode pembayaran(1/2/3): ")

        match metode_input:
            case "1" | "2" | "3":
                metode_pembayaran = {
                    "1": "Transfer Bank", 
                    "2": "E-Wallet", 
                    "3": "Kartu Kredit"
                }[metode_input]

                #simpan transaksi ke riwayat transaksi.csv
                detail_pesanan = {
                    'nama_event': event['nama_event'],
                    'jumlah_tiket': jumlah,
                    'total_harga': event['harga'] * jumlah,
                    'metode_pembayaran': metode_pembayaran,
                    'tanggal_pesan': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                # Update stok
                database_event.loc[database_event['nama_event'] == event['nama_event'], 'stock_ticket'] -= jumlah

                # Simpan perubahan
                simpan_database_event()
                simpan_riwayat_transaksi(detail_pesanan)
                loading_animation()
                clear_terminal()
                return dashboard()
            case _:
                print("Metode pembayaran tidak valid!")
                loading_animation()
                clear_alert(2)
                continue
            
def pesan_ticket():
    """Pesan tiket untuk acara tertentu"""
    pilihan = pilih_acara()
    if pilihan is None:
        return  # Kembali ke menu utama

def cek_kalender(tahun=None, bulan=None):
    """Menampilkan kalender untuk tahun dan bulan tertentu"""
    if tahun is None:
        tahun = datetime.now().year
    if bulan is None:
        bulan = datetime.now().month

    try:
        cal = calendar.monthcalendar(tahun, bulan)
        print(f"\n===== KALENDER {calendar.month_name[bulan]} {tahun} =====")
        print("Sen Sel Rab Kam Jum Sab Min")
        for minggu in cal:
            for hari in minggu:
                if hari == 0:
                    print("   ", end="")
                else:
                    print(f"{hari:2d} ", end="")
            print()
        
        # Tambahkan opsi kembali ke menu utama
        print("\n[1] Kembali ke Menu Utama")
        while True:
            try:
                pilihan = input("Masukkan pilihan: ")
                if pilihan == '1':
                    return
                else:
                    print("Pilihan tidak valid!")
            except Exception:
                print("Terjadi kesalahan!")
    except ValueError:
        print("Masukkan tahun dan bulan yang valid!")
        clear_alert(3)

def batalkan_tiket():
    """Membatalkan tiket dari riwayat transaksi"""
    global riwayat_transaksi
    global database_event
    clear_terminal()

    if riwayat_transaksi.empty:
        print("Belum ada riwayat transaksi!")
        loading_animation()
        clear_alert(2)
        return

    print("╔═════════════════════════════════════════╗")
    print("║            Riwayat Transaksi            ║")
    print("╠═════════════════════════════════════════╣")
    for index, transaksi in riwayat_transaksi.iterrows():
        print(f"    {index+1}. {transaksi['nama_event']} - {transaksi['jumlah_tiket']} tiket")
    print("╚═════════════════════════════════════════╝")

    print("\n[1] Batalkan Tiket")
    print("[2] Kembali ke Menu Utama")
    while True:
        try:
            menu_pilihan = input("Masukkan pilihan (1/2): ")
            
            if menu_pilihan == '1':
                break
            elif menu_pilihan == '2':
                return
            else:
                print("Pilihan tidak valid!")
                clear_alert(2)
        except Exception:
            print("Terjadi kesalahan!")
            clear_alert(2)

    while True:
        try:
            pilihan = int(input("Masukkan nomor transaksi yang ingin dibatalkan: ")) - 1
            if 0 <= pilihan < len(riwayat_transaksi):
                transaksi = riwayat_transaksi.iloc[pilihan]
                # Kembalikan stok tiket ke database_event
                database_event.loc[database_event['nama_event'] == transaksi['nama_event'], 'stock_ticket'] += transaksi['jumlah_tiket']
                # Hapus transaksi dari riwayat
                riwayat_transaksi = riwayat_transaksi.drop(pilihan).reset_index(drop=True)
                print("Tiket berhasil dibatalkan!")
                
                # Simpan perubahan stok tiket ke database_event.csv
                simpan_database_event()
                # Simpan riwayat transaksi yang baru ke CSV
                riwayat_transaksi.to_csv('riwayat_transaksi.csv', index=False)
                
                print("\n[1] Kembali ke Menu Utama")
                while True:
                    pilihan = input("Masukkan pilihan: ")
                    if pilihan == '1':
                        return
                    else:
                        print("Pilihan tidak valid!")
                break
            else:
                print("Pilihan tidak valid!")
                clear_alert(2)
        except ValueError:
            print("Masukkan harus berupa angka!")
            clear_alert(2)


def tampilkan_riwayat_transaksi():
    """Menampilkan riwayat transaksi"""
    clear_terminal()
    if riwayat_transaksi.empty:
        print("Belum ada riwayat transaksi!")
        loading_animation()
        clear_alert(2)
        return

    print("╔═════════════════════════════════════════╗")
    print("║            Riwayat Transaksi            ║")
    print("╠═════════════════════════════════════════╣")
    for index, transaksi in riwayat_transaksi.iterrows():
        print(f"    Transaksi #{index+1}")
        for key, value in transaksi.items():
            print(f"    {key.replace('_', ' ').title()}: {value}")
        print(f"    {"-" * 30}")
    print("╚═════════════════════════════════════════╝")

    print("\n[1] Kembali ke Menu Utama")
    while True:
        try:
            pilihan = input("Masukkan pilihan: ")
            if pilihan == '1':
                return
            else:
                print("Pilihan tidak valid!")
        except Exception:
            print("Terjadi kesalahan!")

def main():
    global database_event
    global riwayat_transaksi
    file_database = 'database_event.csv'
    file_riwayat_transaksi = 'riwayat_transaksi.csv'
    database_event = cek_file(file_database)
    riwayat_transaksi = cek_file_riwayat(file_riwayat_transaksi)
    dashboard()

main()