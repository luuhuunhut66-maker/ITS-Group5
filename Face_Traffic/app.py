"""Chương trình demo nhận diện khuôn mặt bằng webcam."""

import os
import time
import tkinter as tk
from tkinter import ttk, messagebox

import cv2
from PIL import Image, ImageTk

from face_engine import FaceEngine
from report import CASES, UNKNOWN_LABEL, ExperimentLog
from storage import FaceDatabase, Settings


class FaceTrafficApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Demo nhận diện khuôn mặt trong giao thông")
        self.root.geometry("1280x850")
        self.root.minsize(1100, 720)

        self.database = FaceDatabase()
        self.settings = Settings()
        self.report = ExperimentLog()
        self.people_features = self.database.templates()

        self.engine = None
        self.camera = None
        self.camera_running = False
        self.after_id = None
        self.latest_frame = None
        self.latest_result = None
        self.photo = None

        self.camera_number = tk.StringVar(value="0")
        self.threshold_value = tk.StringVar(value=str(self.settings.get_threshold()))
        self.status_text = tk.StringVar(value="Chưa mở webcam")
        self.name_text = tk.StringVar(value="-")
        self.score_text = tk.StringVar(value="-")
        self.time_text = tk.StringVar(value="-")

        self.person_name = tk.StringVar()
        self.consent = tk.BooleanVar(value=False)
        self.registration_text = tk.StringVar(value="Chưa bắt đầu đăng ký")
        self.registering = False
        self.register_features = []
        self.last_sample_time = 0

        self.case_value = tk.StringVar(value="TC01")
        self.case_display_value = tk.StringVar(value="TC01 - " + CASES["TC01"])
        self.case_description_text = tk.StringVar(value=CASES["TC01"])
        self.expected_value = tk.StringVar(value=UNKNOWN_LABEL)
        self.note_value = tk.StringVar()

        self.build_window()
        self.refresh_people()
        self.refresh_test_table()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def build_window(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab", padding=(14, 8))
        style.configure("Title.TLabel", font=("Segoe UI", 17, "bold"))
        style.configure("Info.TLabel", font=("Segoe UI", 10))
        style.configure("TButton", padding=(9, 6))
        style.configure("Treeview", rowheight=25)

        header = ttk.Frame(self.root, padding=(18, 14))
        header.pack(fill="x")
        ttk.Label(header, text="NHẬN DIỆN KHUÔN MẶT TRONG GIAO THÔNG",
                  style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Đăng ký và nhận diện người tham gia trên cùng một màn hình",
                  foreground="#555555").pack(anchor="w", pady=(3, 0))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Đăng ký và nhận diện được bố trí chung trên một trang.
        self.camera_tab = ttk.Frame(self.tabs, padding=10)
        self.test_tab = ttk.Frame(self.tabs, padding=12)
        self.tabs.add(self.camera_tab, text="Nhận diện & đăng ký")
        self.tabs.add(self.test_tab, text="Kiểm thử")

        self.build_camera_tab()
        self.build_test_tab()

    def build_camera_tab(self):
        self.camera_tab.columnconfigure(0, weight=3)
        self.camera_tab.columnconfigure(1, weight=2)
        self.camera_tab.rowconfigure(0, weight=1)
        self.camera_tab.rowconfigure(1, weight=0)

        video_frame = ttk.LabelFrame(self.camera_tab, text="Hình ảnh từ webcam", padding=8)
        video_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10), pady=(0, 8))
        self.video_label = tk.Label(
            video_frame, text="Nhấn 'Mở webcam' để bắt đầu",
            bg="#202020", fg="white", font=("Segoe UI", 12),
            width=68, height=28,
        )
        self.video_label.pack(fill="both", expand=True)

        right = ttk.Frame(self.camera_tab)
        right.grid(row=0, column=1, sticky="nsew", pady=(0, 8))

        camera_box = ttk.LabelFrame(right, text="Điều khiển camera", padding=9)
        camera_box.pack(fill="x", pady=(0, 8))
        ttk.Label(camera_box, text="Số webcam (thường là 0):").grid(row=0, column=0, sticky="w")
        ttk.Entry(camera_box, textvariable=self.camera_number, width=7).grid(row=0, column=1, padx=5)
        ttk.Button(camera_box, text="Mở webcam", command=self.start_camera).grid(row=0, column=2, padx=3)
        ttk.Button(camera_box, text="Tắt webcam", command=self.stop_camera).grid(row=0, column=3, padx=3)

        result_box = ttk.LabelFrame(right, text="Kết quả nhận diện", padding=9)
        result_box.pack(fill="x", pady=(0, 8))
        result_grid = ttk.Frame(result_box)
        result_grid.pack(fill="x")
        ttk.Label(result_grid, text="Trạng thái:").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Label(result_grid, textvariable=self.status_text, style="Info.TLabel",
                  wraplength=300).grid(row=0, column=1, sticky="w")
        ttk.Label(result_grid, text="Danh tính:").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=3)
        ttk.Label(result_grid, textvariable=self.name_text,
                  font=("Segoe UI", 12, "bold")).grid(row=1, column=1, sticky="w")
        ttk.Label(result_grid, text="Độ tương đồng:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=3)
        ttk.Label(result_grid, textvariable=self.score_text).grid(row=2, column=1, sticky="w")
        ttk.Label(result_grid, text="Thời gian xử lý:").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=3)
        ttk.Label(result_grid, textvariable=self.time_text).grid(row=3, column=1, sticky="w")

        setting_row = ttk.Frame(result_box)
        setting_row.pack(fill="x", pady=(7, 0))
        ttk.Label(setting_row, text="Ngưỡng cosine:").pack(side="left")
        ttk.Entry(setting_row, textvariable=self.threshold_value, width=8).pack(side="left", padx=5)
        ttk.Button(setting_row, text="Lưu ngưỡng", command=self.save_threshold).pack(side="left")
        ttk.Label(result_box, text="Ngưỡng mặc định 0.363; nên hiệu chỉnh bằng dữ liệu thực tế của nhóm.",
                  wraplength=450, foreground="#555555").pack(anchor="w", pady=(5, 0))

        registration_box = ttk.LabelFrame(right, text="Đăng ký khuôn mặt", padding=10)
        registration_box.pack(fill="both", expand=True)
        ttk.Label(registration_box, text="Họ tên người tham gia:").pack(anchor="w")
        ttk.Entry(registration_box, textvariable=self.person_name).pack(fill="x", pady=(3, 6))
        ttk.Checkbutton(
            registration_box,
            text="Người tham gia đồng ý cho sử dụng dữ liệu khuôn mặt",
            variable=self.consent,
        ).pack(anchor="w", pady=(0, 6))
        registration_buttons = ttk.Frame(registration_box)
        registration_buttons.pack(fill="x")
        ttk.Button(registration_buttons, text="Bắt đầu lấy 12 mẫu",
                   command=self.start_registration).pack(side="left", padx=(0, 6))
        ttk.Button(registration_buttons, text="Hủy đăng ký",
                   command=self.cancel_registration).pack(side="left")
        ttk.Label(registration_box, textvariable=self.registration_text,
                  wraplength=440, foreground="#245b8f").pack(anchor="w", pady=(7, 3))
        ttk.Label(registration_box,
                  text="Cách dùng: mở webcam, nhập tên, tích đồng ý rồi bắt đầu lấy mẫu. Nhìn camera và xoay nhẹ mặt đến khi đủ 12 mẫu. Có thể đăng ký và nhận diện ngay tại trang này.",
                  wraplength=450, justify="left", foreground="#555555").pack(anchor="w")

        people_box = ttk.LabelFrame(self.camera_tab, text="Danh sách người đã đăng ký", padding=7)
        people_box.grid(row=2, column=0, columnspan=2, sticky="nsew")
        people_box.columnconfigure(0, weight=1)
        self.people_table = ttk.Treeview(
            people_box, columns=("name", "samples"), show="headings", height=4
        )
        self.people_table.heading("name", text="Họ tên")
        self.people_table.heading("samples", text="Số mẫu")
        self.people_table.column("name", width=260)
        self.people_table.column("samples", width=100, anchor="center")
        self.people_table.grid(row=0, column=0, sticky="nsew")
        people_scroll = ttk.Scrollbar(people_box, orient="vertical", command=self.people_table.yview)
        people_scroll.grid(row=0, column=1, sticky="ns")
        self.people_table.configure(yscrollcommand=people_scroll.set)
        ttk.Button(people_box, text="Xóa người được chọn", command=self.delete_person).grid(
            row=0, column=2, sticky="ns", padx=(8, 0)
        )

    def build_test_tab(self):
        test_form = ttk.LabelFrame(self.test_tab, text="Ghi một lượt kiểm thử", padding=10)
        test_form.pack(fill="x", pady=(0, 10))

        ttk.Label(test_form, text="Kịch bản kiểm thử:").grid(row=0, column=0, sticky="w", padx=5)
        scenario_values = [f"{code} - {description}" for code, description in CASES.items()]
        self.case_box = ttk.Combobox(
            test_form, textvariable=self.case_display_value,
            values=scenario_values, state="readonly", width=48
        )
        self.case_box.grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.case_box.bind("<<ComboboxSelected>>", self.case_changed)

        ttk.Label(test_form, text="Danh tính thực tế:").grid(row=0, column=1, sticky="w", padx=5)
        self.expected_box = ttk.Combobox(test_form, textvariable=self.expected_value,
                                         state="readonly", width=22)
        self.expected_box.grid(row=1, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(test_form, text="Ghi chú điều kiện thử:").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Entry(test_form, textvariable=self.note_value, width=30).grid(
            row=1, column=2, sticky="ew", padx=5, pady=4
        )
        test_form.columnconfigure(2, weight=1)
        ttk.Label(test_form, textvariable=self.case_description_text,
                  foreground="#245b8f", wraplength=850).grid(
            row=2, column=0, columnspan=3, sticky="w", padx=5, pady=(4, 7)
        )

        buttons = ttk.Frame(test_form)
        buttons.grid(row=3, column=0, columnspan=4, sticky="w", pady=(4, 0))
        ttk.Button(buttons, text="Ghi mẫu hiệu chỉnh", command=self.record_calibration).pack(side="left", padx=(3, 8))
        ttk.Button(buttons, text="Ghi kết quả kiểm thử", command=self.record_test).pack(side="left", padx=3)
        ttk.Button(buttons, text="Xuất bảng tổng hợp", command=self.export_report).pack(side="left", padx=3)
        ttk.Label(test_form,
                  text="TC01: đã đăng ký, nhìn thẳng/đủ sáng | TC02: đã đăng ký, nghiêng mặt | TC03: đã đăng ký, ánh sáng yếu | TC04: đã đăng ký, thay đổi khoảng cách | TC05: đã đăng ký, đeo kính/che một phần mặt | TC06: người chưa đăng ký.",
                  foreground="#555555", wraplength=1000, justify="left").grid(
            row=4, column=0, columnspan=4, sticky="w", padx=5, pady=(8, 0)
        )

        table_box = ttk.LabelFrame(self.test_tab, text="Các lượt đã ghi", padding=8)
        table_box.pack(fill="both", expand=True)
        columns = ("case", "expected", "predicted", "result", "score", "time")
        self.test_table = ttk.Treeview(table_box, columns=columns, show="headings", height=14)
        headings = {
            "case": "Kịch bản kiểm thử", "expected": "Danh tính thật", "predicted": "Kết quả nhận diện",
            "result": "Đánh giá", "score": "Độ tương đồng", "time": "Thời gian (ms)",
        }
        widths = {"case": 390, "expected": 150, "predicted": 150,
                  "result": 120, "score": 100, "time": 110}
        for col in columns:
            self.test_table.heading(col, text=headings[col])
            self.test_table.column(col, width=widths[col], anchor="center")
        self.test_table.pack(fill="both", expand=True)
        ttk.Label(self.test_tab,
                  text="Mở webcam ở trang 'Nhận diện & đăng ký' trước khi ghi kết quả. Mỗi dòng được lưu từ một lượt thử thực tế.",
                  foreground="#555555").pack(anchor="w", pady=(8, 0))

    def start_camera(self):
        if self.camera_running:
            return
        try:
            index = int(self.camera_number.get())
            if index < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Camera", "Số webcam phải là số nguyên không âm.")
            return

        try:
            if self.engine is None:
                self.engine = FaceEngine()
            if os.name == "nt":
                self.camera = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            else:
                self.camera = cv2.VideoCapture(index)
            if not self.camera.isOpened():
                self.camera.release()
                self.camera = None
                messagebox.showerror("Camera", "Không mở được webcam. Hãy kiểm tra camera hoặc thử số 1.")
                return
        except Exception as error:
            messagebox.showerror("Không khởi động được", str(error))
            return

        self.camera_running = True
        self.status_text.set("Đang mở webcam")
        self.update_camera()

    def stop_camera(self):
        self.camera_running = False
        if self.registering:
            self.registering = False
            self.register_features = []
            self.registration_text.set("Đã dừng đăng ký.")
        if self.after_id is not None:
            try:
                self.root.after_cancel(self.after_id)
            except tk.TclError:
                pass
            self.after_id = None
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.video_label.configure(image="", text="Webcam đã tắt")
        self.video_label.image = None
        self.photo = None
        self.latest_frame = None
        self.latest_result = None
        self.status_text.set("Chưa mở webcam")
        self.name_text.set("-")
        self.score_text.set("-")
        self.time_text.set("-")

    def update_camera(self):
        if not self.camera_running or self.camera is None:
            return

        ok, frame = self.camera.read()
        if not ok:
            self.stop_camera()
            messagebox.showerror("Camera", "Không đọc được hình ảnh từ webcam.")
            return

        frame = cv2.flip(frame, 1)
        self.latest_frame = frame.copy()
        try:
            threshold = self.settings.get_threshold()
            result = self.engine.analyze(frame, self.people_features, threshold)
            self.latest_result = result
        except Exception as error:
            self.status_text.set("Lỗi xử lý hình ảnh: " + str(error))
            self.after_id = self.root.after(100, self.update_camera)
            return

        if result.face_box:
            x, y, width, height = result.face_box
            color = (40, 180, 40) if result.status == "MATCH" else (30, 150, 230)
            cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)

        self.show_frame(frame)
        self.update_result(result)
        self.collect_registration_sample(result)
        self.after_id = self.root.after(30, self.update_camera)

    def show_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)
        image.thumbnail((760, 520), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)
        self.video_label.configure(image=self.photo, text="")
        self.video_label.image = self.photo

    def update_result(self, result):
        messages = {
            "MATCH": "Đã nhận diện",
            "UNKNOWN": "Chưa xác định",
            "NO_DB": "Chưa có dữ liệu đăng ký",
            "NO_FACE": "Không tìm thấy khuôn mặt",
            "MULTIPLE_FACES": "Có nhiều hơn một khuôn mặt",
            "LOW_QUALITY": "Ảnh chưa đủ rõ",
        }
        self.status_text.set(messages.get(result.status, result.message))
        self.name_text.set(result.name or UNKNOWN_LABEL)
        self.score_text.set(f"{result.similarity:.3f}" if result.candidate else "-")
        self.time_text.set(f"{result.elapsed_ms:.1f} ms")

    def start_registration(self):
        name = " ".join(self.person_name.get().split())
        if not name:
            messagebox.showwarning("Đăng ký", "Bạn chưa nhập họ tên.")
            return
        if not self.consent.get():
            messagebox.showwarning("Đăng ký", "Cần có sự đồng ý của người tham gia.")
            return
        if not self.camera_running:
            messagebox.showwarning("Đăng ký", "Hãy mở webcam ở tab Nhận diện trước.")
            return

        existing = [person for person in self.database.list_people()
                    if person["name"].casefold() == name.casefold()]
        if existing and not messagebox.askyesno(
            "Đăng ký lại", f"{name} đã có trong danh sách. Bạn muốn thay mẫu cũ không?"
        ):
            return

        self.registering = True
        self.register_features = []
        self.last_sample_time = 0
        self.registration_text.set("Đang lấy mẫu: 0/12")

    def collect_registration_sample(self, result):
        if not self.registering:
            return
        if result.feature is None or result.face_count != 1:
            self.registration_text.set(
                f"Đang lấy mẫu: {len(self.register_features)}/12. {result.message}"
            )
            return

        now = time.time()
        if now - self.last_sample_time < 0.55:
            return
        self.last_sample_time = now
        self.register_features.append(result.feature.copy())
        count = len(self.register_features)
        self.registration_text.set(f"Đang lấy mẫu: {count}/12. Hãy xoay nhẹ mặt.")

        if count == 12:
            try:
                self.database.add_or_replace(
                    self.person_name.get(), self.register_features, consent=self.consent.get()
                )
                self.people_features = self.database.templates()
                self.refresh_people()
                self.registration_text.set("Đăng ký thành công.")
                self.registering = False
                self.register_features = []
                messagebox.showinfo("Đăng ký", "Đã lưu 12 mẫu khuôn mặt.")
            except Exception as error:
                self.registering = False
                self.register_features = []
                messagebox.showerror("Đăng ký", str(error))

    def cancel_registration(self):
        self.registering = False
        self.register_features = []
        self.registration_text.set("Đã hủy đăng ký.")

    def refresh_people(self):
        if hasattr(self, "people_table"):
            for item in self.people_table.get_children():
                self.people_table.delete(item)
            for person in self.database.list_people():
                self.people_table.insert("", "end", values=(person["name"], person["samples"]))
        if hasattr(self, "expected_box"):
            names = [person["name"] for person in self.database.list_people()]
            self.expected_box["values"] = names + [UNKNOWN_LABEL]
            if self.case_value.get() == "TC06":
                self.expected_value.set(UNKNOWN_LABEL)
            elif names and self.expected_value.get() not in names:
                self.expected_value.set(names[0])

    def delete_person(self):
        selected = self.people_table.selection()
        if not selected:
            messagebox.showwarning("Xóa dữ liệu", "Chọn một người trong danh sách trước.")
            return
        values = self.people_table.item(selected[0], "values")
        name = values[0]
        if messagebox.askyesno("Xóa dữ liệu", f"Bạn có muốn xóa mẫu khuôn mặt của {name} không?"):
            self.database.delete(name)
            self.people_features = self.database.templates()
            self.refresh_people()

    def save_threshold(self):
        try:
            value = float(self.threshold_value.get())
            self.settings.set_threshold(value)
            self.threshold_value.set(f"{value:.3f}")
            messagebox.showinfo("Ngưỡng", "Đã lưu ngưỡng so khớp.")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Ngưỡng không hợp lệ", str(error))

    def case_changed(self, _event=None):
        selected = self.case_display_value.get()
        code = selected.split(" - ", 1)[0].strip()
        if code not in CASES:
            code = "TC01"
        self.case_value.set(code)
        self.case_description_text.set(f"{code}: {CASES[code]}")
        if code == "TC06":
            self.expected_value.set(UNKNOWN_LABEL)
        else:
            names = [person["name"] for person in self.database.list_people()]
            self.expected_value.set(names[0] if names else UNKNOWN_LABEL)

    def record_test(self):
        if not self.camera_running or self.latest_result is None:
            messagebox.showwarning("Kiểm thử", "Hãy mở webcam trước khi ghi kết quả.")
            return

        case = self.case_value.get()
        expected = self.expected_value.get()
        names = [person["name"] for person in self.database.list_people()]
        if case != "TC06" and expected not in names:
            messagebox.showwarning("Kiểm thử", "Hãy đăng ký và chọn người tham gia trước.")
            return
        if case == "TC06" and expected != UNKNOWN_LABEL:
            messagebox.showwarning("Kiểm thử", "TC06 dành cho người chưa đăng ký.")
            return

        try:
            self.report.record(
                case, expected, self.latest_result,
                self.settings.get_threshold(), self.note_value.get()
            )
            self.refresh_test_table()
            messagebox.showinfo("Kiểm thử", "Đã lưu kết quả vào thư mục data.")
        except Exception as error:
            messagebox.showerror("Kiểm thử", str(error))

    def record_calibration(self):
        if not self.camera_running or self.latest_result is None:
            messagebox.showwarning("Hiệu chỉnh", "Hãy mở webcam trước khi ghi mẫu.")
            return
        expected = self.expected_value.get()
        names = [person["name"] for person in self.database.list_people()]
        if expected != UNKNOWN_LABEL and expected not in names:
            messagebox.showwarning("Hiệu chỉnh", "Hãy chọn người đã đăng ký hoặc Chưa đăng ký.")
            return
        try:
            self.report.record_calibration(expected, self.latest_result)
            messagebox.showinfo("Hiệu chỉnh", "Đã lưu mẫu riêng vào data/calibration.csv.")
        except Exception as error:
            messagebox.showerror("Hiệu chỉnh", str(error))

    def refresh_test_table(self):
        if not hasattr(self, "test_table"):
            return
        for item in self.test_table.get_children():
            self.test_table.delete(item)
        rows = self.report.read_trials()
        for row in rows[-100:]:
            code = row["Kịch bản"]
            scenario = f"{code} - {CASES.get(code, 'Không rõ kịch bản')}"
            self.test_table.insert("", "end", values=(
                scenario, row["Danh tính thật"], row["Kết quả nhận diện"],
                row["Đánh giá"], row["Độ tương đồng"], row["Thời gian xử lý (ms)"],
            ))

    def export_report(self):
        try:
            path = self.report.export_summary()
            messagebox.showinfo(
                "Xuất báo cáo",
                f"Đã xuất bảng tổng hợp:\n{path}\n\n"
                f"Dữ liệu từng lượt thử:\n{self.report.trials_file}"
            )
        except Exception as error:
            messagebox.showerror("Xuất báo cáo", str(error))

    def close(self):
        self.stop_camera()
        self.root.destroy()


def main():
    root = tk.Tk()
    FaceTrafficApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
