# Image to Text Converter using Tesseract OCR

## Overview

This project provides a user-friendly GUI application for extracting text from images using Tesseract OCR. The application supports multiple languages, image preprocessing options (brightness, contrast, thresholding), and features to save or copy the extracted text.

## Features

- **Multi-Language Support**: Recognizes text in multiple languages (English, Spanish, French, German, Hindi).
- **Image Preprocessing**: Adjust brightness, contrast, and thresholding to improve OCR accuracy.
- **Interactive GUI**: A tabbed interface to handle multiple images simultaneously.
- **Save & Export**: Save the extracted text to a file (e.g., `.txt`, `.docx`).
- **Clipboard Copy**: Copy the extracted text to the clipboard with a single click.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/puckuz5/Tesseract-OCR-.git
    cd Tesseract-OCR-
    ```

2. **Install Dependencies**:
    Ensure you have Python installed (version 3.6 or above). Then install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```
    `requirements.txt` should include:
    - `opencv-python`
    - `pytesseract`
    - `Pillow`
    - `langdetect`
    - `pyperclip`
    - `tkinter` (Usually comes pre-installed with Python)

3. **Tesseract Installation**:
    - Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).
    - Set the path to the Tesseract executable in the code:
      ```python
      pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
      ```
      Adjust the path as per your installation.

## Usage

1. **Run the Application**:
    ```bash
    python image.py
    ```

2. **Upload Images**:
    - Click on "Upload Images" to select one or more images from your file system.
    
3. **Adjust Image Settings**:
    - Use the sliders to adjust brightness, contrast, and thresholding as needed.
    - The processed image preview is displayed in real-time.

4. **Select Language**:
    - Choose the language of the text in the image from the dropdown menu.

5. **Extract Text**:
    - The extracted text will be displayed in a new tab for each image.

6. **Save or Copy Text**:
    - Save the extracted text to a file or copy it to the clipboard using the buttons provided.

## Troubleshooting

- **Empty Page Error**: Ensure the image has clear, visible text and adjust the preprocessing settings (brightness, contrast, thresholding) for better accuracy.
- **Permission Denied**: Ensure the file path and permissions are correct. Run the application as an administrator if needed.
- **Incorrect Language Detection**: Fine-tune the preprocessing settings or provide more varied training data for Tesseract.

## Contribution

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for deta


