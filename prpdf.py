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
import settings
from autoscan import *

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

@app.route('/autoscan')
def autoscan():
        try:
            run()
        except Exception as e:
            print("An exception occurred "+e)
            logging.error("An exception occurred "+e)

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
        
        filedatum=date.fromtimestamp(os.path.getmtime(unknown_dir+"/"+id)).strftime('%d_%m_%Y')
        fileneu=newid+"_"+filedatum+"_"+str(random.randint(1111,9999))+".pdf" 
        
        print(folder)
        if newid!="":
                if folder!="unknown":
                        shutil.move(unknown_dir+"/"+id,archiv_dir+"/"+folder+"/"+fileneu)
                else:
                        shutil.move(unknown_dir+"/"+id,unknown_dir+"/"+fileneu) 
        pdf=loadFiles()
        if newid!="":
                return render_template('explorer.html', message="title changed", liste=pdf, preview=newid+'.pdf', folders=loadArchivFolder(),iterator=iterator)
        else:
                return render_template('explorer.html', message="Error: title was empty", liste=pdf, preview=id, folders=loadArchivFolder(),iterator=iterator)


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
        
        folder=unknown_dir # config unknown dir
        files=os.listdir(folder)
        res=[]
        for file in files:
                filer={}
                filer["name"]=file
                filer["size"]=str(os.path.getsize(folder+"/"+file)/1000000)+" MB"
                timestamp = date.fromtimestamp(os.path.getmtime(folder+"/"+file))
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
