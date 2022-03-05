import os
from tokenize import String
FILEEXTENSION = "confirm"
__storage__ = {}

def stsave(value):
    id = len(__storage__)
    __storage__[id] = value
    return id
def stget(id):
    return __storage__[id]

def load(filename):
    with open(filename, "r") as f:
        return f.read()

def parse(string, confirm):
    LEN = True
    parsed = False
    try:
        string = int(string)
    except:
        pass
    linebyline = confirm.split("\n")
    for line in linebyline:
        if line.startswith("#"):
            continue
        else:
            type, value = line.split(":")
            values = value.split(",")
            if type == "LENGHT":
                parsed = True
                if not len(string) == int(value):
                    LEN = False
                else:
                    LEN = True
            if isinstance(string, str) and type == "STR" and LEN == True:
                for value in values:
                    if value == string:
                        return True
                    else:
                        continue
            if isinstance(string, int) and type == "INT" and LEN == True:
                for value in values:
                    if "-" in value:
                        valuex = value.split("-")
                        for valueR in range(int(valuex[0]), int(valuex[1])):
                            if valueR == string:
                                return True
                    else:
                        if int(value) == string:
                            return True
    print (
        parsed, LEN,
        "fallback triggered"
    )
    return parsed==LEN
                        

class file:
    def __init__(self, confirm_file: str):
        self.confirm_file = load(confirm_file)
    def confirm(self, var: str):
        print("Confirming: "+var+"| with: "+self.confirm_file)
        return parse(var, self.confirm_file)