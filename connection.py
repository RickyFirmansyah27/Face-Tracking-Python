import socket
import os

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (os.getenv('SERVER_HOST', '192.168.1.1'), int(os.getenv('SERVER_PORT', '12345')))
    client_socket.connect(server_address)
    print("Terhubung ke server.")
    return client_socket

def send_ping(client_socket):
    try:
        if client_socket.fileno() == -1:
            print("Koneksi ditutup. Mencoba menyambung kembali ke server...")
            client_socket = connect_to_server()
            if client_socket:
                print("Koneksi berhasil dibuat kembali.")
        else:
            client_socket.sendall("Ping".encode())
            print("Pesan ping terkirim")
    except OSError as e:
        if e.errno == 10054:
            print("Koneksi terputus oleh server. Mencoba menyambung kembali...")
            client_socket.close()
            client_socket = connect_to_server()
            if client_socket:
                print("Terhubung kembali ke server.")
        else:
            print("Gagal mengirim pesan:", e)
    except Exception as e:
        print("Gagal mengirim pesan:", e)
    return client_socket
