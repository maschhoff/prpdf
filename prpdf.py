"""

PR PDF

Main Server File

2020 maschhoff github.com/maschhoff

""" 

import os
from flask import Flask, render_template, request
from datetime import datetime, date
import logging
import time
import threading
import shutil
import random
import settings
import autoscan
import merge
from vars import *

app = Flask(__name__)


@app.route('/')
def index():
        pdf=loadFiles()
        if pdf:
                search=pdf[0]
        else:
                search={}
                search["name"]=""
        return render_template('explorer.html', liste=pdf, preview=search['name'], folders=loadArchivFolder(),iterator=0)


@app.route('/', methods=['POST'])
def my_form_post():
        newid = request.form['pdf']
        id = request.form['oldpdf']
        folder=request.form['folder']
        iterator=request.form['inputiterator']
        
        filedatum=date.fromtimestamp(os.path.getmtime(unknown_dir+id)).strftime('%d_%m_%Y')
        fileneu=newid+"_"+filedatum+"_"+str(random.randint(1111,9999))+".pdf" 
        
        print(folder)
        if newid!="":
                if folder!="unknown":
                        shutil.move(unknown_dir+id,archiv_dir+"/"+folder+"/"+fileneu)
                else:
                        shutil.move(unknown_dir+id,unknown_dir+"/"+fileneu) 
        pdf=loadFiles()
        if newid!="":
                return render_template('explorer.html', message="title changed", liste=pdf, preview=newid+'.pdf', folders=loadArchivFolder(),iterator=iterator)
        else:
                return render_template('explorer.html', message="Error: title was empty", liste=pdf, preview=id, folders=loadArchivFolder(),iterator=iterator)


@app.route('/merge')
def domerge():
        pdf=loadFiles()
        return render_template('merge.html', files=pdf)

@app.route('/merge', methods=['POST'])
def domergepost():
        file1 = request.form['file1']
        file2 = request.form['file2']
        option = request.form['option']
        filename = request.form['pdf']

        if "merge" in option:
                message=merge.pdf_merge_file(unknown_dir+file1,unknown_dir+file2,filename)
        else:
                message=merge.pdf_adf(unknown_dir+file1,unknown_dir+file2,filename)

        pdf=loadFiles()
        return render_template('explorer.html', liste=pdf, message=message, folders=loadArchivFolder(),iterator=0)

@app.route('/autoscan')
def doautoscan():
        try:
            autoscan.run()
        except Exception as e:
            print("An exception occurred "+str(e))
            logging.error("An exception occurred "+str(e))

        pdf=loadFiles()
        if pdf:
                search=pdf[0]
        else:
                search={}
                search["name"]=""
        return render_template('explorer.html', liste=pdf, preview=search['name'], folders=loadArchivFolder(),iterator=0)

@app.route('/<string:id>')
def doocr(id):
        text=autoscan.ocr(unknown_dir,id) 
        return render_template('magic.html', text=text, folders=loadArchivFolder(), pdf=id)

@app.route('/magic', methods=['POST'])
def autoscan_rule():
        newid = request.form['pdf']
        folder = request.form['folder']
        keywords = request.form['keywords']
        
        keyw_array=keywords.split(",")
        key=folder+"/"+newid

        config["index"].update({key:keyw_array})
        settings.writeJsonConfig(config)

        pdf=loadFiles()
        return render_template('explorer.html', liste=pdf, folders=loadArchivFolder(),iterator=0, message="autoscan rule saved")

@app.route('/settings')
def setting():
	config_raw= settings.getConfigRaw()
	return render_template('settings.html', config=config, config_raw=config_raw.read())

@app.route('/settings', methods=['POST'])
def setting_save():
	config_raw=request.form['hiddenconfig']
	settings.writeConfig(config_raw)
	global config
	config=settings.loadConfig()
	#os.execl(sys.executable, sys.executable, *sys.argv)
	return render_template('settings.html', config=config, config_raw=config_raw, message="config saved")


def loadArchivFolder():
        return sorted(os.listdir(archiv_dir))

def loadFiles():
        
        res=[]
        if os.path.exists(unknown_dir):
                files=sorted(os.listdir(unknown_dir))
                
                for file in files:
                        filer={}
                        filer["name"]=file
                        filer["size"]=str(os.path.getsize(unknown_dir+file)/1000000)+" MB"
                        timestamp = date.fromtimestamp(os.path.getmtime(unknown_dir+file))
                        filer["date"]=timestamp
                        res.append(filer)
        
        return res


if __name__ == '__main__':
        logging.basicConfig(filename='/source/config/server.log',level=logging.INFO)
        config=settings.loadConfig()

        #Server start
        logging.info("Start PR PDF Server...")
        print("Start PR PDF Server...")
        print(""" 
	
	 (\__/)  .-  -.)
	 /0 0 `./    .'
	(O__,   \   (
	  / .  . )  .
	  |-| '-' \  )
	  (   _(   ).'
	°....~....$

	  PR PDF

	""")

        app.run(host='0.0.0.0',port=config["port"],debug=True)
