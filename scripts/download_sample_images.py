import os
import requests
import cv2
import face_recognition

headers = {
    'User-Agent': 'FaceRecognitionStudentDemo/1.0 (student.project@university.edu.vn)',
    'Referer': 'https://commons.wikimedia.org/'
}

images_to_download = {
    "personA_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/8/8d/President_Barack_Obama.jpg",
        "https://commons.wikimedia.org/wiki/File:President_Barack_Obama.jpg"
    ),
    "personA_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/e/e9/Official_portrait_of_Barack_Obama.jpg",
        "https://commons.wikimedia.org/wiki/File:Official_portrait_of_Barack_Obama.jpg"
    ),
    "personA_3_tilted.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/1/1a/Barack_Obama_2004.jpg",
        "https://commons.wikimedia.org/wiki/File:Barack_Obama_2004.jpg"
    ),
    "personB_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/3/34/Elon_Musk_Royal_Society_%28crop2%29.jpg",
        "https://commons.wikimedia.org/wiki/File:Elon_Musk_Royal_Society_(crop2).jpg"
    ),
    "personB_2.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/e/ed/Elon_Musk_-_The_Summit_2013.jpg",
        "https://commons.wikimedia.org/wiki/File:Elon_Musk_-_The_Summit_2013.jpg"
    ),
    "personB_3.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/c/cb/Elon_Musk_2015.jpg",
        "https://commons.wikimedia.org/wiki/File:Elon_Musk_2015.jpg"
    ),
    "stranger_1.jpg": (
        "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg",
        "https://commons.wikimedia.org/wiki/File:Lionel-Messi-Argentina-2022-FIFA-World-Cup_(cropped).jpg"
    )
}

raw_dir = "raw_images"
os.makedirs(raw_dir, exist_ok=True)
sources_file = os.path.join(raw_dir, "image_sources.txt")
sources_lines = []

print("=== BẮT ĐẦU TẢI ẢNH MẪU TỪ WIKIMEDIA COMMONS ===")

for filename, (download_url, page_url) in images_to_download.items():
    file_path = os.path.join(raw_dir, filename)
    print(f"Đang tải {filename}...")
    resp = requests.get(download_url, headers=headers, timeout=30)
    if resp.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(resp.content)
        
        # Kiểm tra khuôn mặt
        image = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(image)
        face_count = len(face_locations)
        print(f" -> Thành công ({len(resp.content)} bytes). Số khuôn mặt phát hiện: {face_count}")
        sources_lines.append(f"{filename}: {download_url} (Chi tiết: {page_url})")
    else:
        print(f" -> LỖI tải {filename}: HTTP {resp.status_code}")

with open(sources_file, "w", encoding="utf-8") as f:
    f.write("\n".join(sources_lines) + "\n")

print(f"=== ĐÃ LƯU NGUỒN ẢNH VÀO {sources_file} ===")
