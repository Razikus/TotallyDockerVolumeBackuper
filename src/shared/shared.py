from .modules import DynamicPythonModuleLoader

class SharedObject:
    def __init__(self, config):
        self.dynamicLoader = DynamicPythonModuleLoader()
        self.config = config
        self.processedTypes = self.dynamicLoader.loadModulesAndAssignNames(self.config["processTypes"])
        self.backupTypes = self.dynamicLoader.loadModulesAndAssignNames(self.config["backupTypes"])