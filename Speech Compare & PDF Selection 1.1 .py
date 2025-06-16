import os
import sys
import pdfplumber
import speech_recognition as sr
import difflib
import string

def find_pdf_files(folder_path):
    pdf_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def select_pdf_file(pdf_files):
    if not pdf_files:
        print("No PDF files found in the specified folder.")
        return None
    print("\nAvailable PDF files:")
    for idx, file in enumerate(pdf_files):
        print(f"{idx + 1}: {os.path.basename(file)}")
    while True:
        try:
            choice = int(input("Select a PDF number (or 0 to exit): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(pdf_files):
                return pdf_files[choice - 1]
            else:
                print("Invalid number. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def extract_page_text(pdf_path, page_number):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if page_number < 0 or page_number >= len(pdf.pages):
                print(f"Invalid page number. PDF has {len(pdf.pages)} pages.")
                return ""
            page = pdf.pages[page_number]
            text = page.extract_text()
            if text is None:
                print("No text found on that page.")
                return ""
            return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def normalize_text(text):
    # Lowercase and remove punctuation
    return ''.join([c.lower() for c in text if c not in string.punctuation])

def get_speech_input(prompt="Please say something..."):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print(prompt)
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
        return ""
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        return ""

def calculate_similarity(text1, text2):
    # Tokenize into words and compare sequences
    words1 = normalize_text(text1).split()
    words2 = normalize_text(text2).split()
    matcher = difflib.SequenceMatcher(None, words1, words2)
    return matcher.ratio() * 100  # As a percentage

def main():
    # Step 1: Use a fixed folder path instead of input
    folder_path = r"C:\Users\jmwre\OneDrive\Desktop\PDF's for App"
    pdf_files = find_pdf_files(folder_path)
    if not pdf_files:
        print("No PDF files found. Exiting.")
        return

    # Step 2: User selects PDF
    selected_pdf = select_pdf_file(pdf_files)
    if not selected_pdf:
        print("No PDF selected. Exiting.")
        return
    print(f"\nYou selected: {selected_pdf}")

    # Step 3: User selects page
    try:
        with pdfplumber.open(selected_pdf) as pdf:
            num_pages = len(pdf.pages)
        print(f"This PDF has {num_pages} pages.")
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return

    while True:
        try:
            page_num = int(input(f"Enter page number to extract as reference (1 - {num_pages}): "))
            if 1 <= page_num <= num_pages:
                break
            else:
                print("Page number out of range.")
        except ValueError:
            print("Please enter a valid number.")

    reference_text = extract_page_text(selected_pdf, page_num - 1)
    if not reference_text.strip():
        print("No reference text found on that page. Exiting.")
        return

    # Step 4: Speech recognition and similarity check
    print("\nSpeak into your microphone to test.")
    spoken_text = get_speech_input()
    print("\nYou said:")
    print(spoken_text)
    similarity = calculate_similarity(spoken_text, reference_text)
    print(f"\nMatch Percentage: {similarity:.2f}%")

if __name__ == "__main__":
    main()