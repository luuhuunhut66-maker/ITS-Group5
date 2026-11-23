# KHẢO SÁT CÔNG NGHỆ NHẬN DIỆN KHUÔN MẶT VÀ ỨNG DỤNG TRONG GIAO THÔNG
**Môn học:** Hệ thống Giao thông Thông minh (ITS) | **Nhóm thực hiện:** Nhóm 5 (4 thành viên)

---

## 📌 BẢNG PHÂN CÔNG NHIỆM VỤ TIỂU LUẬN

| Thành viên phụ trách | Nhiệm vụ chính theo phân công nhóm | Trạng thái & Tài nguyên liên quan |
| :--- | :--- | :--- |
| **Chương 1, 5 & 6** | Tổng quan đề tài, đánh giá ưu/nhược điểm công nghệ và kết luận | Sử dụng số liệu thực nghiệm tại `output_figures/ket_qua_kiem_thu_mau.txt` |
| **Chương 2** | Cơ sở lý thuyết các công nghệ nhận diện khuôn mặt, chọn mô hình | Đã chuẩn bị sẵn tài liệu: `CHUONG_2_TRICH_DAN_VA_HINH_MINH_HOA.md` |
| **Chương 3** *(Khánh)* | Chuẩn bị tập dữ liệu mẫu, xuất hình minh họa và kiểm tra bản quyền nguồn | **ĐÃ HOÀN THÀNH 100%** (Xem mục Cấu trúc thư mục bên dưới) |
| **Chương 4** | Xây dựng chương trình nhận diện thời gian thực qua Webcam & demo | Đã chuẩn bị sẵn khung mã nguồn: `scripts/test_webcam.py` |

---

## 📂 CẤU TRÚC VÀ CHỨC NĂNG CỦA CÁC THƯ MỤC TRONG DỰ ÁN

```text
face-recognition/
├── dataset/                               # Tập dữ liệu ảnh chuẩn hóa (đã phân tách 3 tập độc lập)
│   ├── registered/                        # DỮ LIỆU ĐĂNG KÝ (Enrollment / Known Faces)
│   │   ├── Person_A/                      # Chứa ảnh chính diện của Người A (Barack Obama)
│   │   └── Person_B/                      # Chứa ảnh chính diện của Người B (Elon Musk)
│   ├── calibration/                       # DỮ LIỆU HIỆU CHUẨN NGƯỠNG (Mục 4.5)
│   │   ├── Person_A/                      # Ảnh Người A ở điều kiện chụp khác để đo khoảng cách L2
│   │   └── Person_B/                      # Ảnh Người B ở điều kiện chụp khác
│   └── test/                              # DỮ LIỆU KIỂM THỬ (Testing)
│       ├── test_tilted.jpg                # Ảnh nghiêng đầu (~27.7°) dùng minh họa Căn chỉnh Affine
│       └── stranger_1.jpg                 # Ảnh người lạ (Lionel Messi) kiểm tra nhãn "Chưa xác định"
│
├── output_figures/                        # TÀI NGUYÊN HÌNH ẢNH & BÁO CÁO THỰC NGHIỆM ĐÃ XUẤT
│   ├── hinh_2_1_phat_hien_diem_moc.jpg    # Hình 2.1: Bounding Box + 5 điểm mốc đặc trưng (Mục 2.4)
│   ├── hinh_2_2_can_chinh_khuon_mat.jpg   # Hình 2.2: So sánh khuôn mặt Trước & Sau căn chỉnh Affine (Mục 2.5)
│   └── ket_qua_kiem_thu_mau.txt           # Nhật ký đo khoảng cách Euclid 128D & kiểm thử ngưỡng L2
│
├── raw_images/                            # ẢNH THÔ GỐC & TRÍCH DẪN BẢN QUYỀN
│   ├── image_sources.txt                  # URL gốc từ Wikimedia Commons (Public Domain / CC-BY-SA)
│   └── *.jpg                              # Các file ảnh gốc tải về
│
├── scripts/                               # MÃ NGUỒN XỬ LÝ & CHƯƠNG TRÌNH THỰC THI
│   ├── prepare_chapter2_assets.py         # Script tự động xuất Hình 2.1, 2.2 và chạy kiểm thử ngưỡng L2
│   ├── test_webcam.py                     # Chương trình nhận diện khuôn mặt REAL-TIME qua WEBCAM
│   └── download_sample_images.py          # Script tự động tải ảnh mẫu có bản quyền từ Wikimedia
│
├── CHUONG_2_TRICH_DAN_VA_HINH_MINH_HOA.md # Mẫu caption hình, bảng ánh xạ vị trí trích dẫn & 12 nguồn IEEE
├── PLAYBOOK_HUONG_DAN.md                  # Tài liệu hướng dẫn playbook gốc
└── README.md                              # Tài liệu tổng quan dự án (file này)
```

---

## 🚀 HƯỚNG DẪN DÀNH CHO CÁC THÀNH VIÊN TRONG NHÓM

### 1. Dành cho bạn phụ trách Chương 2 (Lý thuyết & Trích dẫn)
- Mở file `CHUONG_2_TRICH_DAN_VA_HINH_MINH_HOA.md`:
  - **Mục 1:** Sao chép mẫu chú thích và nguồn ảnh để dán dưới **Hình 2.1** và **Hình 2.2** trong file Word.
  - **Mục 2:** Xem bảng ánh xạ để gắn số trích dẫn `[1]` – `[12]` vào đúng các công nghệ (Eigenfaces, Fisherfaces, LBPH, HOG, DeepFace, FaceNet, ArcFace, Haar, MTCNN, RetinaFace, Dlib, OpenCV).
  - **Mục 3:** Sao chép danh mục 12 tài liệu tham khảo định dạng chuẩn IEEE vào cuối bài.

### 2. Dành cho bạn phụ trách Chương 4 (Lập trình Webcam & Demo)
Bạn đã có sẵn toàn bộ nền tảng để chạy và mở rộng chương trình demo:

#### Bước 2.1: Kích hoạt môi trường ảo
Mở terminal tại thư mục gốc `face-recognition`:
```powershell
# Trên Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# Hoặc nếu dùng Command Prompt (CMD):
.\.venv\Scripts\activate.bat
```

#### Bước 2.2: Chạy thử nhận diện trực tiếp qua Webcam
```bash
python scripts/test_webcam.py
```
- Khi webcam bật lên:
  - Nếu đưa ảnh/khuôn mặt của **Người A (Obama)** hoặc **Người B (Elon Musk)** vào: Khung nhận diện **màu xanh lá**, hiển thị tên và khoảng cách $L_2 < 0.60$.
  - Nếu là khuôn mặt người khác: Khung **màu đỏ**, hiển thị **"Chua xac dinh"** (Unknown).
  - Nhấn phím **`s`**: Tự động chụp lại khung hình lưu vào `output_figures/` để chèn vào báo cáo Chương 4.
  - Nhấn phím **`q`** hoặc **`ESC`**: Thoát chương trình.

#### Bước 2.3: Thay thế bằng khuôn mặt thành viên nhóm để demo trên lớp
Để hệ thống nhận diện chính các thành viên trong nhóm khi lên thuyết trình:
1. Vào thư mục `dataset/registered/`.
2. Tạo thư mục mang tên bạn (ví dụ `dataset/registered/Huynh_Nhat_Khanh/`, `dataset/registered/Thanh_Vien_2/`).
3. Chụp 2–3 tấm ảnh rõ mặt của mỗi người bỏ vào thư mục tương ứng.
4. Chạy lại `python scripts/test_webcam.py`, chương trình sẽ **tự động học và nhận diện khuôn mặt của các thành viên nhóm** mà không cần sửa code!

---

## 📊 KẾT QUẢ THỰC NGHIỆM ĐÃ ĐẠT ĐƯỢC

Toàn bộ kiểm thử trên không gian đặc trưng 128 chiều (ResNet Dlib) với ngưỡng quyết định chuẩn $Threshold = 0.60$:
- **Cùng danh tính (Intra-class):** Khoảng cách $L_2 \approx 0.30 - 0.44 < 0.60 \rightarrow$ Nhận diện chính xác 100%.
- **Khác danh tính & Người lạ (Inter-class):** Khoảng cách $L_2 \approx 0.85 - 0.88 \ge 0.60 \rightarrow$ Từ chối và phân loại "Chưa xác định" đạt độ tin cậy tuyệt đối, tỷ lệ nhận nhầm FAR = 0%.
