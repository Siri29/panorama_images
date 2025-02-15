This project provides a GUI-based application for stitching images into a panorama using OpenCV and PyQt5. It includes two versions:

2-Image Panorama Stitcher: Allows users to select two images, visualize keypoints, and stitch them into a panorama.

3-Image Panorama Stitcher: Extends the functionality to handle three images for more complex panoramas.

Features:

Select images from your file system.

Visualize keypoints using ORB (for better compatibility) before stitching.

Stitch images seamlessly into a panorama using OpenCV’s stitching module.

Display stitched output directly in the GUI.

Installation:

Ensure you have Python installed, then install the required dependencies:

pip install opencv-python opencv-contrib-python PyQt5

Running the Applications

2-Image Stitcher

Run the following command:

python test.py


3-Image Stitcher

Run the following command:

python test2.py

Usage

Click the buttons to select images.

Click "Visualize & Stitch" to see keypoints and get the stitched output.

If successful, the panorama will be displayed; otherwise, an error message will appear.


Troubleshooting:

If the stitching fails, ensure images have enough overlapping regions.

Ensure OpenCV and PyQt5 are correctly installed.

Try using well-aligned images with similar lighting conditions.

License

This project is open-source.

Author

Developed by Siri29

