# PLAYBOOK HƯỚNG DẪN ANTIGRAVITY: CHUẨN BỊ DỮ LIỆU DEMO, HÌNH MINH HỌA & KIỂM TRA NGUỒN

> **Cách dùng file này:**  
> 1. Bạn làm nhanh **Phần 0** (tải sẵn khoảng 7–8 ảnh người nổi tiếng và lưu link nguồn).  
> 2. Mở workspace bằng **Antigravity**, đặt file này ở thư mục gốc và nhập lệnh:  
>    `"Hãy đọc kỹ file HUONG_DAN_ANTIGRAVITY.md và thực hiện tuần tự từ Bước 1 đến Bước 4. Báo cáo kết quả sau mỗi bước."`

---

## PHẦN 0: VIỆC BẠN CẦN LÀM TRƯỚC (CHUẨN BỊ ẢNH THÔ)

Để tránh lỗi chặn tải tự động và đảm bảo bạn kiểm soát được bản quyền/nguồn ảnh ngay từ đầu, hãy tự tải **7–8 ảnh người nổi tiếng** (ưu tiên từ **Wikimedia Commons** hoặc ảnh báo chí rõ nét, chỉ có 1 khuôn mặt trong khung hình) vào thư mục `raw_images/`:

1. **Người A (ví dụ: Sơn Tùng M-TP) – 3 ảnh:**
   - `personA_1.jpg`: Ảnh nhìn chính diện, đủ sáng (dùng làm mẫu đăng ký).
   - `personA_2.jpg`: Ảnh góc mặt hơi khác hoặc ánh sáng khác nhẹ (dùng làm mẫu hiệu chỉnh ngưỡng).
   - `personA_3_tilted.jpg`: Ảnh **nghiêng đầu khoảng 15°–30°** (dùng để xuất hình minh họa bước Căn chỉnh khuôn mặt – Face Alignment ở Mục 2.5).
2. **Người B (ví dụ: Elon Musk hoặc nghệ sĩ khác) – 3 ảnh:**
   - `personB_1.jpg`: Ảnh chính diện (mẫu đăng ký).
   - `personB_2.jpg`: Ảnh chính diện khác biểu cảm (mẫu đăng ký).
   - `personB_3.jpg`: Ảnh khác góc nhẹ (mẫu hiệu chỉnh ngưỡng).
3. **Người C (Người lạ / Chưa đăng ký) – 1 đến 2 ảnh:**
   - `stranger_1.jpg`: Ảnh một người nổi tiếng khác hoàn toàn không có trong nhóm A, B (dùng để kiểm thử nhãn `"Chưa xác định"`).
4. **Lưu lại đường dẫn nguồn ảnh:**
   - Tạo file `raw_images/image_sources.txt` và dán URL gốc của từng ảnh vừa tải (để Antigravity tự động chèn trích dẫn nguồn ngay dưới hình minh họa theo đúng yêu cầu đề cương).

---

## QUY TẮC BẮT BUỘC DÀNH CHO ANTIGRAVITY

Khi thực thi các bước dưới đây, Antigravity phải tuân thủ nghiêm ngặt các nguyên tắc của đề cương tiểu luận **"Khảo sát công nghệ nhận diện khuôn mặt và ứng dụng trong giao thông"**:
1. **Thư viện sử dụng:** Python + `face_recognition` (Dlib) + `opencv-python` + `numpy`.
2. **Tách bạch tập dữ liệu:** Không dùng chung ảnh giữa tập đăng ký (`registered`), tập hiệu chỉnh ngưỡng (`calibration`) và tập kiểm thử (`test`).
3. **Tính xác thực nguồn:** Mọi hình ảnh minh họa sử dụng dữ liệu bên ngoài phải ghi rõ URL nguồn gốc ngay bên dưới chú thích hình. Không bịa đặt số liệu thực nghiệm hay tài liệu tham khảo.

---

## BƯỚC 1: THIẾT LẬP MÔI TRƯỜNG & PHÂN LOẠI THƯ MỤC DỮ LIỆU

**Nhiệm vụ của Antigravity:**
1. Kiểm tra phiên bản Python hiện có, tạo môi trường ảo (`.venv`) nếu chưa có và cài đặt các thư viện cần thiết (ưu tiên cài `dlib-bin` trước `face_recognition` nếu chạy trên Windows để tránh lỗi biên dịch C++):
   ```bash
   pip install dlib-bin face_recognition opencv-python numpy
   ```
2. Tạo cấu trúc thư mục chuẩn của dự án và phân phối ảnh từ `raw_images/` vào đúng vị trí:
   ```text
   face_recognition_demo/
   ├── raw_images/                 # Ảnh thô người dùng đã tải + image_sources.txt
   ├── dataset/
   │   ├── registered/             # Dữ liệu đăng ký mẫu (Enrollment)
   │   │   ├── Person_A/           # Chứa personA_1.jpg
   │   │   └── Person_B/           # Chứa personB_1.jpg, personB_2.jpg
   │   ├── calibration/            # Dữ liệu hiệu chỉnh ngưỡng quyết định (Mục 4.5)
   │   │   ├── Person_A/           # Chứa personA_2.jpg
   │   │   └── Person_B/           # Chứa personB_3.jpg
   │   └── test/                   # Dữ liệu kiểm thử & xuất hình minh họa
   │       ├── test_tilted.jpg     # Copy từ personA_3_tilted.jpg
   │       └── stranger_1.jpg      # Copy từ stranger_1.jpg
   ├── output_figures/             # Nơi lưu hình minh họa xuất cho Chương 2
   └── scripts/                    # Chứa mã nguồn xử lý
   ```
3. Chạy kiểm tra nhanh xem thư viện `face_recognition` có phát hiện được khuôn mặt trong tất cả các ảnh ở `dataset/` hay không. Nếu ảnh nào không nhận diện được mặt, báo lại ngay cho người dùng thay ảnh khác.

---

## BƯỚC 2: XUẤT HÌNH MINH HỌA CHƯƠNG 2 & KIỂM THỬ NGƯỠNG SO KHỚP

**Nhiệm vụ của Antigravity:**
Tạo file `scripts/prepare_chapter2_assets.py` và chạy script để thực hiện 3 đầu việc sau:

1. **Xuất Hình minh họa Mục 2.4 (`output_figures/hinh_2_1_phat_hien_diem_moc.jpg`):**
   - Đọc ảnh `dataset/test/test_tilted.jpg`.
   - Phát hiện khung bao khuôn mặt (`face_locations`) và trích xuất đặc trưng điểm mốc (`face_landmarks`).
   - Vẽ khung bao chữ nhật màu xanh lá quanh khuôn mặt và vẽ 5 điểm mốc đặc trưng màu đỏ (tâm mắt trái, tâm mắt phải, đầu mũi, khóe miệng trái, khóe miệng phải) kèm chú thích rõ ràng trên ảnh.

2. **Xuất Hình minh họa Mục 2.5 (`output_figures/hinh_2_2_can_chinh_khuon_mat.jpg`):**
   - Từ tọa độ tâm hai mắt của ảnh `dataset/test/test_tilted.jpg`, tính góc nghiêng $\theta = \arctan2(\Delta y, \Delta x)$.
   - Áp dụng phép biến đổi hình học Affine (`cv2.getRotationMatrix2D` + `cv2.warpAffine`) để xoay ảnh sao cho đường nối hai mắt nằm ngang chuẩn hóa.
   - Cắt vùng khuôn mặt **Trước căn chỉnh** (bên trái) và **Sau căn chỉnh** (bên phải), chuẩn hóa về cùng kích thước (ví dụ $250 \times 250$ pixel), ghép ngang thành 1 ảnh so sánh trực quan và lưu lại.

3. **Kiểm thử logic so khớp & ngưỡng quyết định (Phục vụ Mục 2.6 & Mục 4.5):**
   - Trích xuất vectơ `face_encoding` (128 chiều) cho toàn bộ ảnh trong `dataset/registered/`.
   - Tính khoảng cách Euclid ($L_2$ distance) khi đối chiếu với:
     - Ảnh cùng người trong `dataset/calibration/` (kỳ vọng khoảng cách nhỏ, $< 0.6$).
     - Ảnh người lạ trong `dataset/test/stranger_1.jpg` (kỳ vọng khoảng cách lớn, $\ge 0.6$).
   - Xuất kết quả kiểm thử ra terminal và lưu log vào `output_figures/ket_qua_kiem_thu_mau.txt` để nhóm đối chiếu.

---

## BƯỚC 3: KIỂM TRA NGUỒN & TẠO FILE BỔ SUNG TRÍCH DẪN CHO CHƯƠNG 2

**Nhiệm vụ của Antigravity:**
Đọc file `raw_images/image_sources.txt` và đối chiếu với nội dung `Chuong_2_Cac_Cong_Nghe_Nhan_Dien_Khuon_Mat.docx`, sau đó tạo file `CHUONG_2_TRICH_DAN_VA_HINH_MINH_HOA.md` gồm 3 phần:

1. **Mẫu chèn Hình minh họa kèm nguồn trích dẫn chuẩn đề cương:**
   - Tạo sẵn đoạn văn bản và chú thích để chèn vào **Mục 2.4** (Hình 2.1) và **Mục 2.5** (Hình 2.2), tự động điền URL nguồn ảnh từ `raw_images/image_sources.txt` ngay bên dưới mỗi hình.

2. **Bảng ánh xạ trích dẫn `[1]` – `[12]` cho nội dung Chương 2:**
   - Liệt kê chính xác vị trí cần gắn số trích dẫn `[1]`, `[2]`... vào các đoạn văn hiện có trong Chương 2 (Eigenfaces, Fisherfaces, LBPH, HOG+SVM, DeepFace, FaceNet, ArcFace, Haar Cascade, MTCNN, RetinaFace, OpenCV, thư viện `face_recognition`/Dlib) mà **không làm thay đổi văn phong gốc của nhóm**.

3. **Danh mục Tài liệu tham khảo chuẩn (Định dạng IEEE) đã kiểm chứng:**
   Sử dụng chính xác các công trình gốc dưới đây (không tự ý thêm nguồn chưa kiểm chứng):
   - `[1]` M. Turk and A. Pentland, "Eigenfaces for recognition," *Journal of Cognitive Neuroscience*, vol. 3, no. 1, pp. 71–86, 1991.
   - `[2]` P. N. Belhumeur, J. P. Hespanha, and D. J. Kriegman, "Eigenfaces vs. Fisherfaces: recognition using class specific linear projection," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 19, no. 7, pp. 711–720, 1997.
   - `[3]` T. Ahonen, A. Hadid, and M. Pietikainen, "Face description with local binary patterns: application to face recognition," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 28, no. 12, pp. 2037–2041, 2006.
   - `[4]` N. Dalal and B. Triggs, "Histograms of oriented gradients for human detection," in *Proc. IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)*, 2005, pp. 886–893.
   - `[5]` Y. Taigman, M. Yang, M. Ranzato, and L. Wolf, "DeepFace: closing the gap to human-level performance in face verification," in *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2014, pp. 1701–1708.
   - `[6]` F. Schroff, D. Kalenichenko, and J. Philbin, "FaceNet: a unified embedding for face recognition and clustering," in *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2015, pp. 815–823.
   - `[7]` J. Deng, J. Guo, N. Xue, and S. Zafeiriou, "ArcFace: additive angular margin loss for deep face recognition," in *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2019, pp. 4690–4699.
   - `[8]` P. Viola and M. Jones, "Rapid object detection using a boosted cascade of simple features," in *Proc. IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)*, 2001, pp. I-511–I-518.
   - `[9]` K. Zhang, Z. Zhang, Z. Li, and Y. Qiao, "Joint face detection and alignment using multitask cascaded convolutional networks," *IEEE Signal Processing Letters*, vol. 23, no. 10, pp. 1499–1503, 2016.
   - `[10]` J. Deng, J. Guo, E. Ververas, I. Kotsia, and S. Zafeiriou, "RetinaFace: single-shot multi-level face localisation in the wild," in *Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2020, pp. 5203–5212.
   - `[11]` D. E. King, "Dlib-ml: a machine learning toolkit," *Journal of Machine Learning Research*, vol. 10, pp. 1755–1758, 2009. (Tài liệu nền tảng của thư viện `face_recognition`).
   - `[12]` G. Bradski, "The OpenCV Library," *Dr. Dobb's Journal of Software Tools*, 2000.

---

## BƯỚC 4: CHECKLIST BÀN GIAO CHO NHÓM

Sau khi chạy xong 3 bước trên, Antigravity tự kiểm tra và xác nhận lại toàn bộ danh mục bàn giao:
- [ ] Thư mục `dataset/` đã chia chuẩn 3 tập (`registered`, `calibration`, `test`) sẵn sàng để bạn Chương 4 thay thế ảnh người nổi tiếng bằng ảnh thật của thành viên nhóm.
- [ ] Hai ảnh `output_figures/hinh_2_1_phat_hien_diem_moc.jpg` và `output_figures/hinh_2_2_can_chinh_khuon_mat.jpg` hiển thị rõ nét, không lỗi font/lệch khung.
- [ ] File `CHUONG_2_TRICH_DAN_VA_HINH_MINH_HOA.md` có đầy đủ nguồn URL của ảnh mẫu và 12 tài liệu tham khảo chuẩn xác cho Chương 2.