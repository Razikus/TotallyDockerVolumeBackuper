import docker 
import uuid
import tarfile
import os
import tempfile

def transfer(sharedObj, spec):
    name = spec["name"]
    path = spec["path"]
    processorType = "glacier"
    print("[TRANSFER] Starting transfer with processor type: " + processorType)
    sharedObj.backupTypes["glacier"].pushArchive(path)
    
def packVolume(client, sharedObj, spec):
    containerUuid = str(uuid.uuid4()).replace("-", "")
    processType = spec["process"]["type"]
    processor = sharedObj.processedTypes.get(processType, None)
    if(not processor):
        print(f"[PACKER FAIL] Can't process { processType }")
        return False
    backupVolumeName = processor.getBackupName(spec["process"])
    print(f"[PACKER] Processing { backupVolumeName } with type { processType }")
    for container in spec["containers"]:
        try:
            print(f"[PACKER] Pausing associated container { container }")
            client.containers.get(container).pause()
        except:
            print("[PACKER FAIL] Cannot pause container", container)
    volumePathInContainer = "/volume"
    print("[PACKER] Starting packer container...")
    client.containers.run("razikus/volumebackuper:1.0", name = containerUuid, tty=True, mounts=[processor.getMountType(spec["process"], volumePathInContainer)], stream=False, detach=False, command=backupVolumeName)
    print("[PACKER] Done!")
    container = client.containers.get(containerUuid)
    for toUnpause in spec["containers"]:
        try:
            print(f"[PACKER] Unpausing associated container { toUnpause }")
            client.containers.get(toUnpause).unpause()
        except:
            print("[PACKER FAIL] Cannot unpause container", toUnpause)
    print("[PACKER] Moving packed volume to temp directory...")
    with tempfile.TemporaryDirectory() as tmpdirname:
        transferArchive(container, "/" + backupVolumeName, os.path.join(tmpdirname, containerUuid + ".tar.gz.tar"))
        print("[PACKER] Done!")
        print("[PACKER] Unpacking packed volume...")
        tar = tarfile.open(os.path.join(tmpdirname, containerUuid + ".tar.gz.tar"))
        tar.extractall(path="backups")
        tar.close()
        print("[PACKER] Done!")
    container.remove()

    return {"name": processor.getSourceName(spec["process"]), "path": os.path.abspath(os.path.join("backups", backupVolumeName))}

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
        if(sharedObj.isContainerExcluded(container.name)):
            print("[AUTODISCOVER INFO] Container " + container.name + " excluded")
            continue
        mountsFromContainer = container.attrs.get("Mounts", dict())
        containerId = container.id
        for mount in mountsFromContainer:
            volumeName = mount["Source"]
            print("[AUTODISCOVER INFO] Discovered " + mount["Source"] + " from " + container.name)
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
                    print("[AUTODISCOVER FAIL] Can't process type:", mount["Type"])
                
    return volumes
    
