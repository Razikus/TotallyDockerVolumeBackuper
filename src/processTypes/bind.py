def processMount(mount):
    result = dict()
    result["type"] = mount["Type"]
    result["source"] = mount["Source"]
    return result