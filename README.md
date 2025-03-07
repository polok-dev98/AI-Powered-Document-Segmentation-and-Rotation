# **SmartDocFix** – Intelligent Document Segmentation & Rotation Correction  

This project is designed to segment documents from images using the **YOLOv11 segmentation model** and correct their orientation if they are rotated, similar to **CamScanner**. The model is trained on various types of documents and integrated into a **Flask** web application for easy usage.  

## 🚀 Features  
- 📄 **Document Segmentation**: Detects and extracts documents from images using a trained YOLOv11 segmentation model.  
- 🔄 **Orientation Correction**: Automatically corrects rotated documents to align them properly.  
- 🌐 **Flask API**: Provides a simple web interface for uploading images and obtaining processed results.  
- 🐳 **Docker Support**: Easily deployable using Docker.  

## 📂 Project Structure  
```
📂 project-root
│-- modules
│   │-- segmentation.py  # YOLOv11-based document segmentation
│   │-- rotation.py      # Corrects document rotation
│-- output               # Stores final processed images
│-- processed_images     # Stores intermediate segmented images
│-- templates            # Flask HTML templates
│-- uploads              # Stores uploaded images
│-- app.py               # Flask application
│-- Dockerfile           # Docker configuration
│-- model.pt             # Pretrained YOLOv11 segmentation model (request for access)
│-- requirements.txt     # Required dependencies
```

## ⚙️ Installation  

### Prerequisites  
Ensure you have **Python 3.10+** and **Docker** installed.  

### 🔧 Local Setup  
1. Clone the repository:  
   ```sh
   git clone https://github.com/polok-dev98/AI-Powered-Document-Segmentation-and-Rotation
   cd AI-Powered-Document-Segmentation-and-Rotation
   ```

2. Create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```sh
   python app.py
   ```

4. Access the web interface at: [http://localhost:5001](http://localhost:5001)


### 📸 Output
<div align="center">
  <img src="https://github.com/user-attachments/assets/bb9866b5-8134-49b1-80fd-965df3bd248b" width="70%" style="padding:20px; margin:10px;">
  <img src="https://github.com/user-attachments/assets/83772468-e35d-4042-9d3a-92836395e8ba" width="70%" style="padding:20px; margin:10px;">
  <img src="https://github.com/user-attachments/assets/8fb426f8-9d2c-4d81-81cf-171e29b66495" width="70%" style="padding:20px; margin:10px;">
  <img src="https://github.com/user-attachments/assets/fd5f3946-1daa-4dd0-ab49-9e8a66eec35b" width="70%" style="padding:20px; margin:10px;">
  <img src="https://github.com/user-attachments/assets/ccbd0138-4548-4567-974f-330ff534557f" width="70%" style="padding:20px; margin:10px;">
  <img src="https://github.com/user-attachments/assets/601681f7-1a03-454f-9c9e-3830aa07d32d" width="70%" style="padding:20px; margin:10px;">
</div>


### 🐳 Docker Setup  
1. Build the Docker image:
   ```sh
   docker build -t doc-segmentation .
   ```

2. Run the container:
   ```sh
   docker run -p 5001:5001 doc-segmentation
   ```

## 📡 API Usage  

### Upload and Process an Image  

- **Endpoint:** `POST /process_image`

#### Request:
- Form-data with a file input named `file`

#### Response:
```json
{
  "uploaded_image": "data:image/jpeg;base64,...",
  "final_image": "data:image/jpeg;base64,..."
}
```

## 🛠️ Technologies Used  
- **YOLOv11**: For document segmentation  
- **OpenCV**: For image processing  
- **Flask**: Backend web framework  
- **Docker**: Containerization for easy deployment  

## 🔮 Future Improvements  
- Improve segmentation accuracy with additional training data.  
- Implement real-time document processing using FastAPI.  
- Add a front-end interface for better usability.  

## 📜 License  
This project is licensed under the **MIT License**.  

## ✨ Author  
👨‍💻 **Asif Pervez Polok**  
🔗 **LinkedIn**: [polok98](https://www.linkedin.com/in/polok98/)  

