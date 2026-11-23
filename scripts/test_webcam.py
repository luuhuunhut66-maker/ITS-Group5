"""
=============================================================================
CHƯƠNG TRÌNH DEMO NHẬN DIỆN KHUÔN MẶT REAL-TIME QUA WEBCAM
Phục vụ: Tiểu luận "Khảo sát công nghệ nhận diện khuôn mặt và ứng dụng trong giao thông"
Nhóm 5 - Môn ITS
=============================================================================
Cách sử dụng:
  1. Kích hoạt môi trường ảo: .\\.venv\\Scripts\\Activate.ps1
  2. Chạy lệnh: python scripts/test_webcam.py
  3. Phím tắt trong cửa sổ camera:
     - Nhấn phím 'q' hoặc 'ESC': Thoát chương trình
     - Nhấn phím 's': Chụp ảnh frame hiện tại lưu vào output_figures/snapshot.jpg
=============================================================================
"""

import os
import sys
import time
import cv2
import numpy as np
import face_recognition

# Tự động xác định thư mục gốc của dự án (face-recognition/) dù chạy từ bất kỳ đâu
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_registered_faces(registered_dir=None):
    """
    Tự động quét toàn bộ thư mục con trong dataset/registered/
    Mỗi thư mục con là 1 danh tính (Person_A, Person_B, hoặc tên thành viên nhóm)
    """
    if registered_dir is None:
        registered_dir = os.path.join(BASE_DIR, "dataset", "registered")

    known_face_encodings = []
    known_face_names = []

    if not os.path.exists(registered_dir):
        print(f"[CẢNH BÁO] Không tìm thấy thư mục: {registered_dir}")
        return known_face_encodings, known_face_names

    print(f">>> Đang nạp dữ liệu khuôn mặt đã đăng ký từ: {registered_dir} ...")
    for person_name in os.listdir(registered_dir):
        person_dir = os.path.join(registered_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        person_encodings = []
        for img_name in os.listdir(person_dir):
            if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(person_dir, img_name)
                try:
                    img = face_recognition.load_image_file(img_path)
                    encs = face_recognition.face_encodings(img)
                    if encs:
                        person_encodings.append(encs[0])
                        print(f"  + Nạp mẫu [{person_name}]: {img_name}")
                except Exception as e:
                    print(f"  - Lỗi đọc ảnh {img_path}: {e}")

        # Tính trung bình các vector embedding nếu có nhiều ảnh mẫu của cùng 1 người
        if person_encodings:
            mean_encoding = np.mean(person_encodings, axis=0)
            known_face_encodings.append(mean_encoding)
            known_face_names.append(person_name)

    print(f">>> Đã nạp thành công {len(known_face_names)} danh tính: {', '.join(known_face_names)}\n")
    return known_face_encodings, known_face_names

def main():
    known_face_encodings, known_face_names = load_registered_faces()

    if not known_face_encodings:
        print("[LỖI] Chưa có dữ liệu đăng ký trong 'dataset/registered/'. Vui lòng kiểm tra lại!")
        return

    # Ngưỡng phân loại khoảng cách Euclid (Threshold = 0.60 theo chuẩn Dlib)
    # Khoảng cách < 0.60: Nhận diện đúng danh tính
    # Khoảng cách >= 0.60: Gán nhãn Chưa xác định (Unknown)
    MATCH_THRESHOLD = 0.60

    print(">>> Đang mở Webcam...")
    video_capture = cv2.VideoCapture(0)

    # Đặt độ phân giải camera (720p nếu được hỗ trợ)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not video_capture.isOpened():
        print("[LỖI] Không thể kết nối với Webcam. Hãy kiểm tra xem camera máy tính có đang bị ứng dụng khác chiếm dụng không.")
        return

    print("=================================================================")
    print("WEBCAM ĐÃ SẴN SÀNG! Đang truyền hình ảnh trực tiếp...")
    print(" - Nhấn 'q' hoặc 'ESC' trên cửa sổ camera để DỪNG.")
    print(" - Nhấn 's' để LƯU ẢNH chụp màn hình.")
    print("=================================================================\n")

    # Tối ưu hiệu năng: Xử lý nhận diện cách quãng (mỗi 2 frame xử lý 1 lần)
    process_this_frame = True
    face_locations = []
    face_names = []
    face_distances = []

    fps_start_time = time.time()
    fps_frame_count = 0
    fps = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("[CẢNH BÁO] Không nhận được frame từ webcam.")
            break

        fps_frame_count += 1
        if time.time() - fps_start_time >= 1.0:
            fps = fps_frame_count / (time.time() - fps_start_time)
            fps_frame_count = 0
            fps_start_time = time.time()

        # Thu nhỏ kích thước frame xuống 1/4 để tăng tốc độ xử lý real-time
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Chuyển BGR sang RGB cho face_recognition
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        if process_this_frame:
            # Tìm tất cả khuôn mặt trong frame hiện tại
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            face_distances = []

            for face_encoding in face_encodings:
                # Tính khoảng cách Euclid tới toàn bộ mẫu đã đăng ký
                distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(distances)
                min_distance = distances[best_match_index]

                if min_distance < MATCH_THRESHOLD:
                    name = known_face_names[best_match_index]
                else:
                    name = "Chua xac dinh"

                face_names.append(name)
                face_distances.append(min_distance)

        process_this_frame = not process_this_frame

        # Vẽ kết quả lên khung hình gốc
        for (top, right, bottom, left), name, dist in zip(face_locations, face_names, face_distances):
            # Nhân tọa độ lên 4 lần vì trước đó đã thu nhỏ 0.25
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Màu sắc: Xanh lá nếu nhận diện đúng, Đỏ nếu chưa xác định
            is_known = (name != "Chua xac dinh")
            box_color = (0, 220, 0) if is_known else (0, 0, 255)

            # Vẽ khung bao khuôn mặt
            cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)

            # Khung nền chứa tên
            label = f"{name} (d={dist:.2f})"
            label_size, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            cv2.rectangle(frame, (left, bottom - label_size[1] - 10), (left + label_size[0] + 10, bottom),
                          box_color, cv2.FILLED)
            cv2.putText(frame, label, (left + 5, bottom - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        # Hiển thị thông tin hệ thống góc trên bên trái
        cv2.putText(frame, f"FPS: {fps:.1f} | Ngưỡng L2: {MATCH_THRESHOLD}", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Nhan 'q' de thoat | 's' de chup anh", (15, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1, cv2.LINE_AA)

        # Hiển thị cửa sổ
        cv2.imshow("ITS Nhom 5 - Demo Nhan dien Khuon mat Real-time", frame)

        # Xử lý sự kiện phím
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # Phím q hoặc ESC
            break
        elif key == ord('s'):
            out_dir = os.path.join(BASE_DIR, "output_figures")
            os.makedirs(out_dir, exist_ok=True)
            snap_path = os.path.join(out_dir, f"webcam_snapshot_{int(time.time())}.jpg")
            cv2.imwrite(snap_path, frame)
            print(f">>> Đã chụp và lưu frame tại: {snap_path}")

    video_capture.release()
    cv2.destroyAllWindows()
    print("\n>>> Đã đóng chương trình Webcam thành công!")

if __name__ == "__main__":
    main()
