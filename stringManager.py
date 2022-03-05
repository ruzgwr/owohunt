#this is a module, import it to use it
if __name__ == "__main__":
    exit()

import os, json
def avaible_languages(app_version = open('version.txt').readline()):
    """
    returns a list of avaible languages
    """
    files = os.listdir("etc/languages")
    files = [f for f in files if f.endswith(".json")] #json dosyalarını al
    languages = []
    for f in files:
        #sürüm kontrolü
        try:
            x = json.load(open("etc/languages/"+f))
        except:
            print("Json Decode Error: in file etc/languages/"+f)
        try:
            if x["__TRANSLATION_FILE_VERSION"] == app_version:
                languages.append(f[:-5])
            else:
                print("Version mismatch: etc/languages/"+f)
        except:
            print("File version error: in file etc/languages/"+f)
    return languages
class stringman():
    def __init__(self, language = "en"):
        """
        used to get strings from a language file 
        usage:
        languagemanager = stringManager.stringman("tr")
        print(languagemanager.get("hello"))
        >> Merhaba
        """
        self.language = language
        try:
            self.strings = json.load(open("etc/languages/"+language+".json"))
        except:
            print("Language file not found: etc/languages/"+language+".json")
            try:
                self.strings = json.load(open("etc/languages/en.json"))
            except:
                print("Language file not found: etc/languages/en.json")
                print("Failsafe failed. strings may show weird.")
                fail = True
        try:
            self.failsafeenglish = json.load(open("etc/languages/en.json"))
        except:
            print("Language file not found: etc/languages/en.json")
            print("Can't load failsafe language.")
            self.failsafeenglish = {}
    def get(self, string):
        """
        returns a string
        """
        try:
            return self.strings[string]
        except KeyError:
            try:
                return self.failsafeenglish[string]
            except KeyError:
                return string
    