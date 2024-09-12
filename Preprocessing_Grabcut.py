#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage import exposure
from skimage.feature import canny

class ImageSegmenter:
    def __init__(self, image, output_size=(300, 300), min_contour_area=1000):
        self.image = image
        self.output_size = output_size
        self.min_contour_area = min_contour_area
        self.segmented_image = None
        self.cropped_image = None
        self.resized_image = None

    def manual_mask_initialization(self, image):
        mask = np.zeros(image.shape[:2], np.uint8)
        fg_model = np.zeros((1, 65), np.float64)
        bg_model = np.zeros((1, 65), np.float64)

        mask[20:-20, 20:-20] = cv2.GC_PR_FGD
        
        mask[:10, :] = cv2.GC_BGD
        mask[-10:, :] = cv2.GC_BGD
        mask[:, :10] = cv2.GC_BGD
        mask[:, -10:] = cv2.GC_BGD

        return mask, bg_model, fg_model

    def grabcut_segmentation(self):
        mask, bg_model, fg_model = self.manual_mask_initialization(self.image)
        cv2.grabCut(self.image, mask, None, bg_model, fg_model, 5, cv2.GC_INIT_WITH_MASK)
        final_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1, 0).astype('uint8')
        self.segmented_image = self.image * final_mask[:, :, np.newaxis]

        kernel = np.ones((5, 5), np.uint8)
        self.segmented_image = cv2.morphologyEx(self.segmented_image, cv2.MORPH_OPEN, kernel, iterations=2)
        self.segmented_image = cv2.morphologyEx(self.segmented_image, cv2.MORPH_CLOSE, kernel, iterations=2)

        return self.segmented_image
    
    def filter_small_contours(self):
        gray = cv2.cvtColor(self.segmented_image, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        mask = np.zeros(gray.shape, np.uint8)
        for contour in contours:
            if cv2.contourArea(contour) > self.min_contour_area:
                cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

        self.segmented_image = cv2.bitwise_and(self.segmented_image, self.segmented_image, mask=mask)

        # Additional small contour filtering
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                cv2.drawContours(mask, [contour], -1, 0, thickness=cv2.FILLED)
        
        self.segmented_image = cv2.bitwise_and(self.segmented_image, self.segmented_image, mask=mask)

    def crop_and_resize(self):
        gray = cv2.cvtColor(self.segmented_image, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            self.cropped_image = self.segmented_image[y:y+h, x:x+w]
            self.resized_image = cv2.resize(self.cropped_image, self.output_size, interpolation=cv2.INTER_AREA)
        else:
            self.resized_image = cv2.resize(self.segmented_image, self.output_size, interpolation=cv2.INTER_AREA)
    
    def process_image(self):
        self.grabcut_segmentation()
        self.filter_small_contours()
        self.crop_and_resize()
        return self.segmented_image, self.cropped_image, self.resized_image

    def display_images(self):
        segmented_image, cropped_image, resized_image = self.process_image()
        plt.figure(figsize=(20, 8))

        plt.subplot(1, 4, 1)
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.title('Original Image')
        plt.axis('off')

        plt.subplot(1, 4, 2)
        plt.imshow(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))
        plt.title('Segmented Image')
        plt.axis('off')

        plt.subplot(1, 4, 3)
        plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        plt.title('Cropped Image')
        plt.axis('off')

        plt.subplot(1, 4, 4)
        plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
        plt.title('Resized Image')
        plt.axis('off')

        plt.show()

class ImagePipeline:
    def __init__(self, image):
        self.image = image
        self.preprocessed_image_color = None
        self.preprocessed_image_gray = None
        self.edges_color = None
        self.edges_gray = None
    
    def preprocess_image_color(self):
        self.preprocessed_image_color = cv2.GaussianBlur(self.image, (7, 7), 0)
        return self.preprocessed_image_color

    def preprocess_image_gray(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        equalized = exposure.equalize_hist(gray)
        self.preprocessed_image_gray = cv2.GaussianBlur((equalized * 255).astype(np.uint8), (7, 7), 0)
        return self.preprocessed_image_gray
    
    def save_preprocessed_images(self, save_path, file_name):
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        if self.preprocessed_image_gray is not None:
            # Save grayscale preprocessed image as high-quality JPEG
            cv2.imwrite(os.path.join(save_path, f'{file_name}_preprocessed_gray.jpg'), 
                        (self.preprocessed_image_gray * 255).astype(np.uint8),
                        [cv2.IMWRITE_JPEG_QUALITY, 100])


    def display_results_color(self):
        plt.figure(figsize=(15, 8))

        plt.subplot(1, 3, 1)
        plt.title('Original Image')
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.title('Preprocessed Image (Color)')
        plt.imshow(cv2.cvtColor(self.preprocessed_image_color, cv2.COLOR_BGR2RGB))
        plt.axis('off')


        plt.show()

    def display_results_grayscale(self):
        plt.figure(figsize=(15, 8))

        plt.subplot(1, 3, 1)
        plt.title('Original Image (Grayscale)')
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY), cmap='gray')
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.title('Preprocessed Image (Grayscale)')
        plt.imshow(self.preprocessed_image_gray, cmap='gray')
        plt.axis('off')

        plt.show()

# Main Processing Function for Folder
def process_images_in_folder(input_dir, output_dir, output_size=(300, 300), min_contour_area=1000):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(input_dir, file_name)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Failed to load image {file_name}. Skipping...")
                continue

            print(f"Processing image: {file_name}")

            # Segment the image
            segmenter = ImageSegmenter(image, output_size=output_size, min_contour_area=min_contour_area)
            segmented_image, cropped_image, resized_image = segmenter.process_image()

            if cropped_image is None:
                print(f"No valid contours found in {file_name}. Skipping...")
                continue

            # Process the segmented image with the pipeline
            pipeline = ImagePipeline(cropped_image)
            pipeline.preprocess_image_color()
            pipeline.preprocess_image_gray()
            pipeline.detect_edges_color()
            pipeline.detect_edges_gray()

            # Save the preprocessed images
            file_base_name = os.path.splitext(file_name)[0]
            pipeline.save_preprocessed_images(output_dir, file_base_name)

            # Optionally display results
            pipeline.display_results_color()
            pipeline.display_results_grayscale()

# Example Usage
input_dir = 'data/Cheddar_Wood_Ash_1'
output_dir = 'Preprocess/Gray/Cheddar_Wood_Ash_11'

process_images_in_folder(input_dir, output_dir, output_size=(300, 300), min_contour_area=5000)


# In[ ]:




