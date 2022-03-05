import json
def profiles(config = "etc/settings.json"):
    """
    checks if profile name are same
    returns:
        [
            [0, "profile 1"],
            [1, "profile 2"]
        ]
    """
    config = json.load(config)
    validprofiles = []
    i=0
    for profile in list(config.keys()):
        if profile == config[profile]["profile_name"]:
            validprofiles.append([i, profile])
            i+=1
    return validprofiles
def profile(config = "etc/settings.json", pointer: int = None, profile_name = None):
    if pointer == None and profile_name == None:
        print (pointer, profile_name)
        raise Exception("profile() needs either a pointer or a profile name")
    if pointer and profile_name:
        raise Exception("profile selector require exactly one identifier 2 supplied")
    with open (config, "r") as f:
        try:
            config=json.load(f)
        except Exception as e:
            print("An error occured while loading settings.json", e)
            config = {}
    if pointer:
        return config[pointer]
    elif profile_name:
        for profile in config.keys():
            if config[profile]["profile_name"] == profile_name:
                return config[profile]
        raise Exception("profile_name not found")
def cheats(profil, config = "etc/settings.json", schema = "etc/config_schema.json"):
    """
    returns a list of cheats
    profil is dict of active settings
    """
    with open (config, "r") as f:
        try:
            config=json.load(f)
        except Exception as e:
            print("An error occured while loading settings.json", e)
            config = {}
    with open (schema, "r") as f:
        try:
            schema=json.load(f)
        except Exception as e:
            print("An error occured while loading settings.json", e)
            schema = {}
    returnmodules = [
        #modulepath,
        #modulestatus
    ]
    for item in profil.keys():
        print (item)
        print(schema[item])
        try:
            returnmodules.append([schema[item]["path"], profil[item] == True])
        except Exception as e:
            print("An error occured while loading settings.json", e)
            pass
    return returnmodules
    