"""
PR PDF

settings - Helpers

2020 maschhoff github.com/maschhoff

"""

import json
import os

configsrc = os.environ["WORKDIR"]+'/config/config.json'

# or '/data/prpdf/config/config.json'

def getConfigRaw():
	config_raw= open(configsrc, 'r')
	return config_raw

def loadConfig():
    #print("loadConfig()")
    res={}

    if not os.path.exists(configsrc):
        writeConfig(""" {
        "port":80,
        "debug":"off",
        "lang":"eng",
        "updatetime":1800,
        "index":{
            "Foldername/Filename":["Keyword1"],
            "Foldername2/Filename":["Keyword1","Keyword2 ","Keyword3"]
        }
        }""")

    with open(configsrc, 'r') as fp:
        res = json.load(fp)
    return res
   
def writeJsonConfig(config):
    jc=json.dumps(config)
    writeConfig(jc)

def writeConfig(config):
	f = open(configsrc, "w")
	f.write(config)
	f.close()
