import fitz  # PyMuPDF
def is_handwritten_text(text):
    #Heuristic to determine if the text is handwritten based on certain features
    #You may need to adjust these conditions based on your observations
    return len(text) < 50  # If the text is short, it's more likely to be handwritten
def analyze_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    handwritten_detected_all_pages = False
    machine_written_detected_all_pages = False
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        # Extract text from the page
        text = page.get_text()
        # Analyze the extracted text
        if is_handwritten_text(text):
            print(f"Page {page_number + 1}: Handwritten Text Detected")
            handwritten_detected_all_pages = True
        else:
            print(f"Page {page_number + 1}: Machine-written Text Detected")
            machine_written_detected_all_pages = True
    pdf_document.close()
    # Overall output based on the presence of handwritten or machine-written text
    output_result = 1 if handwritten_detected_all_pages else 0
    print(f"Overall Output: {output_result}")
if __name__ == "_main_":
    pdf_path = r"C:\Users\nitis.DESKTOP-GPCDIV9\Favorites\Downloads\Student Manual_Writing.pdf" # Provide the path to your PDF file
    analyze_pdf(pdf_path)