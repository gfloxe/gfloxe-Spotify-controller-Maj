import traceback
import time

def log_error(message):
    with open("error_log.txt", "a") as log_file:
        log_file.write(message + "\n")
        traceback.print_exc(file=log_file)

def scroll_text(label, text, delay=200):
    text = text[1:] + text[0]
    label.config(text=text)
    label.after(delay, lambda: scroll_text(label, text, delay))

def scroll_text_if_needed(label, text):
    label.config(text=text)
    label.update_idletasks()
    if label.winfo_reqwidth() > label.winfo_width():
        label.after(200, lambda: scroll_text(label, text, 200))
