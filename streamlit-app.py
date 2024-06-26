import streamlit as st
import numpy as np
import connection
import time
import cv2


detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def main():
    cap = cv2.VideoCapture(1)  # Use index 0 for the default camera
    if not cap.isOpened():
        st.error("Error: Unable to access the webcam.")
        return

    prev_x, prev_y, prev_w, prev_h = 0, 0, 0, 0 
    alpha = 0.2
    smoothed_dx_box = 0
    smoothed_dy_box = 0
    blue_color = (255, 0, 0)
    blue_box_size = 250

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Error: Unable to receive frames from the webcam.")
            break

        faces = detect_faces(frame)

        # Konversi frame ke skala abu-abu (untuk meningkatkan kinerja deteksi)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blue_box_x = (frame.shape[1] - blue_box_size) // 2
        blue_box_y = (frame.shape[0] - blue_box_size) // 2
        cv2.rectangle(frame, (blue_box_x, blue_box_y), (blue_box_x + blue_box_size, blue_box_y + blue_box_size), blue_color, 2)

        for (x, y, w, h) in faces:
            dx_box = x - prev_x
            dy_box = y - prev_y

            smoothed_dx_box = alpha * dx_box + (1 - alpha) * smoothed_dx_box
            smoothed_dy_box = alpha * dy_box + (1 - alpha) * smoothed_dy_box

            if abs(smoothed_dx_box) > 10:
                if smoothed_dx_box > 0:
                    st.write("Moving to the Right")
                else:
                    st.write("Moving to the Left")

            if abs(smoothed_dy_box) > 10:
                if smoothed_dy_box > 0:
                    st.write("Moving to the Downwards")
                else:
                    st.write("Moving to the Upward")

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
                    st.write("Moving to the Right")
                elif green_box_x + green_box_w < blue_box_x:
                    st.write("Moving to the Left")
                if green_box_y > blue_box_y + blue_box_size:
                    st.write("Moving to the Downwards")
                elif green_box_y + green_box_h < blue_box_y:
                    st.write("Moving to the Upwards")

            # Gambar kotak di sekitar wajah dengan warna hijau
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display frame using Streamlit
        st.image(frame, channels="BGR", use_column_width=True)

    # Release the camera and close OpenCV window
    cap.release()

def reconnect_to_server():
    while True:
        try:
            client_socket = connection.connect_to_server() 
            st.write("Terhubung kembali ke server.")
            return client_socket
        except (ConnectionError, TimeoutError):
            st.write("Gagal menyambung kembali ke server. Akan mencoba lagi dalam beberapa detik...")
            time.sleep(5)

def connect_and_run():
    while True:
        try:
            main()
            # client_socket = Teskoneksi.connect_to_server()
            # if client_socket:
            #     main()
            # else:
            #     st.write("Tidak dapat terhubung ke server. Memulai program utama tanpa koneksi ke server.")
            #     main()
            break
        except (ConnectionResetError, BrokenPipeError):
            st.write("Koneksi ke server terputus. Akan mencoba menyambung kembali...")
            client_socket.close()
            client_socket = reconnect_to_server()

if __name__ == "__main__":
    connect_and_run()
