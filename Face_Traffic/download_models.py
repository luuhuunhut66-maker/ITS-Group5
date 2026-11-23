"""Download pretrained OpenCV Zoo models from the official OpenCV Hugging Face repositories."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent
MODELS = {
    "face_detection_yunet_2023mar.onnx": (
        [
            "https://huggingface.co/opencv/face_detection_yunet/resolve/main/face_detection_yunet_2023mar.onnx",
            "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
        ],
        100_000,
    ),
    "face_recognition_sface_2021dec.onnx": (
        [
            "https://huggingface.co/opencv/face_recognition_sface/resolve/main/face_recognition_sface_2021dec.onnx",
            "https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx",
        ],
        20_000_000,
    ),
}


def download_one(name: str, urls: list[str], minimum_bytes: int, target_dir: Path, force: bool = False) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    dest = target_dir / name
    if dest.exists() and dest.stat().st_size >= minimum_bytes and not force:
        print(f"[OK] Đã có: {name} ({dest.stat().st_size / 1e6:.1f} MB)")
        return dest
    failures: list[str] = []
    for url in urls:
        print(f"Đang tải {name} từ {url.split('/')[2]} ...")
        fd, temp_name = tempfile.mkstemp(dir=target_dir, prefix=".download_", suffix=".part")
        os.close(fd)
        temp = Path(temp_name)
        try:
            request = Request(url, headers={"User-Agent": "FaceTrafficDemo/1.0"})
            with urlopen(request, timeout=90) as response, temp.open("wb") as f:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
            if temp.stat().st_size < minimum_bytes:
                raise RuntimeError(f"File quá nhỏ ({temp.stat().st_size} bytes): tải chưa hoàn tất")
            with temp.open("rb") as f:
                if f.read(40).startswith(b"version https://git-lfs"):
                    raise RuntimeError("Tải nhầm Git LFS pointer")
            temp.replace(dest)
            print(f"[OK] {dest.name} ({dest.stat().st_size / 1e6:.1f} MB)")
            return dest
        except Exception as exc:
            failures.append(f"{url.split('/')[2]}: {exc}")
            print(f"Không tải được từ nguồn này: {exc}")
        finally:
            temp.unlink(missing_ok=True)
    raise RuntimeError("Không tải được mô hình. Kiểm tra Internet hoặc tải thủ công từ OpenCV Zoo.\n" + "\n".join(failures))


def main() -> None:
    parser = argparse.ArgumentParser(description="Tải các mô hình OpenCV Zoo dùng cho demo")
    parser.add_argument("--force", action="store_true", help="Tải lại ngay cả khi mô hình đã có")
    args = parser.parse_args()
    for name, (urls, size) in MODELS.items():
        download_one(name, urls, size, BASE / "models", args.force)
    print("Hoàn tất. Chạy: python app.py")


if __name__ == "__main__":
    main()
