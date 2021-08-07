#importing modules

import pytesseract
# Wenn tesseract exe nicht im System PATH angegeben, dann:
#pytess= r"/home/detleva/.local/bin"
from PIL import Image
# Wenn poppler/bin  nicht im System PATH angegeben, dann:
#pdftoppm_path = r"/home/detleva/.local/bin/pdftoppm"
import os#, subprocess
from pdf2image import convert_from_path
from datetime import datetime
import logging
import time
from datetime import datetime, date
import threading
import shutil
import random
import settings




os.chdir(r'/source/')

#Logging
logging.basicConfig(filename='/source/config/server.log',level=logging.INFO)

#Filedate
#filedatum=datetime.now().strftime('%d_%m_%Y+0') # filename + Tag_Monat_Jahr_Counter

# SETTINGS

config=settings.loadConfig()

lang= config["lang"]
debug=config["debug"]
updatetime=config["updatetime"]
index=config["index"]


# Folder - !!! DO NOT CHANGE FOR DOCKER !!!!

pdf_dir = r"/source/static/pdf"           # Source
temp_dir = r"/tmp/images"        # Temp
archiv_dir= r"/Archiv/"      # Oberordner Archiv -- darunter Ablage der Item Ordner
unknown_dir=r"/source/static/pdf/unknown"     # nicht erkannte PDFs

#Ordner anlegen

if not os.path.exists(archiv_dir):
    os.makedirs(archiv_dir)
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
if not os.path.exists(unknown_dir):
    os.makedirs(unknown_dir,mode = 0o777)


# CRON THREAD

# CRON Run
def autoscan_cron():
    while True:
        logging.info("STARTING CRONJOB PR PDF AUTOSCAN "+str(datetime.now()))
        print("STARTING CRONJOB PR PDF AUTOSCAN "+str(datetime.now()))
        try:
            run()
        except Exception as e:
            print("An exception occurred "+e)
            logging.error("An exception occurred "+e)
        time.sleep(updatetime) # TODO conf updatetime

# aus OCR text indexieren und PDFs in Ordner schieben
def sort(pdf_file,text):
    if debug=="on":
        print("---------------------------------------------------\n\n")
        print(text)
        print("---------------------------------------------------\n\n")
        
    for archiv_item in index:                 # Schleife uber DICT
        ordner,filename=archiv_item.split("/")
        count=0
        treffer=0
        for keywords in index[archiv_item]:   # Schleife uber Keywords in einem Item    
            treffer = text.find(keywords)     # match ein Keyword      
            if treffer>=0:
                count+=1
        if count>=len(index[archiv_item]):    # match auf alle Keywords
            if not os.path.exists(archiv_dir+"/"+ordner): # Ordner mit Item aus Dict anlegen
                os.makedirs(archiv_dir+"/"+ordner)
            filedatum=date.fromtimestamp(os.path.getmtime(pdf_dir+"/"+pdf_file)).strftime('%d_%m_%Y')
            fileneu=filename+"_"+filedatum+"_"+str(random.randint(1111,9999))+".pdf" 

    
            logging.info("MOVE "+pdf_dir+"/"+pdf_file+" to "+archiv_dir+"/"+ordner+"/"+fileneu)   
            print("MOVE "+pdf_dir+"/"+pdf_file+" to "+archiv_dir+"/"+ordner+"/"+fileneu) 
            shutil.move(pdf_dir+"/"+pdf_file, archiv_dir+"/"+ordner+"/"+fileneu) # pdf File in Ordner

def run():           
    # PDFs in Bilder umwandeln und OCR Texterkennung 
    print("Run Dir")
    for pdf_file in os.listdir(pdf_dir):   # Schleife uber Source Ordner 
        print("---- OCR PDF-File: ",pdf_file," ----\n")
        if pdf_file.endswith(".pdf"):
            temp=temp_dir+"/"+pdf_file[:-4]
            source=pdf_dir+"/"+pdf_file
        # Bilder aus pdf
            pages=convert_from_path(source, dpi=400,first_page=1,last_page=1,grayscale=True)
            count=0
            for page in pages:
                count+=1
                filename=temp+"_"+str(count)+".jpg"
                page.save(filename,'JPEG')
                
        # OCR Texterkennung
            try:
                text=pytesseract.image_to_string(Image.open(temp+"_1.jpg"),lang=lang)
            except:
                text=""
            sort(pdf_file,text) # PDFs der Reihe nach indexieren
            
    print("Run Del")    
    for image_file in os.listdir(temp_dir): # temp Dir loeschen
        os.remove(temp_dir+"/"+image_file)
    print("Move")        
    for unknown_file in os.listdir(pdf_dir): # nicht erkannte PDFs nach unknown kopieren
        if os.path.isfile(pdf_dir+"/"+unknown_file):
                logging.info("MOVE "+pdf_dir+"/"+unknown_file+" to "+unknown_dir+"/"+unknown_file)
                print("MOVE "+pdf_dir+"/"+unknown_file+" to "+unknown_dir+"/"+unknown_file)
                shutil.move(pdf_dir+"/"+unknown_file,unknown_dir+"/"+unknown_file)


#Cron Thread start
th = threading.Thread(target=autoscan_cron)
th.start()
