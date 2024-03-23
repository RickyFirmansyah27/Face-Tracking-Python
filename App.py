import cv2
import dlib
import Teskoneksi
import time

# Inisialisasi dataset
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
prev_x, prev_y, prev_w, prev_h = 0, 0, 0, 0
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# Inisialisasi socket dan koneksi ke server
client_socket = Teskoneksi.connect_to_server()


def main():
    cap = cv2.VideoCapture(0)

    alpha = 0.2
    smoothed_dx_box = 0
    smoothed_dy_box = 0
    blue_color = (255, 0, 0)
    blue_box_size = 250

    # Loop utama
    while True:

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blue_box_x = (frame.shape[1] - blue_box_size) // 2
        blue_box_y = (frame.shape[0] - blue_box_size) // 2
        cv2.rectangle(frame, (blue_box_x, blue_box_y), (blue_box_x + blue_box_size, blue_box_y + blue_box_size),
                      blue_color, 2)

        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            dx_box = x - prev_x
            dy_box = y - prev_y

            smoothed_dx_box = alpha * dx_box + (1 - alpha) * smoothed_dx_box
            smoothed_dy_box = alpha * dy_box + (1 - alpha) * smoothed_dy_box

            if abs(smoothed_dx_box) > 10:
                if smoothed_dx_box > 0:
                    print("Moving to the Right")
                else:
                    print("Moving to the Left")

            if abs(smoothed_dy_box) > 10:
                if smoothed_dy_box > 0:
                    print("Moving Downwards")
                else:
                    print("Moving Upwards")

            prev_x, prev_y, prev_w, prev_h = x, y, w, h

            green_box_x = x
            green_box_y = y
            green_box_w = w
            green_box_h = h

            # Periksa apakah kotak hijau berada di dalam kotak biru
            if blue_box_x < green_box_x and blue_box_y < green_box_y and \
                    blue_box_x + blue_box_size > green_box_x + green_box_w and blue_box_y + blue_box_size > green_box_y + green_box_h:
                # Kotak hijau berada di dalam kotak biru, tidak ada pergeseran
                pass
            else:
                # Kotak hijau keluar dari kotak biru, deteksi pergeseran
                if green_box_x > blue_box_x + blue_box_size:
                    print("Moving to the Right")
                elif green_box_x + green_box_w < blue_box_x:
                    print("Moving to the Left")
                if green_box_y > blue_box_y + blue_box_size:
                    print("Moving Downwards")
                elif green_box_y + green_box_h < blue_box_y:
                    print("Moving Upwards")

            # Gambar kotak di sekitar wajah dengan warna hijau
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Tampilkan frame dengan kotak deteksi wajah dan warna yang sesuai
        cv2.imshow('Talking Face Detection', frame)

        # Hentikan loop jika pengguna menekan tombol 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Loop utama
while True:
    try:
        client_socket = Teskoneksi.send_ping(client_socket)
        if client_socket:
            main()

    except (ConnectionResetError, BrokenPipeError):
        print("Koneksi ke server terputus. Akan mencoba menyambung kembali...")
        client_socket.close()
        while True:
            try:
                client_socket = Teskoneksi.connect_to_server()  # Mencoba menyambung kembali ke server
                print("Terhubung kembali ke server.")
                # Setelah tersambung kembali, loop utama akan melanjutkan pengiriman pesan ping
                break
            except (ConnectionError, TimeoutError):
                print("Gagal menyambung kembali ke server. Akan mencoba lagi dalam beberapa detik...")
                time.sleep(5)
