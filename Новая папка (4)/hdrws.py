from googletrans import Translator
from gtts import gTTS
import playsound
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from docx import Document
import fitz  

def translate_and_speak(text):
    try:
        selected_language = language_var.get()
        target_lang = lang_codes.get(selected_language, "en")

        # Убедиться, что текст для перевода является строкой
        if not isinstance(text, str):
            raise ValueError("Текст должен быть строкой.")

        # Логирование текста для перевода
        print(f"Translating text: {text}")

        translation_result = translator.translate(text, dest=target_lang)
        
        # Проверка, что translation_result не None
        if not translation_result or not translation_result.text:
            raise ValueError("Не удалось получить результат перевода. API вернуло None или пустой результат.")

        translated_text = translation_result.text

        print(f"Translated text: {translated_text}")

        tts = gTTS(text=translated_text, lang=target_lang)
        file_path = "temp.mp3"
        tts.save(file_path)
        playsound.playsound(file_path)
        os.remove(file_path)
    except Exception as e:
        translated_text = locals().get('translated_text', "None")
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}\nText: {text}\nTranslated: {translated_text}")

def translate_and_speak_text():
    text = text_entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Предупреждение", "Введите текст для перевода.")
        return
    translate_and_speak(text)

def load_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("Word documents", "*.docx"), ("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    if not file_path:
        return

    content = ""
    try:
        if file_path.endswith(".txt"):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            for para in doc.paragraphs:
                content += para.text + "\n"
        elif file_path.endswith(".pdf"):
            pdf_document = fitz.open(file_path)
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                content += page.get_text()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='windows-1251') as file:
                content = file.read()
        except UnicodeDecodeError:
            messagebox.showerror("Ошибка", "Не удалось прочитать файл. Убедитесь, что файл закодирован в поддерживаемой кодировке.")
            return
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
        return

    text_entry.delete("1.0", tk.END)
    text_entry.insert(tk.END, content)
    translate_and_speak(content)

app = tk.Tk()
app.title("Text Translator and Speaker")
app.state('zoomed')  # Открытие приложения на весь экран

# Настройка стилей
style = ttk.Style()
style.theme_use("clam")

style.configure('TButton', font=('Helvetica', 12), padding=6)
style.configure('TLabel', font=('Helvetica', 12), padding=6)
style.configure('TCombobox', font=('Helvetica', 12), padding=6)
style.configure('TText', font=('Helvetica', 12))

translator = Translator()

# Определение кодов языков
lang_codes = {
    "Английский": "en",
    "Русский": "ru",
    "Испанский": "es",
    "Немецкий": "de",
    "Французский": "fr",
    "Итальянский": "it",
    "Португальский": "pt",
    "Китайский": "zh-cn",
    "Японский": "ja",
    "Корейский": "ko",
    "Арабский": "ar",
    "Хинди": "hi"
}

# Создание виджетов
frame = ttk.Frame(app, padding="10 10 10 10")
frame.pack(fill=tk.BOTH, expand=True)

language_label = ttk.Label(frame, text="Выберите язык для перевода и озвучивания:")
language_label.grid(row=0, column=0, columnspan=2, pady=10, sticky=tk.W)

language_var = tk.StringVar()
language_combobox = ttk.Combobox(frame, textvariable=language_var, state="readonly")
language_combobox['values'] = tuple(lang_codes.keys())
language_combobox.current(0)
language_combobox.grid(row=1, column=0, columnspan=2, pady=10, sticky=tk.W + tk.E)

text_label = ttk.Label(frame, text="Введите текст для перевода и озвучивания:")
text_label.grid(row=2, column=0, columnspan=2, pady=10, sticky=tk.W)

text_entry = tk.Text(frame, height=20, width=80, wrap=tk.WORD, font=('Helvetica', 12))
text_entry.grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)

speak_button = ttk.Button(frame, text="Перевести и озвучить", command=translate_and_speak_text)
speak_button.grid(row=4, column=0, pady=10, sticky=tk.W + tk.E)

load_button = ttk.Button(frame, text="Загрузить файл и перевести", command=load_file)
load_button.grid(row=4, column=1, pady=10, sticky=tk.W + tk.E)

# Настройка адаптивного интерфейса
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(3, weight=1)

app.mainloop()
