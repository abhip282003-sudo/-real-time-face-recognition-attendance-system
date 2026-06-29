import os
import cv2
import pickle
import numpy as np
from skimage.feature import hog
from sklearn.svm import SVC
from config import DATASET_PATH, MODEL_PATH, LABEL_PATH
# Lists to store features and labels
faces = []
labels = []
label_map = {}
# Load Haar Cascade Face Detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)
current_id = 0
# HOG Feature Extraction Function
def extract_hog_features(image):
    features = hog(
        image,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm="L2-Hys",
        visualize=False,
        feature_vector=True
    )
    return features
# Read Dataset
for person in sorted(os.listdir(DATASET_PATH)):
    person_folder = os.path.join(DATASET_PATH, person)
    if not os.path.isdir(person_folder):
        continue
    label_map[person] = current_id
    print(f"Processing {person}...")
    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)
        img = cv2.imread(image_path)
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected_faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(80, 80)
        )
        if len(detected_faces) == 0:
            continue
        for (x, y, w, h) in detected_faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (128, 128))
            features = extract_hog_features(face)
            faces.append(features)
            labels.append(current_id)

    current_id += 1
# Convert to NumPy Array
faces = np.array(faces)
labels = np.array(labels)

print("\nTotal Faces:", len(faces))
print("Total Persons:", len(label_map))
# Train SVM
print("\nTraining Model...")

model = SVC(
    kernel="linear",
    probability=True
)
model.fit(faces, labels)
# Save Model
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)
with open(LABEL_PATH, "wb") as f:
    pickle.dump(label_map, f)
# Training Complete
print("\n===================================")
print("Training Completed Successfully")
print("===================================")

print("\nRegistered Persons:")

for name, label in label_map.items():
    print(f"{label} --> {name}")

print("\nModel Saved Successfully!")




# import cv2
# import os
# import pickle
# import numpy as np
# from config import DATASET_PATH
# from config import MODEL_PATH
# from config import LABEL_PATH
# faces = []
# labels = []
# label_map = {}
# face_detector = cv2.CascadeClassifier(
#     cv2.data.haarcascades +
#     "haarcascade_frontalface_default.xml"
# )
# current_id = 0
# for person in sorted(os.listdir(DATASET_PATH)):
#     person_folder = os.path.join(DATASET_PATH, person)
#     if not os.path.isdir(person_folder):
#         continue
#     label_map[person] = current_id
#     for image_name in os.listdir(person_folder):
#         image_path = os.path.join(person_folder, image_name)
#         img = cv2.imread(image_path)
#         if img is None:
#             continue
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         detected_faces = face_detector.detectMultiScale(
#             gray,
#             1.3,
#             5
#         )
#         for (x, y, w, h) in detected_faces:
#             face = gray[y:y+h, x:x+w]
#             face = cv2.resize(face, (200, 200))
#             faces.append(face)
#             labels.append(current_id)
#     current_id += 1
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.train(
#     faces,
#     np.array(labels)
# )
# recognizer.save(MODEL_PATH)
# with open(LABEL_PATH, "wb") as f:
#     pickle.dump(label_map, f)
# print("\nTraining Completed Successfully")
# print("\nRegistered Persons")
# for k, v in label_map.items():
#     print(v, "->", k)