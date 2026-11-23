"""Các bước phát hiện và so khớp khuôn mặt dùng trong demo."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter

import cv2
import numpy as np

MODEL_DIR = Path(__file__).resolve().parent / "models"
DETECT_MODEL = MODEL_DIR / "face_detection_yunet_2023mar.onnx"
RECOGNIZE_MODEL = MODEL_DIR / "face_recognition_sface_2021dec.onnx"


def normalize(feature: np.ndarray) -> np.ndarray:
    """Chuẩn hóa embedding để tính cosine bằng tích vô hướng."""
    data = np.asarray(feature, dtype=np.float32).reshape(-1)
    if data.size == 0 or not np.all(np.isfinite(data)):
        raise ValueError("Dữ liệu đặc trưng không hợp lệ")
    length = float(np.linalg.norm(data))
    if not np.isfinite(length) or length < 1e-8:
        raise ValueError("Không thể chuẩn hóa đặc trưng khuôn mặt")
    return data / length


def compare(feature: np.ndarray, templates: dict[str, np.ndarray]) -> tuple[str | None, float]:
    """Chọn người gần nhất; việc xét ngưỡng được làm ở bước sau."""
    if not templates:
        return None, 0.0
    query = normalize(feature)
    best_name = None
    best_score = -1.0
    for name, reference in templates.items():
        reference = normalize(reference)
        if reference.shape != query.shape:
            continue
        score = float(np.dot(query, reference))
        if score > best_score:
            best_score = score
            best_name = name
    return best_name, best_score if best_name is not None else 0.0


@dataclass
class Recognition:
    status: str
    face_count: int
    name: str | None = None
    candidate: str | None = None
    similarity: float = 0.0
    elapsed_ms: float = 0.0
    face_box: tuple[int, int, int, int] | None = None
    feature: np.ndarray | None = None
    message: str = ""


class FaceEngine:
    def __init__(self, minimum_face_px: int = 90):
        for path in (DETECT_MODEL, RECOGNIZE_MODEL):
            if not path.is_file():
                raise FileNotFoundError(f"Thiếu {path.name}. Chạy download_models.py trước.")
        if not hasattr(cv2, "FaceDetectorYN") or not hasattr(cv2, "FaceRecognizerSF"):
            raise RuntimeError("OpenCV chưa hỗ trợ YuNet/SFace. Hãy cài lại requirements.txt.")
        self.detector = cv2.FaceDetectorYN.create(
            str(DETECT_MODEL), "", (320, 320),
            score_threshold=0.90, nms_threshold=0.3, top_k=5000,
        )
        self.recognizer = cv2.FaceRecognizerSF.create(str(RECOGNIZE_MODEL), "")
        self.minimum_face_px = minimum_face_px

    def analyze(self, frame: np.ndarray, templates: dict[str, np.ndarray], threshold: float) -> Recognition:
        started = perf_counter()
        if frame is None or not isinstance(frame, np.ndarray) or frame.size == 0:
            return Recognition("NO_FACE", 0, message="Không có ảnh từ webcam")
        if frame.ndim != 3 or frame.shape[2] != 3:
            return Recognition("LOW_QUALITY", 0, message="Định dạng ảnh webcam không hợp lệ")

        height, width = frame.shape[:2]
        self.detector.setInputSize((width, height))
        _, faces = self.detector.detect(frame)
        count = len(faces) if faces is not None else 0

        def finish(status: str, **details) -> Recognition:
            return Recognition(
                status=status, face_count=count,
                elapsed_ms=(perf_counter() - started) * 1000,
                **details,
            )

        if count == 0:
            return finish("NO_FACE", message="Không tìm thấy khuôn mặt")
        if count > 1:
            return finish("MULTIPLE_FACES", message="Chỉ để một người đứng trước webcam")

        face = faces[0]
        x, y, face_w, face_h = (int(round(float(n))) for n in face[:4])
        box = (x, y, face_w, face_h)
        if min(face_w, face_h) < self.minimum_face_px:
            return finish("LOW_QUALITY", face_box=box,
                          message="Khuôn mặt quá nhỏ, hãy đứng gần camera hơn")
        if x < 0 or y < 0 or x + face_w > width or y + face_h > height:
            return finish("LOW_QUALITY", face_box=box,
                          message="Khuôn mặt nằm ngoài khung hình")

        try:
            aligned_face = self.recognizer.alignCrop(frame, face)
            feature = normalize(self.recognizer.feature(aligned_face))
        except (cv2.error, ValueError) as exc:
            return finish("LOW_QUALITY", face_box=box,
                          message=f"Không lấy được đặc trưng: {exc}")

        # Dù chưa có dữ liệu đăng ký vẫn trả lại feature để có thể lấy mẫu.
        if not templates:
            return finish("NO_DB", face_box=box, feature=feature,
                          message="Chưa có người được đăng ký")

        candidate, score = compare(feature, templates)
        if candidate is not None and score >= threshold:
            return finish("MATCH", name=candidate, candidate=candidate,
                          similarity=score, face_box=box, feature=feature,
                          message=f"Đã nhận diện: {candidate}")
        return finish("UNKNOWN", candidate=candidate, similarity=score,
                      face_box=box, feature=feature, message="Chưa xác định")
