import docker 
import uuid
import tarfile
import os
import tempfile

def packVolume(client, sharedObj, spec):
    containerUuid = str(uuid.uuid4()).replace("-", "")
    processType = spec["process"]["type"]
    processor = sharedObj.processedTypes.get(processType, None)
    if(not processor):
        return False
    
    backupVolumeName = processor.getBackupName(spec["process"])
    for container in spec["containers"]:
        try:
            client.containers.get(container).pause()
        except:
            print("Cannot pause container", container)
    volumePathInContainer = "/volume"
    client.containers.run("razikus/volumebackuper:1.0", name = containerUuid, tty=True, mounts=[processor.getMountType(spec["process"], volumePathInContainer)], stream=False, detach=False, command=backupVolumeName)
    container = client.containers.get(containerUuid)
    transferArchive(container, "/" + backupVolumeName, "backups/" + containerUuid + ".tar.gz.tar")
    tar = tarfile.open("backups/" + containerUuid + ".tar.gz.tar")
    tar.extractall()
    tar.close()
    os.remove("backups/" + containerUuid + ".tar.gz.tar")
    container.remove()

    for container in spec["containers"]:
        try:
            client.containers.get(container).unpause()
        except:
            print("Cannot unpause container", container)
    return True

def transferArchive(container, path, transferPath, chunk_size=2097152):
    transferFile = open(transferPath, "wb")
    bits, stat = container.get_archive(path, chunk_size)
    for chunk in bits:
        transferFile.write(chunk)
    transferFile.close()
    return True


def discoverVolumes(client, sharedObj):
    containers = client.containers.list(all=True)
    volumes = {}
    for container in containers:
        mountsFromContainer = container.attrs.get("Mounts", dict())
        containerId = container.id
        for mount in mountsFromContainer:
            volumeName = mount["Source"]
            if(mount["Source"] in volumes):
                volumes[volumeName]["_specs"].append(mount)
                volumes[volumeName]["containers"].append(containerId)
            else:
                volumes[volumeName] = dict()
                volumes[volumeName]["_specs"] = [mount]
                volumes[volumeName]["containers"] = [containerId]
                processor = sharedObj.processedTypes.get(mount["Type"], None)
                if(processor):
                    volumes[volumeName]["process"] = processor.processMount(mount)
                else:
                    print("Can't process type:", mount["Type"])
                
    return volumes
    
