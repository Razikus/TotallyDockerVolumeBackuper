
import json
import docker 
import shared
from backuper.backuper import packVolume, discoverVolumes



def main():
    config = loadAsJson("config.json")
    client = createClient()
    sharedObj = shared.SharedObject(config)
    volumes = discoverVolumes(client, sharedObj)

def createClient():
    return docker.from_env()




def loadAsJson(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    main()
