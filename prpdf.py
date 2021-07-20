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

app = Flask(__name__)


@app.route('/')
def index():
        pdf=loadFolder()
        search=pdf[0]
        return render_template('layout.html', liste=pdf, preview=search['name'])



@app.route('/', methods=['POST'])
def my_form_post():
        newid = request.form['pdf']
        id = request.form['oldpdf']
        if newid!="":
                os.rename(r'/source/static/pdf/'+id,r'/source/static/pdf/'+newid+'.pdf')
        pdf=loadFolder()
        if newid!="":
                return render_template('layout.html', message="title changed", liste=pdf, preview=newid+'.pdf')
        else:
                return render_template('layout.html', message="Error: title was empty", liste=pdf, preview=id)

def loadFolder():
        
        folder="/source/static/pdf/"
        files=os.listdir(folder)
        res=[]
        for file in files:
                filer={}
                filer["name"]=file
                filer["size"]=str(os.path.getsize(folder+file)/1000000)+" MB"
                timestamp = date.fromtimestamp(os.path.getctime(folder+file))
                filer["date"]=timestamp
                res.append(filer)
        
        return res


if __name__ == '__main__':
	logging.basicConfig(filename='server.log',level=logging.INFO)


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

	app.run(host='0.0.0.0',port=80,debug=True)
