import cv2
import pandas as pd
import pytesseract as pt
from transformers import pipeline
import csv
import os

# Load once at the top
classifier = pipeline("text-classification", model="textattack/bert-base-uncased-CoLA") #for classifying extracted text
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #for extracting text
def vp(vs):
    with open("vtext.txt", mode='a') as f: #text file containing info from video
        cam = cv2.VideoCapture(f"{vs}.mp4")
        currentframe = 0

        # Read the first frame
        ret, prev_frame = cam.read()
        if not ret:
            print("Couldn't read first frame.")
            exit()
        height, width = prev_frame.shape[:2]
        x_start = int(width * 0.10)
        x_end = int(width * 0.90)
        y_start = int(height * 0.20)
        y_end = int(height * 0.93)
        prev_frame = prev_frame[y_start:y_end, x_start:x_end] #cropping the frame
        # Resize for consistency and speed (optional)
        # prev_frame = cv2.resize(prev_frame, (1300, 650))
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)      #preprocessing the frame
        prev_gray = cv2.GaussianBlur(prev_gray, (5, 5), 0)

        while True:
            ret, frame = cam.read()
            if not ret:
                break
            currentframe += 1

            if currentframe % 30 != 0: #skipping the same frames, needs adjustment based on different videos
                continue

            # frame = cv2.resize(frame, (1300, 650))  # resize to keep size consistent
            frame = frame[y_start:y_end, x_start:x_end]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)

            # Difference between previous and current grayscale frames
            diff = cv2.absdiff(prev_gray, gray)
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            non_zero_count = cv2.countNonZero(thresh)

            if non_zero_count > 6000:
                # Optional: Resize down slightly before OCR to speed up
                ocr_ready = cv2.resize(gray, (900, int(gray.shape[0] * 900 / gray.shape[1])))
                #cv2.imshow("pframe", ocr_ready)
                # Extract text
                text = pt.image_to_string(ocr_ready).strip()

                # Run sentence classifier
                result = classifier(text)[0]
                if result['label'] == 'LABEL_1':
                    f.write(text+"\n")
            prev_gray = gray

            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #break
    cam.release()
    cv2.destroyAllWindows()
    with open("vtext.txt", mode='r') as f:
        lines = [line.strip() for line in f if line.strip()]
    with open("vtext.csv", "w", newline="", encoding="utf-8") as csv_file: #for removing duplicate lines in text file
        writer = csv.writer(csv_file)
        for line in lines:
            writer.writerow([line])
    dataset=pd.read_csv("vtext.csv")
    dataset=dataset.drop_duplicates()
    dataset.to_csv("vtext.txt", index=False, header=False)
    os.remove("vtext.csv")
