from .modules import DynamicPythonModuleLoader

class SharedObject:
    def __init__(self, config):
        self.dynamicLoader = DynamicPythonModuleLoader()
        self.config = config
        self.processedTypes = self.dynamicLoader.loadModulesAndAssignNames(self.config["processTypes"])
        self.backupTypes = self.dynamicLoader.loadModulesAndAssignNames(self.config["backupTypes"])
        self.defaultMethod = self.config.get("defaultMethod", dict())
        self.volumeSpecific = self.config.get("volumeSpecific", [])
    
    def isContainerExcluded(self, name):
        return name in self.config["excludedContainersFromAutoDiscover"]

    def getBackupTypeForVolume(self, volumeName):
        found = self.defaultMethod
        for vol in self.volumeSpecific:
            if(vol.get("name", "") == ""):
                return vol
        return found
