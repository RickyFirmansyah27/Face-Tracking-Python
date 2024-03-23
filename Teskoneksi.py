import socket
import time
import os

server = os.environ["SERVER"]

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server,12345)
    while True:
        try:
            client_socket.connect(server_address)
            print("Terhubung ke server.")
            return client_socket
        except (ConnectionError, TimeoutError) as e:
            print("Gagal terhubung ke server:", e)
            print("Akan mencoba lagi dalam beberapa detik...")
            time.sleep(5)  # Menunggu beberapa detik sebelum mencoba lagi

# Fungsi untuk mengirim pesan ping ke server
def send_ping(client_socket):
    try:
        # Pengujian koneksi sebelum mengirim pesan
        if client_socket.fileno() == -1:
            # Jika koneksi telah ditutup, coba buat koneksi baru
            print("Koneksi ditutup. Mencoba menyambung kembali ke server...")
            client_socket = connect_to_server()  # Update socket yang digunakan
            if client_socket:
                print("Koneksi berhasil dibuat kembali.")
        else:
            client_socket.sendall("Ping".encode())
            print("Pesan ping terkirim")
    except OSError as e:
        if e.errno == 10054:  # WinError 10054: An existing connection was forcibly closed by the remote host
            print("Koneksi terputus oleh server. Mencoba menyambung kembali...")
            client_socket.close()
            client_socket = connect_to_server()  # Mencoba menyambung kembali ke server
            if client_socket:
                print("Terhubung kembali ke server.")
        else:
            print("Gagal mengirim pesan:", e)
    except Exception as e:
        print("Gagal mengirim pesan:", e)
    return client_socket  # Kembalikan socket yang baru atau yang telah diperbarui