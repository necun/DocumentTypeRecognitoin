import cv2

def is_handwritten(aspect_ratio, spacing_ratio, density_ratio, area_ratio):
    # Heuristic to determine if it is handwritten based on various features
    return 0.1 <= aspect_ratio <= 0.7 and spacing_ratio > 0.5 and density_ratio > 0.2 and area_ratio > 0.3

def calculate_spacing_ratio(stats, i, thresholded):
    # Calculate spacing ratio for a word
    x, y, w, h = stats[i][:4]
    word_image = thresholded[y:y + h, x:x + w]
    projection = cv2.reduce(word_image, 0, cv2.REDUCE_AVG).flatten()
    spacing_ratio = sum(projection == 255) / len(projection)
    return spacing_ratio

def calculate_density_ratio(stats, i, thresholded):
    # Calculate density ratio for a word
    x, y, w, h = stats[i][:4]
    word_image = thresholded[y:y + h, x:x + w]
    density_ratio = cv2.countNonZero(word_image) / (w * h)
    return density_ratio

image = cv2.imread(r"C:\Users\nitis.DESKTOP-GPCDIV9\OneDrive\Documents\WhatsApp Image 5.jpg")
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresholded = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
_, labels, stats, centroids = cv2.connectedComponentsWithStats(thresholded)

total_words = 0
handwritten_words = 0

for i in range(1, len(stats)):
    x, y, w, h = stats[i][:4]
    aspect_ratio = float(w) / h

    # Calculate spacing ratio
    spacing_ratio = calculate_spacing_ratio(stats, i, thresholded)

    # Calculate density ratio
    density_ratio = calculate_density_ratio(stats, i, thresholded)

    # Calculate contour area ratio
    area_ratio = stats[i][4] / (w * h)

    text_type = "Machine_written" if not is_handwritten(aspect_ratio, spacing_ratio, density_ratio, area_ratio) else "Hand_written"
    print(f"Word {i}: Aspect Ratio - {aspect_ratio:.2f}, Spacing Ratio - {spacing_ratio:.2f}, Density Ratio - {density_ratio:.2f}, Area Ratio - {area_ratio:.2f}, Text Type - {text_type}")

    total_words += 1
    if text_type == "Hand_written":
        handwritten_words += 1

# Output result based on features of individual words
output_result = 1 if handwritten_words > 0 else 0

print(f"\nNumber of Words: {total_words}")
print(f"Handwritten Words: {handwritten_words}")
print(f"Overall Output: {output_result}")

# Display the labeled image
cv2.imshow("Labeled Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()