
import json
import docker 
import shared
from backuper.backuper import packVolume, discoverVolumes, transfer

def main():
    config = loadAsJson("config.json")
    client = createClient()
    sharedObj = shared.SharedObject(config)
    print("[INFO] Starting autodiscovering")
    volumes = discoverVolumes(client, sharedObj)
    print("[INFO] Starting volume backups")
    toTransfer = []
    for volume in volumes:
        readyForTransfer = packVolume(client, sharedObj, volumes[volume])
        if(readyForTransfer):
            toTransfer.append(readyForTransfer)
    print("[INFO] Starting transfering")
    for transferable in toTransfer:
        transfer(sharedObj, transferable)

def createClient():
    return docker.from_env()

def loadAsJson(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    main()
