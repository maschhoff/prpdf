import json
import os

# Configuration file path, depends on WORKDIR environment variable
configsrc = os.path.join(os.environ.get("WORKDIR", "."), "config", "config.json")

def getConfigRaw():
    """
    Returns a file object opened in read mode for the raw config JSON file.
    Caller is responsible for closing the file.
    """
    return open(configsrc, 'r')

def loadConfig():
    """
    Loads the configuration JSON from file.
    If the config file does not exist, creates it with default values.
    Returns the configuration as a Python dictionary.
    """
    if not os.path.exists(configsrc):
        default_config = """
        {
            "port": 80,
            "debug": "off",
            "lang": "eng",
            "updatetime": 1800,
            "append_date": true,
            "append_random": true,
            "enable_update_flag": true,
            "index": {
                "Foldername/Filename": ["Keyword1"],
                "Foldername2/Filename": ["Keyword1", "Keyword2", "Keyword3"]
            }
        }
        """
        writeConfig(default_config)

    with open(configsrc, 'r') as fp:
        return json.load(fp)

def writeJsonConfig(config_dict):
    """
    Accepts a dictionary, serializes it to JSON string, and writes to config file.
    """
    json_str = json.dumps(config_dict, indent=4)
    writeConfig(json_str)

def writeConfig(config_str):
    """
    Writes a JSON string directly to the config file.
    """
    with open(configsrc, "w") as f:
        f.write(config_str)
