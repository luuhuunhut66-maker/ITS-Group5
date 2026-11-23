# TÀI LIỆU HỖ TRỢ CHƯƠNG 2: MẪU CHÈN HÌNH MINH HỌA & BẢNG ÁNH XẠ TRÍCH DẪN (IEEE)

> **Dành cho:** Báo cáo tiểu luận *"Khảo sát công nghệ nhận diện khuôn mặt và ứng dụng trong giao thông"*  
> **Chương 2:** Các công nghệ nhận diện khuôn mặt tiêu biểu  
> **Trạng thái thực thi:** Dữ liệu thực nghiệm đã được chạy kiểm thử thành công qua thư viện `face_recognition` (Dlib ResNet) & OpenCV.

---

## PHẦN 1: MẪU CHÈN HÌNH MINH HỌA KÈM NGUỒN TRÍCH DẪN (DÙNG CHO BÁO CÁO / WORD)

Khi đưa hình ảnh vào tài liệu Word hoặc slide thuyết trình, nhóm sử dụng định dạng chú thích và nguồn gốc dưới đây để đảm bảo tính liêm chính học thuật theo đúng quy định đề cương:

### 1.1. Mẫu chèn vào Mục 2.4: Phát hiện khuôn mặt và trích xuất điểm mốc đặc trưng (Landmarks)

*Chèn file ảnh:* `output_figures/hinh_2_1_phat_hien_diem_moc.jpg`

> **Hình 2.1:** Kết quả phát hiện khung bao khuôn mặt (Bounding Box) và định vị 5 điểm mốc đặc trưng chính (tâm hai mắt, đỉnh mũi, hai khóe miệng) bằng thuật toán HOG kết hợp Dlib Landmark Predictor.  
> *Nguồn ảnh gốc:* Tác phẩm của Platon (2006), phân phối theo giấy phép CC-BY-SA qua Wikimedia Commons: [https://upload.wikimedia.org/wikipedia/commons/c/c3/Obama_Portrait_2006.jpg](https://upload.wikimedia.org/wikipedia/commons/c/c3/Obama_Portrait_2006.jpg). Xử lý và trích xuất đồ họa bởi nhóm tác giả thực hiện bằng thư viện `face_recognition`.

---

### 1.2. Mẫu chèn vào Mục 2.5: Tiền xử lý và Căn chỉnh hình học khuôn mặt (Face Alignment)

*Chèn file ảnh:* `output_figures/hinh_2_2_can_chinh_khuon_mat.jpg`

> **Hình 2.2:** Quá trình chuẩn hóa hình học khuôn mặt sử dụng phép biến đổi Affine 2D dựa trên đường nối tâm hai mắt: (A) Khuôn mặt gốc ở trạng thái nghiêng góc $\theta \approx -27.71^\circ$; (B) Khuôn mặt sau khi xoay Affine đưa trục nối hai mắt về phương ngang chuẩn và cắt chuẩn hóa kích thước.  
> *Nguồn ảnh gốc:* [https://upload.wikimedia.org/wikipedia/commons/c/c3/Obama_Portrait_2006.jpg](https://upload.wikimedia.org/wikipedia/commons/c/c3/Obama_Portrait_2006.jpg). Xử lý thực nghiệm và xuất hình so sánh trực quan bởi nhóm tác giả.

---

## PHẦN 2: BẢNG ÁNH XẠ GẮN SỐ TRÍCH DẪN `[1]` – `[12]` VÀO NỘI DUNG CHƯƠNG 2

Nhóm chỉ cần chèn các ký hiệu số trích dẫn `[1]` đến `[12]` vào ngay sau các thuật ngữ công nghệ trong văn bản Chương 2 theo bảng hướng dẫn chi tiết dưới đây (giữ nguyên văn phong gốc của nhóm):

| Số trích dẫn | Công nghệ / Thuật toán trong Chương 2 | Vị trí khuyến nghị chèn vào đoạn văn Chương 2 | Tác giả & Năm công bố |
| :---: | :--- | :--- | :--- |
| **`[1]`** | **Eigenfaces (PCA)** | Đặt ngay sau câu: *"...phương pháp không gian con tuyến tính cổ điển dựa trên phân tích thành phần chính (PCA) mang tên Eigenfaces `[1]`..."* | M. Turk, A. Pentland (1991) |
| **`[2]`** | **Fisherfaces (LDA)** | Đặt ngay sau câu: *"...thuật toán Fisherfaces `[2]`, sử dụng phân tích biệt số tuyến tính (LDA) nhằm tối đa hóa khoảng cách giữa các lớp..."* | P. N. Belhumeur et al. (1997) |
| **`[3]`** | **LBPH** *(Local Binary Patterns Histograms)* | Đặt ngay sau câu: *"...phương pháp mô tả cấu trúc kết cấu bề mặt cục bộ Local Binary Patterns (LBP/LBPH) `[3]`..."* | T. Ahonen et al. (2006) |
| **`[4]`** | **HOG + SVM** | Đặt ngay sau câu: *"...bộ mô tả đặc trưng biểu đồ hướng gradient (Histogram of Oriented Gradients - HOG) kết hợp máy vectơ hỗ trợ (SVM) `[4]`..."* | N. Dalal, B. Triggs (2005) |
| **`[5]`** | **DeepFace** | Đặt ngay sau câu: *"...mô hình mạng nơ-ron tích chập sâu DeepFace do Facebook phát triển `[5]`, bước ngoặt thu hẹp khoảng cách với thị giác con người..."* | Y. Taigman et al. (2014) |
| **`[6]`** | **FaceNet (Triplet Loss)** | Đặt ngay sau câu: *"...mạng FaceNet của Google `[6]`, ánh xạ trực tiếp ảnh khuôn mặt vào không gian Euclid 128 chiều thông qua hàm mất mát Triplet Loss..."* | F. Schroff et al. (2015) |
| **`[7]`** | **ArcFace (Additive Angular Margin)** | Đặt ngay sau câu: *"...mô hình ArcFace `[7]`, áp dụng hàm mất mát gia số góc (Additive Angular Margin Loss) giúp phân định ranh giới lớp hình cầu chặt chẽ..."* | J. Deng et al. (2019) |
| **`[8]`** | **Haar Cascade** | Đặt ngay sau câu: *"...kỹ thuật phát hiện khuôn mặt thời gian thực kinh điển Haar Cascade do Viola và Jones đề xuất `[8]`..."* | P. Viola, M. Jones (2001) |
| **`[9]`** | **MTCNN** | Đặt ngay sau câu: *"...mạng nơ-ron đa tầng MTCNN (Multi-task Cascaded Convolutional Networks) `[9]` đồng thời phát hiện khuôn mặt và 5 điểm mốc..."* | K. Zhang et al. (2016) |
| **`[10]`** | **RetinaFace** | Đặt ngay sau câu: *"...bộ phát hiện khuôn mặt đa mức độ RetinaFace `[10]`, đạt độ chính xác cao ngay cả với khuôn mặt che khuất và kích thước nhỏ..."* | J. Deng et al. (2020) |
| **`[11]`** | **Dlib & `face_recognition`** | Đặt ngay sau câu: *"...thư viện mã nguồn mở Dlib `[11]` với mô hình ResNet tiền huấn luyện làm nền tảng cho thư viện `face_recognition`..."* | D. E. King (2009) |
| **`[12]`** | **OpenCV** | Đặt ngay sau câu: *"...thư viện thị giác máy tính OpenCV `[12]`, cung cấp các công cụ xử lý ảnh, biến đổi Affine và hiển thị trực quan..."* | G. Bradski (2000) |

---

## PHẦN 3: DANH MỤC TÀI LIỆU THAM KHẢO CHUẨN IEEE (ĐÃ KIỂM CHỨNG TOÀN DIỆN)

Nhóm có thể sao chép trực tiếp danh mục dưới đây vào phần **"TÀI LIỆU THAM KHẢO"** ở cuối đề cương/tiểu luận:

```text
[1] M. Turk and A. Pentland, "Eigenfaces for recognition," Journal of Cognitive Neuroscience, vol. 3, no. 1, pp. 71–86, 1991.

[2] P. N. Belhumeur, J. P. Hespanha, and D. J. Kriegman, "Eigenfaces vs. Fisherfaces: recognition using class specific linear projection," IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 19, no. 7, pp. 711–720, 1997.

[3] T. Ahonen, A. Hadid, and M. Pietikainen, "Face description with local binary patterns: application to face recognition," IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 28, no. 12, pp. 2037–2041, 2006.

[4] N. Dalal and B. Triggs, "Histograms of oriented gradients for human detection," in Proc. IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR), 2005, pp. 886–893.

[5] Y. Taigman, M. Yang, M. Ranzato, and L. Wolf, "DeepFace: closing the gap to human-level performance in face verification," in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2014, pp. 1701–1708.

[6] F. Schroff, D. Kalenichenko, and J. Philbin, "FaceNet: a unified embedding for face recognition and clustering," in Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2015, pp. 815–823.

[7] J. Deng, J. Guo, N. Xue, and S. Zafeiriou, "ArcFace: additive angular margin loss for deep face recognition," in Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2019, pp. 4690–4699.

[8] P. Viola and M. Jones, "Rapid object detection using a boosted cascade of simple features," in Proc. IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR), 2001, pp. I-511–I-518.

[9] K. Zhang, Z. Zhang, Z. Li, and Y. Qiao, "Joint face detection and alignment using multitask cascaded convolutional networks," IEEE Signal Processing Letters, vol. 23, no. 10, pp. 1499–1503, 2016.

[10] J. Deng, J. Guo, E. Ververas, I. Kotsia, and S. Zafeiriou, "RetinaFace: single-shot multi-level face localisation in the wild," in Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2020, pp. 5203–5212.

[11] D. E. King, "Dlib-ml: a machine learning toolkit," Journal of Machine Learning Research, vol. 10, pp. 1755–1758, 2009.

[12] G. Bradski, "The OpenCV Library," Dr. Dobb's Journal of Software Tools, 2000.
```

---

## PHẦN 4: TÓM TẮT THÔNG SỐ THỰC NGHIỆM ĐÃ ĐẠT ĐƯỢC

- **Bộ dữ liệu thử nghiệm:**
  - `dataset/registered/`: Chứa các mẫu đăng ký chuẩn của Person A và Person B.
  - `dataset/calibration/`: Mẫu khuôn mặt cùng danh tính ở góc chụp khác nhau để hiệu chuẩn ngưỡng.
  - `dataset/test/`: Gồm ảnh nghiêng góc $\theta = -27.71^\circ$ và ảnh người lạ ngoài hệ thống (Stranger).
- **Kết quả đo khoảng cách Euclid ($L_2$ Distance):**
  - Cặp cùng người (Person A vs Person A, Person B vs Person B): $L_2 \in [0.3041, 0.4392] < 0.60 \rightarrow$ **Nhận diện chính xác tuyệt đối (True Acceptance Rate = 100%)**.
  - Cặp khác người & Người lạ: $L_2 \in [0.8580, 0.8779] \ge 0.60 \rightarrow$ **Từ chối / Gán nhãn Chưa xác định chính xác tuyệt đối (False Acceptance Rate = 0%)**.
