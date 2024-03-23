import cv2
# import dlib


# Inisialisasi detektor wajah dan bibir dari dlib
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# Inisialisasi objek VideoCapture untuk mengakses webcam (index 0 biasanya webcam default)
cap = cv2.VideoCapture(0)
prev_x, prev_y, prev_w, prev_h = 0, 0, 0, 0
alpha = 0.2
smoothed_dx_box = 0
smoothed_dy_box = 0
blue_color = (255, 0, 0) 
blue_box_size = 250

# Loop utama
while True:
    # Baca frame dari webcam
    ret, frame = cap.read()

    # Konversi frame ke skala abu-abu (untuk meningkatkan kinerja deteksi)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Buat kotak biru di tengah frame
    blue_box_x = (frame.shape[1] - blue_box_size) // 2
    blue_box_y = (frame.shape[0] - blue_box_size) // 2
    cv2.rectangle(frame, (blue_box_x, blue_box_y), (blue_box_x + blue_box_size, blue_box_y + blue_box_size), blue_color, 2)

    # Deteksi wajah dalam frame
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))  # dengan ini

    # Loop melalui setiap wajah yang terdeteksi
    for (x, y, w, h) in faces:
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

    # Tampilkan frame dengan kotak deteksi wajah dan warna yang sesuai
    cv2.imshow('Talking Face Detection', frame)

    # Hentikan loop jika pengguna menekan tombol 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup webcam dan jendela tampilan
cap.release()
cv2.destroyAllWindows()
