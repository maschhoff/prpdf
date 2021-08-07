"""
PR PDF

settings - Helpers

2020 maschhoff github.com/maschhoff

"""

import json

def getConfigRaw():
	config_raw= open('/source/config/config.json', 'r')
	return config_raw

def loadConfig():
    #print("loadConfig()")
    res={}
    with open('/source/config/config.json', 'r') as fp:
        res = json.load(fp)
    return res
   

def writeConfig(config):
	f = open("/source/config/config.json", "w")
	f.write(config)
	f.close()