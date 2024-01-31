import cv2
import numpy as np

def is_handwritten_contour(contour):
    # You can define heuristics or features to determine if a contour represents handwritten text
    # Here, we're checking the contour area, aspect ratio, and height-to-width ratio
    x, y, w, h = cv2.boundingRect(contour)
    contour_area = cv2.contourArea(contour)
    aspect_ratio = float(w) / h
    height_width_ratio = float(h) / w

    # Adjust these thresholds based on the characteristics of your handwritten text
    if contour_area > 100 and 0.2 <= aspect_ratio <= 10.0 and height_width_ratio > 1.0:
        return True

    return False

def is_machine_written_contour(contour):
    # Define criteria to identify machine-written text
    # You may need to adjust these thresholds based on the characteristics of your machine-written text
    x, y, w, h = cv2.boundingRect(contour)
    contour_area = cv2.contourArea(contour)
    aspect_ratio = float(w) / h
    height_width_ratio = float(h) / w

    # Adjust these thresholds based on the characteristics of your machine-written text
    if contour_area > 50 and 0.1 <= aspect_ratio <= 10.0 and 0.1 <= height_width_ratio <= 10.0:
        return False

    return True

image = cv2.imread(r"C:\Users\nitis.DESKTOP-GPCDIV9\OneDrive\Documents\WhatsApp Image 5.jpg")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred_image = cv2.medianBlur(gray_image, 5)  # Apply median blur for noise reduction
_, thresholded = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

total_words = 0
handwritten_words = 0

for i, contour in enumerate(contours):
    if is_handwritten_contour(contour):
        x, y, w, h = cv2.boundingRect(contour)
        word_image = thresholded[y:y + h, x:x + w]

        text_type = "Hand_written"
        label_text = f"Type: {text_type}"
        cv2.putText(image, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print(f"Word {i + 1}: Text Type - {text_type}")

        total_words += 1
        handwritten_words += 1
    elif is_machine_written_contour(contour):
        # If it doesn't meet handwritten criteria, consider it as machine-written
        x, y, w, h = cv2.boundingRect(contour)
        text_type = "Machine_written"
        label_text = f"Type: {text_type}"
        cv2.putText(image, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print(f"Word {i + 1}: Text Type - {text_type}")
        total_words += 1

# Overall output based on the majority of words
output_result = 1 if handwritten_words > total_words / 2 else 0

print(f"Number of Words: {total_words}")
print(f"Handwritten Words: {handwritten_words}")
print(f"Overall Output: {output_result}")

# Display the labeled image
cv2.imshow("Labeled Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()