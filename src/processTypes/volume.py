from docker.types import Mount

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
    return mount["type"] + mount["name"] + ".tar.gz"