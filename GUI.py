import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QPushButton, QSlider, QWidget, QHBoxLayout, QGridLayout, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap

class ObjectDetectionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        # Nilai HSV untuk warna oranye
        self.lh, self.ls, self.lv = 10, 150, 150
        self.uh, self.us, self.uv = 25, 255, 255

        # Output state
        self.output_state = 0

        # Setup GUI
        self.init_ui()

    def init_ui(self):
        # Video displays
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(400, 300)
        self.video_label.setStyleSheet("border: 2px solid black;")
        
        self.video_bw_label = QLabel(self)
        self.video_bw_label.setFixedSize(400, 300)
        self.video_bw_label.setStyleSheet("border: 2px solid black;")

        # Data display
        self.x_label = QLabel("0", self)
        self.y_label = QLabel("0", self)
        self.distance_label = QLabel("0", self)
        self.video_label.setStyleSheet("border: 2px solid black;")
        # Output buttons
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.start_button.setStyleSheet("background-color: green; color: white;")
        self.stop_button.setStyleSheet("background-color: red; color: white;")
        
        # Trackbars
        self.lh_slider = self.create_slider(0, 255, self.lh)
        self.ls_slider = self.create_slider(0, 255, self.ls)
        self.lv_slider = self.create_slider(0, 255, self.lv)
        self.uh_slider = self.create_slider(0, 255, self.uh)
        self.us_slider = self.create_slider(0, 255, self.us)
        self.uv_slider = self.create_slider(0, 255, self.uv)

        # Layout
        video_layout = QGridLayout()
        video_layout.addWidget(QLabel("Video Asli"), 0, 0)
        video_layout.addWidget(self.video_label, 1, 0)
        video_layout.addWidget(QLabel("Video Hitam Putih"), 0, 1)
        video_layout.addWidget(self.video_bw_label, 1, 1)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        
        settings_layout = QFormLayout()
        settings_layout.addRow("Lower Hue", self.lh_slider)
        settings_layout.addRow("Lower Saturation", self.ls_slider)
        settings_layout.addRow("Lower Value", self.lv_slider)
        settings_layout.addRow("Upper Hue", self.uh_slider)
        settings_layout.addRow("Upper Saturation", self.us_slider)
        settings_layout.addRow("Upper Value", self.uv_slider)

        data_layout = QFormLayout()
        data_layout.addRow("X Coordinate :", self.x_label)
        data_layout.addRow("Y Coordinate :", self.y_label)
        data_layout.addRow("Distance       :", self.distance_label)

        main_layout = QGridLayout()
        main_layout.addLayout(video_layout, 0, 0, 1, 2)
        main_layout.addLayout(button_layout, 1, 0)
        main_layout.addLayout(settings_layout, 1, 1)
        main_layout.addLayout(data_layout, 2, 1)

        self.setLayout(main_layout)

        # Button actions
        self.start_button.clicked.connect(self.start_detection)
        self.stop_button.clicked.connect(self.stop_detection)

        # Slider actions
        self.lh_slider.valueChanged.connect(self.update_hsv_values)
        self.ls_slider.valueChanged.connect(self.update_hsv_values)
        self.lv_slider.valueChanged.connect(self.update_hsv_values)
        self.uh_slider.valueChanged.connect(self.update_hsv_values)
        self.us_slider.valueChanged.connect(self.update_hsv_values)
        self.uv_slider.valueChanged.connect(self.update_hsv_values)

        # Window settings
        self.setWindowTitle('Object Detection')
        self.setGeometry(100, 100, 900, 700)
        self.show()

    def create_slider(self, min_val, max_val, init_val):
        slider = QSlider(Qt.Horizontal, self)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(init_val)
        return slider

    def update_hsv_values(self):
        self.lh = self.lh_slider.value()
        self.ls = self.ls_slider.value()
        self.lv = self.lv_slider.value()
        self.uh = self.uh_slider.value()
        self.us = self.us_slider.value()
        self.uv = self.uv_slider.value()

    def start_detection(self):
        self.cap = cv2.VideoCapture(1)
        self.timer.start(20)

    def stop_detection(self):
        self.timer.stop()
        if self.cap is not None:
            self.cap.release()
        self.clear_video_labels()

    def clear_video_labels(self):
        # Create a blank image to clear the video labels
        blank_image = QImage(400, 300, QImage.Format_RGB888)
        blank_image.fill(Qt.black)
        self.video_label.setPixmap(QPixmap.fromImage(blank_image))
        self.video_bw_label.setPixmap(QPixmap.fromImage(blank_image))

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create mask
        lower_green = np.array([self.lh, self.ls, self.lv])
        upper_green = np.array([self.uh, self.us, self.uv])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Apply filters
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Contour detection
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        output = np.zeros_like(mask)

        for contour in contours:
            if cv2.contourArea(contour) < 1000:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center_x = x + w // 2
            center_y = y + h // 2
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            # Draw on black and white output
            cv2.drawContours(output, [contour], -1, (255), thickness=cv2.FILLED)

            # Update data labels with coordinates and size
            self.x_label.setText(f"X: {center_x}")
            self.y_label.setText(f"Y: {center_y}")
            self.distance_label.setText(f"Distance: {w * h}")

        # Convert frames to QImage
        color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        color_image = QImage(color_frame.data, color_frame.shape[1], color_frame.shape[0], QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(color_image))

        bw_image = QImage(output.data, output.shape[1], output.shape[0], QImage.Format_Grayscale8)
        self.video_bw_label.setPixmap(QPixmap.fromImage(bw_image))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ObjectDetectionApp()
    sys.exit(app.exec_())
