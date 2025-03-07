from flask import Flask, request, jsonify, render_template
import os
import base64
import cv2
import numpy as np
from modules.segmentation import roiSegmentation_with_class
from modules.rotation import correct_angle_vertical

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
FINAL_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FINAL_FOLDER, exist_ok=True)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode()}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process_image", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if not file:
        return jsonify({"error": "No file provided"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, "uploaded_image.jpg")
    file.save(file_path)
    
    _, _, cropped_img = roiSegmentation_with_class(file_path)
    if cropped_img is None:
        return jsonify({"error": "Image processing failed"}), 500
    
    final_image = correct_angle_vertical(cropped_img)
    final_path = os.path.join(FINAL_FOLDER, "final_image.jpg")
    cv2.imwrite(final_path, final_image)
    
    return jsonify({
        "uploaded_image": encode_image_to_base64(file_path),
        "final_image": encode_image_to_base64(final_path)
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
