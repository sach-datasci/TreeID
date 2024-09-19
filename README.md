# AI-Based Investigation of Illegal Tree Logging Using Tree Biometrics

## Project Overview

This project is an innovative AI-driven approach to combat illegal tree logging by leveraging advanced deep learning algorithms. It focuses on using tree biometrics to match images of tree stumps found at illegal logging sites with logs, helping authorities track and identify illegally harvested trees. The system provides high accuracy in determining whether a tree has been illegally cut by analyzing image data.

## Features
- **Tree Log Matching**: Matches images of tree stumps with tree logs to track illegal logging.
- **Video to Image Conversion**: Converts video data into individual frames to build a tree biometric database.
- **Illegal Logging Detection**: Upload images to assess the likelihood of a tree being previously logged illegally.

## Installation Instructions

### Prerequisites
To run this project, ensure you have Python installed on your system along with the following dependencies:

```bash
pip install -r requirements.txt
```

### Required Libraries
1. **One-shot learning algorithms**: For image matching and tree biometric analysis.
2. **Deep learning frameworks**: For training the models, e.g., TensorFlow or PyTorch.
3. **Image Processing Libraries**: OpenCV, Pillow, etc.

### Setting Up the Project

1. **Clone the repository**:
   ```bash
   git clone [repository URL]
   ```
   
2. **Navigate to the project directory**:
   ```bash
   cd tree-logging-ai
   ```

3. **Install the required dependencies**:
   Install all necessary libraries for deep learning, image processing, and one-shot learning by running:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment**:
   Ensure you have Python 3.8 or later installed and the appropriate deep learning libraries configured.

## Usage Instructions

The project offers two main functionalities:

1. **Adding Video to the Database**:
   - Users can upload a video of a tree cuted in forest area or anywhere.
   - The system will automatically convert the video into multiple images (frames) to build a tree biometric database for later matching.

   Example usage:
   ```bash
   python convert_video_to_frames.py --input video.mp4 --output ./database/
   ```

2. **Detecting Illegal Logging**:
   - Users can upload an image of a tree stump.
   - The system will then analyze the image and provide an accuracy score indicating the likelihood of the tree having been illegally logged.

   Example usage:
   ```bash
   python check_illegal_logging.py --input tree_stump_image.jpg
   ```

## Dependencies

- **Python 3.8+**
- **TensorFlow** or **PyTorch**
- **OpenCV** for image processing
- **Pillow** for image handling
- **Numpy**, **Pandas** for data handling
- **One-shot learning models**

To install these dependencies, ensure the `requirements.txt` file contains:
```bash
tensorflow
opencv-python
pillow
numpy
pandas
```

## Contributing

We welcome contributions! Please follow the standard Git workflow:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request with a detailed explanation of your changes.

## Contact Information

For inquiries or support, please contact:

- **Meet Guna**, Email: [guna.meet.r@gmail.com]
- **Sachinika Kankanam Pathirannahalage**, Email: [sachinika2.kankanampathirannahal@live.uwe.ac.uk]
- **Thanustiya Thejonayanan**, Email: [thanustiya2.thejonayanan@live.uwe.ac.uk]

---
