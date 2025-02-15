import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class PanoramaApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Panorama Stitcher")
        self.setGeometry(200, 200, 800, 500)

        self.images = []
        self.stitched_image = None

        self.initUI()

    def initUI(self):
        # Labels for displaying images
        self.labels = [QLabel(self) for _ in range(3)]
        for label in self.labels:
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(250, 250)

        self.label_stitched = QLabel(self)
        self.label_stitched.setAlignment(Qt.AlignCenter)
        self.label_stitched.setFixedSize(750, 250)
        self.label_stitched.setStyleSheet("border: 1px solid black;")

        # Buttons for selecting images and stitching
        self.buttons = [QPushButton(f"Select Image {i+1}", self) for i in range(3)]
        for i, button in enumerate(self.buttons):
            button.clicked.connect(lambda _, idx=i: self.select_image(idx))

        self.btn_visualize_stitch = QPushButton("Visualize & Stitch", self)
        self.btn_visualize_stitch.clicked.connect(self.visualize_and_stitch)

        # Layout setup
        layout_buttons = QHBoxLayout()
        for button in self.buttons:
            layout_buttons.addWidget(button)
        layout_buttons.addWidget(self.btn_visualize_stitch)

        layout_images = QHBoxLayout()
        for label in self.labels:
            layout_images.addWidget(label)

        layout_stitch = QVBoxLayout()
        layout_stitch.addWidget(self.label_stitched)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_buttons)
        layout_main.addLayout(layout_images)
        layout_main.addLayout(layout_stitch)

        central_widget = QWidget(self)
        central_widget.setLayout(layout_main)
        self.setCentralWidget(central_widget)

    def select_image(self, index):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            image = cv2.imread(file_path)
            if len(self.images) > index:
                self.images[index] = image
            else:
                self.images.append(image)
            self.display_image(image, self.labels[index])

    def visualize_and_stitch(self):
        if len(self.images) < 3:
            QMessageBox.critical(self, "Error", "Please select all three images!")
            return

        orb = cv2.ORB_create()
        keypoint_images = []
        for img in self.images:
            keypoints, _ = orb.detectAndCompute(img, None)
            keypoint_images.append(cv2.drawKeypoints(img, keypoints, None))

        for img, label in zip(keypoint_images, self.labels):
            self.display_image(img, label)

        stitcher = cv2.Stitcher.create()
        status, stitched = stitcher.stitch(self.images)

        if status == cv2.Stitcher_OK:
            self.stitched_image = stitched
            self.display_image(self.stitched_image, self.label_stitched)
        else:
            QMessageBox.critical(self, "Error", f"Panorama stitching failed! Error Code: {status}")

    def display_image(self, image, label):
        if image is None:
            return
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image_rgb.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))

def main():
    app = QApplication(sys.argv)
    window = PanoramaApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
