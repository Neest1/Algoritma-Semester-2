import fungsi as fs

fs.clear_terminal()
usn = "Admin"
pin = "12345"

fs.pembukaan()

while True:
        input_usn = input("\nMasukkan Username\t: ")
        if input_usn == usn:
             input_pin = input("\nMasukkan PIN\t\t: ")
             if input_pin == pin:
                  while True:
                       fs.clear_terminal()
                       komen =print("===== Pilih Menu =====\n")
                       print("[1] CRUD Obat\n[2] Exit")
                       input_pil = input("Masukkan Pilihan : ")
                       fs.clear_terminal()
                       match input_pil:
                            case "1":
                                 print("===== PILIH MENU =====\n")
                                 print("[1] Tambah Obat\n[2] Tampilkan Obat\n[3] Update Obat\n[4] Hapus Obat")
                                 pilihan = input("Masukkan Pilihan : ")
                                 fs.clear_terminal()
                                 match pilihan:
                                    case "1":
                                           fs.tambah_obat()
                                    case "2":
                                            fs.tabel_obat()
                                            input("\nTekan ENTER untuk kembali")

                                    case "3":
                                             kode = input("Masukkan Kode Obat yang akan diupdate: ").upper()
                                             fs.update_obat(kode)    
                                    case "4":
                                             kode = input("Masukkan Kode Obat yang akan dihapus: ").upper()
                                             fs.hapus_obat(kode)
                                    case "5":
                                     break
                                    case _:
                                        print("Pilihan tidak valid!")
                                        input("Tekan ENTER untuk kembali...")
                            case "2":
                              print("Terima kasih telah menggunakan sistem.")
                              exit()
                            case _:
                              print("Pilihan tidak valid!")
                              input("Tekan ENTER untuk kembali...")
             else:
               print("\n")
               print("="*50)
               print("PIN salah!")
               print("="*50)
        else:
         print("\n")
         print("="*50)
         print("Username Tidak Valid!".center(50))
         print("="*50)   

