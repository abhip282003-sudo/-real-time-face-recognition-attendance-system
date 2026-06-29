import cv2
import pickle
import numpy as np
from skimage.feature import hog
from config import MODEL_PATH, LABEL_PATH
from attendence import mark_attendance   # NEW

# Load Trained Model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(LABEL_PATH, "rb") as f:
    label_map = pickle.load(f)

names = {v: k for k, v in label_map.items()}

# Face Detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# HOG Feature Extraction
def extract_hog_features(image):
    features = hog(
        image,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        block_norm="L2-Hys",
        feature_vector=True
    )
    return features

# Confidence Threshold
THRESHOLD = 0.85

# Start Webcam
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        # Crop Face
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (128, 128))

        # Extract HOG Features
        features = extract_hog_features(face)
        features = np.array(features).reshape(1, -1)

        # Predict
        predicted_label = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]

        confidence = np.max(probabilities)

        # Known Person
        if confidence >= THRESHOLD:

            name = names[predicted_label]
            color = (0, 255, 0)

            # Save Attendance
            mark_attendance(name)

        # Unknown Person
        else:
            name = "Unknown"
            color = (0, 0, 255)

        # Draw Rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            color,
            2
        )

        # Show Name + Confidence
        cv2.putText(
            frame,
            f"{name} ({confidence*100:.2f}%)",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    cv2.imshow("Face Recognition Attendance System", frame)

    key = cv2.waitKey(1)

    if key == 27:      # ESC Key
        break

cap.release()
cv2.destroyAllWindows()



# import cv2
# import pickle
# import numpy as np
# from skimage.feature import hog
# from config import MODEL_PATH, LABEL_PATH
# # Load Trained Model
# with open(MODEL_PATH, "rb") as f:
#     model = pickle.load(f)
# with open(LABEL_PATH, "rb") as f:
#     label_map = pickle.load(f)
# names = {v: k for k, v in label_map.items()}
# # Face Detector
# face_detector = cv2.CascadeClassifier(
#     cv2.data.haarcascades +
#     "haarcascade_frontalface_default.xml"
# )
# # HOG Feature Extraction
# def extract_hog_features(image):
#     features = hog(
#         image,
#         orientations=9,
#         pixels_per_cell=(8, 8),
#         cells_per_block=(2, 2),
#         block_norm="L2-Hys",
#         feature_vector=True
#     )
#     return features
# # Confidence Threshold
# THRESHOLD = 0.85
# # Start Webcam
# cap = cv2.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_detector.detectMultiScale(
#         gray,
#         scaleFactor=1.3,
#         minNeighbors=5,
#         minSize=(100, 100)
#     )
#     for (x, y, w, h) in faces:
#         # Crop face
#         face = gray[y:y+h, x:x+w]
#         face = cv2.resize(face, (128, 128))
#         # Extract HOG Features
#         features = extract_hog_features(face)
#         features = np.array(features).reshape(1, -1)
#         # Predict Person
#         predicted_label = model.predict(features)[0]
#         probabilities = model.predict_proba(features)[0]
#         confidence = np.max(probabilities)
#         # Unknown Detection
#         if confidence >= THRESHOLD:
#             name = names[predicted_label]
#             color = (0, 255, 0)  
#         else:
#             name = "Unknown"
#             color = (0, 0, 255)     
#         # Draw Rectangle
#         cv2.rectangle(
#             frame,
#             (x, y),
#             (x+w, y+h),
#             color,
#             2
#         )
#         # Display Name + Confidence
#         cv2.putText(
#             frame,
#             f"{name} ({confidence*100:.1f}%)",
#             (x, y-10),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.8,
#             color,
#             2
#         )
#     cv2.imshow("Face Recognition using HOG + SVM", frame)
#     key = cv2.waitKey(1)
#     if key == 27:   # ESC
#         break
# cap.release()
# cv2.destroyAllWindows()























# import cv2
# import pickle
# from config import MODEL_PATH
# from config import LABEL_PATH
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.read(MODEL_PATH)
# with open(LABEL_PATH, "rb") as f:
#     label_map = pickle.load(f)
# names = {v: k for k, v in label_map.items()}
# face_detector = cv2.CascadeClassifier(
#     cv2.data.haarcascades +
#     "haarcascade_frontalface_default.xml"
# )
# cap = cv2.VideoCapture(0)
# THRESHOLD = 55
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
#     gray = cv2.cvtColor(
#         frame,
#         cv2.COLOR_BGR2GRAY
#     )
#     faces = face_detector.detectMultiScale(
#         gray,
#         1.3,
#         5
#     )
#     for (x, y, w, h) in faces:
#         face = gray[y:y+h, x:x+w]
#         face = cv2.resize(face, (200, 200))
#         label, confidence = recognizer.predict(face)
#         if confidence < THRESHOLD and label in names:
#             name = names[label]
#         else:
#             name = "Unknown"
#         cv2.rectangle(
#             frame,
#             (x, y),
#             (x+w, y+h),
#             (0, 255, 0),
#             2
#         )
#         cv2.putText(
#             frame,
#             f"{name} ({confidence:.2f})",
#             (x, y-10),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.8,
#             (0, 255, 0),
#             2
#         )
#     cv2.imshow(
#         "Face Recognition",
#         frame
#     )
#     if cv2.waitKey(1) == 27:
#         break
# cap.release()
# cv2.destroyAllWindows()