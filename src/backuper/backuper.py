
async def packVolume(client, volume: str, savePath: str, pauseContainers: bool):
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
                volumes[volumeName]["specs"].append(mount)
                volumes[volumeName]["containers"].append(containerId)
            else:
                volumes[volumeName] = dict()
                volumes[volumeName]["specs"] = [mount]
                volumes[volumeName]["containers"] = [containerId]
                processor = sharedObj.processedTypes.get(mount["Type"], None)
                if(processor):
                    volumes[volumeName]["process"] = processor.processMount(mount)
                else:
                    print("Can't process type:", mount["Type"])
                
    return volumes
    
