import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt

class PanoramaApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Panorama Stitcher")
        self.setGeometry(200, 200, 600, 400)

        self.image1 = None
        self.image2 = None
        self.stitched_image = None

        self.initUI()

    def initUI(self):
        # Labels for displaying images
        self.label_image1 = QLabel(self)
        self.label_image1.setAlignment(Qt.AlignCenter)
        self.label_image1.setFixedSize(280, 280)

        self.label_image2 = QLabel(self)
        self.label_image2.setAlignment(Qt.AlignCenter)
        self.label_image2.setFixedSize(280, 280)

        self.label_stitched = QLabel(self)
        self.label_stitched.setAlignment(Qt.AlignCenter)
        self.label_stitched.setFixedSize(560, 280)
        self.label_stitched.setStyleSheet("border: 1px solid black;")

        # Buttons for selecting images and stitching
        self.btn_image1 = QPushButton("Select Image 1", self)
        self.btn_image1.clicked.connect(self.select_image1)

        self.btn_image2 = QPushButton("Select Image 2", self)
        self.btn_image2.clicked.connect(self.select_image2)

        self.btn_stitch = QPushButton("Stitch Images", self)
        self.btn_stitch.clicked.connect(self.stitch_images)

        self.btn_visualize = QPushButton("Visualize Keypoints and stitch", self)
        self.btn_visualize.clicked.connect(self.visualize_keypoints)

        # Layout setup
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.btn_image1)
        layout_buttons.addWidget(self.btn_image2)
        layout_buttons.addWidget(self.btn_visualize)

        layout_stitch = QVBoxLayout()
        layout_stitch.addWidget(self.btn_stitch)
        layout_stitch.addWidget(self.label_stitched)

        layout_images = QHBoxLayout()
        layout_images.addWidget(self.label_image1)
        layout_images.addWidget(self.label_image2)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_buttons)
        layout_main.addLayout(layout_images)
        layout_main.addLayout(layout_stitch)

        central_widget = QWidget(self)
        central_widget.setLayout(layout_main)
        self.setCentralWidget(central_widget)

    def select_image1(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.image1 = cv2.imread(file_path)
            self.display_image(self.image1, self.label_image1)

    def select_image2(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.image2 = cv2.imread(file_path)
            self.display_image(self.image2, self.label_image2)

    def stitch_images(self):
        if self.image1 is None or self.image2 is None:
            QMessageBox.critical(self, "Error", "Please select both images!")
            return

        images = [self.image1, self.image2]
        stitcher = cv2.Stitcher.create()
        status, stitched = stitcher.stitch(images)

        if status == cv2.Stitcher_OK:
            self.stitched_image = stitched
            self.display_image(self.stitched_image, self.label_stitched)
        else:
            error_message = {
                cv2.Stitcher_ERR_NEED_MORE_IMGS: "Need more images",
                cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: "Homography estimation failed",
                cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: "Camera parameters adjustment failed"
            }.get(status, "Unknown error")
            QMessageBox.information(self, "Success", "Panorama generation successful.")
            
    def visualize_keypoints(self):
        if self.image1 is None or self.image2 is None:
            QMessageBox.critical(self, "Error", "Please select both images!")
            return

        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(self.image1, None)
        kp2, des2 = sift.detectAndCompute(self.image2, None)

        # Draw keypoints
        img1_kp = cv2.drawKeypoints(self.image1, kp1, None)
        img2_kp = cv2.drawKeypoints(self.image2, kp2, None)

        # Display keypoints
        self.display_image(img1_kp, self.label_image1)
        self.display_image(img2_kp, self.label_image2)

        # Match keypoints
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        matches = bf.match(des1, des2)

        # Sort matches by distance
        matches = sorted(matches, key=lambda x: x.distance)

        # Draw matches
        img_matches = cv2.drawMatches(self.image1, kp1, self.image2, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        # Display matches
        self.display_image(img_matches, self.label_stitched)

        QMessageBox.information(self, "Success", "Panorama generation successful.")

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
