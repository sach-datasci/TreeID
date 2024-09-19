import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from PIL import ImageTk, Image

# Load the pre-trained MobileNetV2 model
model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

class VideoToDatasetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Dataset and Image Comparison")
        self.root.geometry("800x600")

        # Frame for Video Upload and Frame Extraction
        self.video_frame = tk.LabelFrame(root, text="Video Upload & Frame Extraction", padx=10, pady=10)
        self.video_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        self.upload_video_button = tk.Button(self.video_frame, text="Upload Video", command=self.upload_video)
        self.upload_video_button.pack(pady=10)

        self.video_status_label = tk.Label(self.video_frame, text="No video uploaded yet.", fg="red")
        self.video_status_label.pack()

        # Frame for Image Upload and Comparison
        self.image_frame = tk.LabelFrame(root, text="Image Upload & Comparison", padx=10, pady=10)
        self.image_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        self.upload_img_button = tk.Button(self.image_frame, text="Upload Image", command=self.upload_image)
        self.upload_img_button.pack(pady=10)

        self.result_label = tk.Label(self.image_frame, text="No image uploaded yet.", fg="red")
        self.result_label.pack()

    def upload_video(self):
        video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
        if video_path:
            self.extract_frames(video_path)

    def extract_frames(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_interval = frame_count // 10

        dataset_dir = "dataset"
        os.makedirs(dataset_dir, exist_ok=True)

        for i in range(10):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i * frame_interval)
            ret, frame = cap.read()
            if ret:
                frame_path = os.path.join(dataset_dir, f"frame_{i}.jpg")
                cv2.imwrite(frame_path, frame)
                self.extract_features(frame_path)

        cap.release()
        self.video_status_label.config(text="Video uploaded and 10 frames extracted.", fg="green")
    
    def extract_features(self, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        features = model.predict(img_array)[0]
        feature_path = img_path.replace(".jpg", ".npy")
        np.save(feature_path, features)

    def upload_image(self):
        img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
        if img_path:
            self.compare_with_dataset(img_path)

    def compare_with_dataset(self, img_path):
        uploaded_features = self.extract_image_features(img_path)
        
        dataset_dir = "dataset"
        similarities = []

        for file_name in os.listdir(dataset_dir):
            if file_name.endswith(".npy"):
                dataset_features = np.load(os.path.join(dataset_dir, file_name))
                similarity = cosine_similarity([uploaded_features], [dataset_features])[0][0]
                similarities.append((file_name.replace(".npy", ".jpg"), similarity))
        
        best_match = max(similarities, key=lambda x: x[1])
        result_text = f"Best match: {best_match[0]} with similarity: {best_match[1]*100:.2f}%"
        
        self.result_label.config(text=result_text, fg="green")

    def extract_image_features(self, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        features = model.predict(img_array)[0]
        return features

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToDatasetApp(root)
    root.mainloop()

    # video_path = filedialog.askopenfilename()
