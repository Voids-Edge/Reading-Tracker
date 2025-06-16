import os
import sys

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

def main():
    # User specifies the folder or uses a default
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = input("Enter the path to the folder containing your PDF books: ").strip()
    pdf_files = find_pdf_files(folder_path)
    if not pdf_files:
        print("No PDF files found. Exiting.")
        return
    selected_pdf = select_pdf_file(pdf_files)
    if selected_pdf:
        print(f"\nYou selected: {selected_pdf}")

if __name__ == "__main__":
    main()