import cv2
import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, Text
from tkinter import ttk, Scale, HORIZONTAL
from langdetect import detect, DetectorFactory
import pyperclip

# Configure the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path if needed

DetectorFactory.seed = 0  # To ensure consistency

def preprocess_image(image_path, brightness=1.0, contrast=1.0, threshold=127):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Adjust brightness and contrast
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast, beta=int(100 * (brightness - 1)))

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, processed_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

    return processed_image

def detect_language(text):
    try:
        language_code = detect(text)
    except:
        language_code = "und"  # Undefined if detection fails
    return language_code

def extract_text_from_image(image_path, language, brightness, contrast, threshold):
    processed_image = preprocess_image(image_path, brightness, contrast, threshold)
    pil_image = Image.fromarray(processed_image)
    custom_config = f'--psm 6 --oem 1 -l {language}'
    text = pytesseract.image_to_string(pil_image, config=custom_config)

    detected_language = detect_language(text)
    return text, detected_language

def open_file_dialog(language, brightness, contrast, threshold):
    languages = {"English": "eng", "Spanish": "spa", "French": "fra", "German": "deu", "Hindi": "hin"}
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if file_paths:
        for file_path in file_paths:
            # Show a real-time preview of the preprocessing effects
            preview_image(file_path, brightness, contrast, threshold)
            extracted_text, detected_language = extract_text_from_image(file_path, languages[language], brightness, contrast, threshold)

            # Create a new tab for each image
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=file_path.split("/")[-1])

            # Create a text area in the new tab to display the extracted text
            text_area = Text(tab, wrap=tk.WORD, height=20, padx=10, pady=10)
            text_area.insert(tk.END, f"Detected Language: {detected_language}\n\n{extracted_text}")
            text_area.pack(expand=True, fill='both')

def preview_image(image_path, brightness, contrast, threshold):
    processed_image = preprocess_image(image_path, brightness, contrast, threshold)
    pil_image = Image.fromarray(processed_image)
    pil_image = pil_image.resize((400, 300), Image.ANTIALIAS)  # Resize for the preview area
    img = ImageTk.PhotoImage(pil_image)

    # Display the image in the GUI
    if 'image_label' not in globals():
        global image_label
        image_label = tk.Label(window, image=img)
        image_label.image = img
        image_label.pack()
    else:
        image_label.configure(image=img)
        image_label.image = img

def save_text_to_file():
    # Get the selected tab's text area
    selected_tab = notebook.select()
    text_area = notebook.nametowidget(selected_tab).winfo_children()[0]
    text = text_area.get(1.0, tk.END)

    if text.strip():  # Check if there is any text to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Word documents", "*.docx")]
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)

def copy_text_to_clipboard():
    # Get the selected tab's text area
    selected_tab = notebook.select()
    text_area = notebook.nametowidget(selected_tab).winfo_children()[0]
    text = text_area.get(1.0, tk.END)
    pyperclip.copy(text)

def create_gui():
    global window, notebook  # Make window and notebook global so they're accessible in other functions
    window = tk.Tk()
    window.title("Interactive OCR with Multi-image Processing")
    window.geometry("800x600")
    

    # Add a dropdown menu for language selection
    languages = {"English": "eng", "Spanish": "spa", "French": "fra", "German": "deu", "Hindi": "hin"}
    selected_language = tk.StringVar(window)
    selected_language.set("English")  # Default value

    language_menu = ttk.OptionMenu(window, selected_language, *languages.keys())
    language_menu.pack()

    # Add sliders for brightness, contrast, and thresholding
    brightness_scale = Scale(window, from_=0, to_=2, orient=HORIZONTAL, resolution=0.1, label="Brightness")
    brightness_scale.set(1.0)
    brightness_scale.pack()

    contrast_scale = Scale(window, from_=0, to_=2, orient=HORIZONTAL, resolution=0.1, label="Contrast")
    contrast_scale.set(1.0)
    contrast_scale.pack()

    threshold_scale = Scale(window, from_=0, to_=255, orient=HORIZONTAL, label="Threshold")
    threshold_scale.set(127)
    threshold_scale.pack()

    # Create a button to upload images
    upload_button = tk.Button(
        window, text="Upload Images", 
        command=lambda: open_file_dialog(selected_language.get(), brightness_scale.get(), contrast_scale.get(), threshold_scale.get()), 
        padx=20, pady=10)
    upload_button.pack()

    # Create a notebook (tabbed interface) to hold the results
    notebook = ttk.Notebook(window)
    notebook.pack(expand=True, fill='both')

    # Create buttons to save text to a file and copy to clipboard
    save_button = tk.Button(window, text="Save Text to File", command=save_text_to_file)
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    copy_button = tk.Button(window, text="Copy Text to Clipboard", command=copy_text_to_clipboard)
    copy_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Start the GUI event loop
    window.mainloop()

# Run the GUI
create_gui()
