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
        return render_template('layout.html', liste=pdf, preview=search['name'], folders=loadArchivFolder())

@app.route('/autoscan')
def autoscan():
        run()

        pdf=loadFiles()
        if pdf:
                search=pdf[0]
        else:
                search={}
                search["name"]=""
        return render_template('layout.html', liste=pdf, preview=search['name'], folders=loadArchivFolder())

@app.route('/<string:id>')
def filter(id):
        pdf=loadFiles()
        res=[]
        for p in pdf:
                if id in p["name"]:
                        res.append(p)
        search=pdf[0]
        return render_template('layout.html', liste=res, preview=search['name'], folders=loadArchivFolder())


@app.route('/', methods=['POST'])
def my_form_post():
        newid = request.form['pdf']
        id = request.form['oldpdf']
        folder=request.form['folder']
        print(folder)
        if newid!="":
                if folder!="unknown":
                        shutil.move(unknown_dir+"/"+id,archiv_dir+"/"+folder+"/"+newid+'.pdf')
                else:
                        shutil.move(unknown_dir+"/"+id,unknown_dir+"/"+newid+'.pdf') 
        pdf=loadFiles()
        if newid!="":
                return render_template('layout.html', message="title changed", liste=pdf, preview=newid+'.pdf', folders=loadArchivFolder())
        else:
                return render_template('layout.html', message="Error: title was empty", liste=pdf, preview=id, folders=loadArchivFolder())


@app.route('/settings')
def setting():
	config_raw= settings.getConfigRaw()
	return render_template('settings.html', config=config, config_raw=config_raw.read())


def loadArchivFolder():
        return os.listdir(archiv_dir)

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