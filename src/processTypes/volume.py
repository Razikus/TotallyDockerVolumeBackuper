from docker.types import Mount
import datetime

def processMount(mount):
    result = dict()
    result["type"] = mount["Type"]
    result["name"] = mount["Name"]
    result["driver"] = mount["Driver"]
    result["source"] = mount["Source"]
    return result

def getMountType(mount, target):
    return Mount(type=mount["type"], source=mount["name"], target=target)


def getBackupName(mount):
    now = datetime.datetime.now()
    prefix = now.strftime('%Y%m%d%H%M%S')
    return prefix + mount["type"] + "-" + mount["name"] + ".tar.gz"

def getSourceName(mount):
    return mount["name"]