import glob
import importlib
import sys

class DynamicPythonModuleLoader:
    def importDynamicImportModuleFromPath(self, path):
        if(path not in sys.path):
            sys.path.append(path)
        if(path.endswith(".py")):
            path = path[:-3]
        path = path.replace("/", ".")
        return importlib.import_module(path)

    def getModuleNameFromPath(self, path):
        if(path.endswith(".py")):
            path = path[:-3]
        splitted = path.split("/")
        return splitted[-1]

    def loadModulesAndAssignNames(self, directories):
        ''' loads all files from directories and assign names without .py name '''
        result = dict()
        for path in directories:
            onlyfiles = glob.glob(path)
            for file in onlyfiles:
                name = self.getModuleNameFromPath(file)
                module = self.importDynamicImportModuleFromPath(file)
                result[name] = module
        return result
            


