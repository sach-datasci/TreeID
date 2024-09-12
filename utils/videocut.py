import cv2
import os

# Set environment variable to disable GStreamer
os.environ["OPENCV_VIDEOIO_PRIORITY_GSTREAMER"] = "0"


def extract_images(video_path, output_folder, interval=1, max_images=30, file_name='a'):
    # Create the output folder if it does not exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    # Determine the interval in frames
    frame_interval = fps * interval
    
    # Calculate the number of frames to skip to get the required number of images
    frame_skip = max(1, total_frames // max_images)
    
    # Extract images
    frame_count = 0
    image_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Check if the current frame is at the required interval
        if frame_count % min(frame_interval, frame_skip) == 0:
            image_path = os.path.join(output_folder, f"{file_name}_{image_count:04d}.jpg")
            cv2.imwrite(image_path, frame)
            image_count += 1
            
            if image_count >= max_images:
                break
        
        frame_count += 1
    
    cap.release()

def process_videos_in_folder(input_folder, output_base_folder, interval=1, max_images=30):
    # Create the output base folder if it does not exist
    os.makedirs(output_base_folder, exist_ok=True)
    
    # List all video files in the input folder
    video_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    for video_file in video_files:
        video_path = os.path.join(input_folder, video_file)
        video_name, _ = os.path.splitext(video_file)
        output_folder = os.path.join(output_base_folder, video_name)
        
        extract_images(video_path, output_base_folder, interval, max_images,video_name)

folder_path = os.path.join('Tree Data','Data')
folder = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

print(folder)

for f in folder:
    input_folder = os.path.join(folder_path,f)
    output_base_folder =os.path.join(folder_path,'IMG_data',f)
    print(f,'All IMG extracted')
    # process_videos_in_folder(input_folder, output_base_folder)
