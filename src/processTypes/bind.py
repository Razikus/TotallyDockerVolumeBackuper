from docker.types import Mount
import datetime

def processMount(mount):
    result = dict()
    result["type"] = mount["Type"]
    result["source"] = mount["Source"]
    return result

def getMountType(mount, target):
    return Mount(type=mount["type"], source=mount["source"], target=target)

def getBackupName(mount):
    now = datetime.datetime.now()
    prefix = now.strftime('%Y%m%d%H%M%S')
    return prefix + mount["type"] + mount["source"].replace("/", "-") + ".tar.gz"

def getSourceName(mount):
    return mount["source"]