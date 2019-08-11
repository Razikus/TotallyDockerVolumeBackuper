from docker.types import Mount

def processMount(mount):
    result = dict()
    result["type"] = mount["Type"]
    result["source"] = mount["Source"]
    return result

def getMountType(mount, target):
    return Mount(type=mount["type"], source=mount["source"], target=target)

def getBackupName(mount):
    return mount["type"] + mount["source"].replace("/", "-") + ".tar.gz"