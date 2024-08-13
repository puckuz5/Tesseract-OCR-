import cv2
import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, Text
from tkinter import ttk, Scale, HORIZONTAL, messagebox
from langdetect import detect, DetectorFactory
import pyperclip
import threading
from googletrans import Translator, LANGUAGES
from textblob import TextBlob

# Configure the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path if needed

DetectorFactory.seed = 0  # To ensure consistency
translator = Translator()

def preprocess_image(image_path, brightness=1.0, contrast=1.0, threshold=127):
    try:
        # Load the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image could not be loaded. Please check the file format and path.")
        
        # Adjust brightness and contrast
        adjusted_image = cv2.convertScaleAbs(image, alpha=contrast, beta=int(100 * (brightness - 1)))

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding
        _, processed_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

        return processed_image
    except Exception as e:
        messagebox.showerror("Error", f"Failed to preprocess image: {e}")
        return None

def detect_language(text):
    try:
        language_code = detect(text)
    except:
        language_code = "und"  # Undefined if detection fails
    return language_code

def extract_text_from_image(image_path, language, brightness, contrast, threshold):
    processed_image = preprocess_image(image_path, brightness, contrast, threshold)
    if processed_image is None:
        return None, None

    pil_image = Image.fromarray(processed_image)
    custom_config = f'--psm 6 --oem 1 -l {language}'
    text = pytesseract.image_to_string(pil_image, config=custom_config)

    if not text.strip():
        messagebox.showwarning("No Text Detected", "No text was detected in the image. Please try another image or adjust the preprocessing settings.")
        return None, None

    detected_language = detect_language(text)
    return text, detected_language

def open_file_dialog(language, brightness, contrast, threshold):
    languages = {"English": "eng", "Spanish": "spa", "French": "fra", "German": "deu", "Hindi": "hin"}
    file_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if file_paths:
        threading.Thread(target=process_images, args=(file_paths, languages[language], brightness, contrast, threshold)).start()

def process_images(file_paths, language, brightness, contrast, threshold):
    for file_path in file_paths:
        show_loading_spinner()
        preview_image(file_path, brightness, contrast, threshold)
        extracted_text, detected_language = extract_text_from_image(file_path, language, brightness, contrast, threshold)
        hide_loading_spinner()

        if extracted_text is not None:
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=file_path.split("/")[-1])

            text_area = Text(tab, wrap=tk.WORD, height=20, padx=10, pady=10)
            text_area.insert(tk.END, f"Detected Language: {detected_language}\n\n{extracted_text}")
            text_area.pack(expand=True, fill='both')

            # Add translation, summarization, and keyword extraction options
            create_nlp_tools(tab, extracted_text)

def preview_image(image_path, brightness, contrast, threshold):
    processed_image = preprocess_image(image_path, brightness, contrast, threshold)
    if processed_image is None:
        return

    pil_image = Image.fromarray(processed_image)
    pil_image = pil_image.resize((400, 300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(pil_image)

    if 'image_label' not in globals():
        global image_label
        image_label = tk.Label(window, image=img)
        image_label.image = img
        image_label.pack()
    else:
        image_label.configure(image=img)
        image_label.image = img

def save_text_to_file():
    selected_tab = notebook.select()
    text_area = notebook.nametowidget(selected_tab).winfo_children()[0]
    text = text_area.get(1.0, tk.END)

    if text.strip():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Word documents", "*.docx")]
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)

def copy_text_to_clipboard():
    selected_tab = notebook.select()
    text_area = notebook.nametowidget(selected_tab).winfo_children()[0]
    text = text_area.get(1.0, tk.END)
    pyperclip.copy(text)

def translate_text(text, target_language):
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        messagebox.showerror("Translation Error", f"Failed to translate text: {e}")
        return None

def summarize_text(text):
    blob = TextBlob(text)
    return str(blob.noun_phrases)

def extract_keywords(text):
    blob = TextBlob(text)
    return ', '.join(blob.words)

def show_loading_spinner():
    global spinner
    spinner = tk.Label(window, text="Processing...", font=("Helvetica", 16))
    spinner.pack(pady=20)

def hide_loading_spinner():
    if 'spinner' in globals():
        spinner.pack_forget()

def create_nlp_tools(tab, extracted_text):
    nlp_frame = ttk.LabelFrame(tab, text="NLP Tools", padding=(10, 5))
    nlp_frame.pack(fill='x', padx=10, pady=10)

    # Translation Dropdown Menu
    translate_label = ttk.Label(nlp_frame, text="Translate to:")
    translate_label.grid(row=0, column=0, padx=5, pady=5)
    
    translate_var = tk.StringVar(value="Select Language")
    translate_menu = ttk.Combobox(nlp_frame, textvariable=translate_var, values=list(LANGUAGES.values()))
    translate_menu.grid(row=0, column=1, padx=5, pady=5)

    def translate_and_display():
        target_language = translate_var.get()
        if target_language != "Select Language":
            translated_text = translate_text(extracted_text, target_language)
            if translated_text:
                translation_area.delete(1.0, tk.END)
                translation_area.insert(tk.END, translated_text)

    translate_button = ttk.Button(nlp_frame, text="Translate", command=translate_and_display)
    translate_button.grid(row=0, column=2, padx=5, pady=5)

    # Summarization
    summary_button = ttk.Button(nlp_frame, text="Summarize Text", command=lambda: show_summary(extracted_text))
    summary_button.grid(row=1, column=0, padx=5, pady=5, columnspan=3)

    # Keyword Extraction
    keywords_button = ttk.Button(nlp_frame, text="Extract Keywords", command=lambda: show_keywords(extracted_text))
    keywords_button.grid(row=2, column=0, padx=5, pady=5, columnspan=3)

    # Translation Area
    translation_area = Text(nlp_frame, wrap=tk.WORD, height=6, padx=10, pady=10)
    translation_area.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

def show_summary(extracted_text):
    summary = summarize_text(extracted_text)
    messagebox.showinfo("Text Summary", summary)

def show_keywords(extracted_text):
    keywords = extract_keywords(extracted_text)
    messagebox.showinfo("Extracted Keywords", keywords)

def create_gui():
    global window, notebook
    window = tk.Tk()
    window.title("Interactive OCR with NLP and Translation Integration")
    window.geometry("800x600")

    languages = {"English": "eng", "Spanish": "spa", "French": "fra", "German": "deu", "Hindi": "hin"}
    selected_language = tk.StringVar(window)
    selected_language.set("English")

    language_menu = ttk.OptionMenu(window, selected_language, *languages.keys())
    language_menu.pack()

    brightness_scale = Scale(window, from_=0, to_=2, orient=HORIZONTAL, resolution=0.1, label="Brightness")
    brightness_scale.set(1.0)
    brightness_scale.pack()

    contrast_scale = Scale(window, from_=0, to_=2, orient=HORIZONTAL, resolution=0.1, label="Contrast")
    contrast_scale.set(1.0)
    contrast_scale.pack()

    threshold_scale = Scale(window, from_=0, to_=255, orient=HORIZONTAL, label="Threshold")
    threshold_scale.set(127)
    threshold_scale.pack()

    upload_button = tk.Button(
        window, text="Upload Images", 
        command=lambda: open_file_dialog(selected_language.get(), brightness_scale.get(), contrast_scale.get(), threshold_scale.get()), 
        padx=20, pady=10)
    upload_button.pack()

    notebook = ttk.Notebook(window)
    notebook.pack(expand=True, fill='both')

    save_button = tk.Button(window, text="Save Text to File", command=save_text_to_file)
    save_button.pack(side=tk.LEFT, padx=10, pady=10)

    copy_button = tk.Button(window, text="Copy Text to Clipboard", command=copy_text_to_clipboard)
    copy_button.pack(side=tk.RIGHT, padx=10, pady=10)

    window.mainloop()

create_gui()
