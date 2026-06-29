import cv2
import os
from config import DATASET_PATH
# Enter person's name
name = input("Enter Person Name: ").strip()
# Create person's folder
person_path = os.path.join(DATASET_PATH, name)
os.makedirs(person_path, exist_ok=True)
# Open webcam
cap = cv2.VideoCapture(0)
# Continue numbering if images already exist
count = len(os.listdir(person_path))
# Total images to capture
TOTAL_IMAGES = 40
print(f"Capturing {TOTAL_IMAGES} images...")
while count < TOTAL_IMAGES:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not access webcam.")
        break
    # Show webcam
    cv2.imshow("Face Capture", frame)
    # Save image
    image_path = os.path.join(person_path, f"{count}.jpg")
    cv2.imwrite(image_path, frame)
    print(f"Image {count + 1} Saved")
    count += 1
    # Wait 200 milliseconds before next image
    cv2.waitKey(200)
# Release webcam
cap.release()
cv2.destroyAllWindows()
print(f"\n{TOTAL_IMAGES} Images Captured Successfully!")