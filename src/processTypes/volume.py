def processMount(mount):
    result = dict()
    result["type"] = mount["Type"]
    result["name"] = mount["Name"]
    result["driver"] = mount["Driver"]
    return result