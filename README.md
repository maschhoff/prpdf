# PR PDF Explorer
Preview and Rename PDF Explorer\

For easy view, rename and move scanned PDF files.\

Functions:
* PDF OCR Autoscan will move known documents based on keywords
* PDF Merge let you merge documents (1+1 and front and back pages)

How it works:
1. Documents get scanned to a scan-folder 
2. these documents will be autoscanned and moved to the specific locations
3. Any files that are not recognized by autoscan will be moved to the subfolder "unknown" of the scan-folder
4. The Webbased PR PDF Explorer lists all documents of the "unknown" folder.

How it looks like:

![Explorer](https://i.ibb.co/b723gYv/Explorer.jpg)
![OCR](https://i.ibb.co/JQb8Frf/OCR.jpg)

# Install and run

## Run as docker
` docker pull knex666/prpdf`

` docker run -d --name='PRPDF' -p 80:80 -v '/mnt/user/Share':'/Archiv/':'rw' -v '/mnt/user/SCAN':'/source/static/pdf/':'rw' -v '/mnt/user/appdata/prpdf/':'/source/config':'rw' 'knex666/prpdf' python3 /source/prpdf.py`

* Note 1: remember to setup the network to map the port of your configuration ` -p 80:80` you can choose any port you want see config
* Note 2: besited a folder structure for documents in a folder you mount to /Archiv/ you can volume mount any directory you want to /Archiv/ to build you own virtual folder structure
` -v '/mnt/user/Files/Accounting':'/Archiv/Accounting':'rw'` etc.

## Run with python on linux
Note: Please ensure to run it from /source/ 
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

