import pytesseract
import ocrmypdf
# If tesseract exe is not in system PATH, set pytess accordingly:
# pytess = r"/home/detleva/.local/bin"
from PIL import Image
# If poppler/bin is not in system PATH, set pdftoppm_path accordingly:
# pdftoppm_path = r"/home/detleva/.local/bin/pdftoppm"
import os
import PyPDF2
from datetime import datetime, date
import logging
import time
import threading
import shutil
import random
import settings
import status
from vars import *

work_dir = os.environ['WORKDIR']

os.chdir(work_dir)

# SETTINGS
config = settings.loadConfig()

lang = config["lang"]
debug = config["debug"]
updatetime = float(config["updatetime"])
index = config["index"]

# Create directories if they don't exist
if not os.path.exists(archiv_dir):
    os.makedirs(archiv_dir)
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
if not os.path.exists(unknown_dir):
    os.makedirs(unknown_dir, mode=0o777)


# CRON THREAD

import uuid
cron_running = False  # global flag to avoid concurrent cron runs

def autoscan_cron():
    global cron_running
    if cron_running:
        print("Cronjob already running, skipping new start.")
        return
    cron_running = True
    try:
        while True:
            print(f"STARTING CRONJOB Interval: {updatetime} - Time: {datetime.now()}")
            try:
                run()
            except Exception as e:
                print(f"Exception in autoscan_cron: {e}")
            time.sleep(updatetime)
    finally:
        cron_running = False


# Function to index text from OCR and move PDFs to folders based on keywords
def sort(pdf_file, text):
    if debug == "on":
        print("---------------------------------------------------\n\n")
        print(text)
        print("---------------------------------------------------\n\n")
        
    for archiv_item in index:  # Loop over dict keys
        try:
            folder, filename = archiv_item.split(";")
        except ValueError:
            logging.error(f"Invalid index key format (expected 'folder;filename'): {archiv_item}")
            continue
        
        count = 0
        for keyword in index[archiv_item]:  # Loop over keywords in each item
            if text.find(keyword) >= 0:  # Keyword match
                count += 1
        
        if count >= len(index[archiv_item]):  # All keywords matched
            if not os.path.exists(folder):
                os.makedirs(folder)
            file_date = date.fromtimestamp(os.path.getmtime(os.path.join(pdf_dir, pdf_file))).strftime('%d_%m_%Y')
            new_filename = f"{filename}_{file_date}_{random.randint(1111,9999)}.pdf"

            logging.info(f"MOVE {os.path.join(pdf_dir, pdf_file)} to {os.path.join(folder, new_filename)}")
            print(f"MOVE {os.path.join(pdf_dir, pdf_file)} to {os.path.join(folder, new_filename)}")
            shutil.move(os.path.join(pdf_dir, pdf_file), os.path.join(folder, new_filename))


def run():
    global update_needed

    if not config.get("enable_update_flag", True):
        logging.info("Update flag disabled in config - update_needed will not be set.")

    # Convert PDFs to images and perform OCR text recognition
    print("Running directory action - converting PDFs to images and performing OCR")
    for pdf_file in os.listdir(pdf_dir):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        if not os.path.isfile(pdf_path):
            logging.info(f"IGNORING FOLDER: {pdf_path}")
            continue
        try:
            text = ocr(pdf_dir, pdf_file)
            if text is None:
                logging.warning(f"No text extracted from {pdf_file}, skipping.")
                continue
            sort(pdf_file, text)  # Only if text is present
        except Exception as e:
            logging.error(f"Exception in run: {e}")
            print(f"Exception in run: {e}")
            continue

    print("Running deletion action - clearing temp directory")
    for image_file in os.listdir(temp_dir):
        image_path = os.path.join(temp_dir, image_file)
        if os.path.isfile(image_path):
            os.remove(image_path)

    print("Running move action - moving unrecognized PDFs to unknown folder")
    moved_files = False
    for unknown_file in os.listdir(pdf_dir):
        source_path = os.path.join(pdf_dir, unknown_file)
        dest_path = os.path.join(unknown_dir, unknown_file)
        if os.path.isfile(source_path):
            logging.info(f"MOVE {source_path} to {dest_path}")
            print(f"MOVE {source_path} to {dest_path}")
            shutil.move(source_path, dest_path)
            moved_files = True

    # Set update_needed flag only if files moved and config flag enabled
    if moved_files and config.get("enable_update_flag", True):
        status.update_needed = True
    else:
        status.update_needed = False


def ocrpdf(file_path, save_path):
    logging.info(f"--- Running OCRmyPDF on: {file_path}")
    ocrmypdf.ocr(file_path, save_path, rotate_pages=True, language=lang, deskew=True, force_ocr=True)


def ocr(folder, pdf_file):
    print(f"---- Performing OCR on PDF file: {pdf_file} ----\n")
    if pdf_file.endswith(".pdf"):
        source = os.path.join(folder, pdf_file)
        try:
            ocrpdf(source, source)
            with open(source, "rb") as pdf_file_obj:
                reader = PyPDF2.PdfFileReader(pdf_file_obj)
                number_of_pages = reader.getNumPages()
                page = reader.pages[0]
                page_content = page.extractText()
            return page_content
        except Exception as e:
            logging.error(f"Exception occurred in OCRPDF: {e}")


# Start the cron thread
th = threading.Thread(target=autoscan_cron, daemon=True)
th.start()
