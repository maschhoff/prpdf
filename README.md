# PR PDF Explorer
Preview and Rename PDF Explorer

For easy view, rename and move scanned PDF files.
PDF OCR Autoscan function based on keywords

![Explorer](https://i.ibb.co/b723gYv/Explorer.jpg)
![OCR](https://i.ibb.co/JQb8Frf/OCR.jpg)

# Install and run

## Run as docker
` docker pull knex666/prpdf`

` docker run -d --name='PRPDF' -v '/mnt/user/Share':'/Archiv/':'rw' -v '/mnt/user/SCAN':'/source/static/pdf/':'rw' -v '/mnt/user/appdata/prpdf/':'/source/config':'rw' 'knex666/prpdf' python3 /source/prpdf.py`

## Run with python on linux
Note: Please enshure to run it from /source/ 
create a folder /Archiv for your files 
and a folder /source/static/pdf/ as location for you scanned pdfs
otherwise feel free to edit the sourcecode on vars.py etc.

* ` python3 -m pip install -r requirements.txt`
* ` sudo apt-get install tesseract-ocr poppler-utils`
* ` python3 prpdf.py`



# configuration
please copy and volume mount the example configuration from https://github.com/maschhoff/prpdf/blob/main/config/config.json

    "port":80, - choose any port you want
    "debug":"off", set so on or off to see ocr results while autoscan
    "lang":"deu", set the ocr language see https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
    "updatetime":1800, uptime in seconds

# donate
Buy me a Pizza -> https://www.buymeacoffee.com/maschhoff

