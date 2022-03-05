from doctest import master
import json
import etc.confirmer as confirm
global profiles
#ayarlar şemasını okuyoruz
#config_schema.json dosyasının yolunu belirler
config_file='etc/config_schema.json'
with open (config_file) as f:
    config_schema=json.load(f)
"""
bilinen hatalar
* profil seçim menüsündeki isim güncellenmiyor
* yeni profil oluşmuyor
"""

import etc.stringManager
languageclass = etc.stringManager.stringman("en")
lanman = lambda stringcaller: languageclass.get(stringcaller)
def createprofile():
    profilecount = 1
    while True:
        try:
            settings["profile "+str(profilecount)]
            profilecount+=1
        except KeyError:
            break
        except Exception as e:
            raise Exception("unexpected expection: "+e)
    settings["profile "+str(profilecount)] = {}
    for key in list(config_schema.keys()):
        settings["profile "+str(profilecount)][key] = config_schema[key]['default']
    settings["profile "+str(profilecount)]["profile_name"] = "profile "+str(profilecount)
    return settings
try:
    with open ("etc/settings.json", "r+") as f:
        try:
            settings=json.load(f)
        except Exception as e:
            print("An error occured while loading settings.json", e)
            settings = {}
            settings = createprofile()
            f.write(json.dumps(settings))
except:
    print("settings.json dosyası bulunamadı. Oluşturuluyor.")
    settings = {}
    settings = createprofile()
    with open ("etc/settings.json", "w+") as f:
        f.write(json.dumps(settings))    
#Bazı çalışma ortamları tkinter desteklemiyor
try:
    from tkinter import ttk
    import tkinter
    GUI=True
except ImportError:
    GUI=False

config = {}
configlabel = {}
class configlegal:
    def __init__(self, button):
        self.configs = {}
        self.button = button
    def changestatus(self, key, status):
        self.configs[key] = status
        for item in self.configs.keys():
            if self.configs[item] == False:
                self.button.config(state=tkinter.DISABLED)
                return
        self.button.config(state=tkinter.ACTIVE)


if GUI:
    window = tkinter.Tk()
    window.title("Config")
    window.geometry("")
    window.resizable(False,False)
    window.configure(background='#f0f0f0')
    window.columnconfigure(0, weight=2)
    window.columnconfigure(1, weight=4)

    
    #config_schema içindeki keyleri liste halinde döndürür
    row, column, nl, loop= 0, 0, 0, 0
    
    settingslistwindow = tkinter.Frame(window, background='#f0f0f0')
    settingslistwindow.grid(row=0, column=0, sticky='nsew')
    keys=list(config_schema.keys())
    for key in keys:
        if config_schema[key]['type']=='bool':
            config[key] = tkinter.BooleanVar()
            configlabel[key] = ttk.Label(settingslistwindow, text=lanman(key), background='#f0f0f0')
            configlabel[key].grid(row=row, column=column, sticky='w')
            ttk.Checkbutton(settingslistwindow, variable=config[key]).grid(row=row, column=column+1, sticky='w')
            if config_schema[key]['default']==True:
                config[key].set(True)
        elif config_schema[key]['type']=='string':
            config[key] = tkinter.StringVar()
            configlabel[key] = ttk.Label(settingslistwindow, text=lanman(key), background='#f0f0f0')
            configlabel[key].grid(row=row, column=column, sticky='w')
            ttk.Entry(settingslistwindow, textvariable=config[key]).grid(row=row, column=column+1, sticky='w')
            if not config_schema[key]['default']==None:
                config[key].set(config_schema[key]['default'])
        elif config_schema[key]['type'].startswith("CONFIRM:"):
            config[key] = tkinter.StringVar()
            configlabel[key] = ttk.Label(settingslistwindow, text=lanman(key), background='#f0f0f0')
            configlabel[key].grid(row=row, column=column, sticky='w')
            widget = ttk.Entry(settingslistwindow, textvariable=config[key])
            widget.grid(row=row, column=column+1, sticky='w')
            confirmfile = config_schema[key]['type'].split(":")[1]
            confirmer=confirm.file(confirmfile)
            def intellientry(q,w,e, widget=widget, confirm=confirmer.confirm, masterkey=key):
                value = config[masterkey].get()
                if confirm(value):
                    configlabel[masterkey].config(background="green")
                    islegal.changestatus(masterkey, True)
                else:
                    configlabel[masterkey].config(background="red")
                    islegal.changestatus(masterkey, False)
            identity = confirm.stsave(intellientry)
            config[key].trace("w", confirm.stget(identity))

        nl+=1
        if nl==2 or loop == 0:
            loop+=1
            row+=1
            nl=0
            column=0
        else:
            column=2


    
    def loadprofile(event, _, __):
        for key in keys:
            config[key].set(settings[profile.get()][key])
            #update the window
            window.update()
    row+=1
    def allowsync(event, _, __):
        update_name.config(state='normal')
    def syncnames():
        """
        updates the profile names in the combobox
        """
        global profiles
        curkey = config["profile_name"].get()
        settingscache=settings[profile.get()]
        settingscache["profile_name"] = curkey
        settings.pop(profile.get())
        settings[curkey] = settingscache
        profile.set(curkey)
        config['profile_name'].set(curkey)
        updateprofilecombobox()
        

    def saveconfig():
        try:
            settings[profile.get()]
        except KeyError:
            settings[profile.get()] = {}
        for key in keys:
            settings[profile.get()][key] = config[key].get()
        with open ("etc/settings.json", "w") as f:
            json.dump(settings, f)
        profiles.append(profile.get())
        updateprofilecombobox()
    def deleteprofile(profilename = None):
        if profilename == None:
            if GUI:
                profilename = profile.get()
            else:
                raise Exception("can't figure out what to delete")
        
        try:
            del settings[profilename]
        except KeyError:
            pass
        with open ("etc/settings.json", "w") as f:
            json.dump(settings, f)
        if GUI:
            profiles.remove(profilename)
            settings.pop(profilename, None)
            if len(profiles) == 0:
                settings["profile 1"] = createprofile()
                profiles.append("profile 1")
            profile.set(profiles[0])
            loadprofile(None, None, None)
            profile.set(profiles[0])
            updateprofilecombobox()
    buttonframe = ttk.Frame(window)
    profileframe = ttk.Frame(window)
    #place them to the bottom
    buttonframe.grid(row=row, column=0, columnspan=2, sticky='se')
    profileframe.grid(row=row+1, column=0, columnspan=2, sticky='se')
    def updateprofilecombobox():
        global profiles
        profiles = []
        for item in settings.keys():
            profiles.append(settings[item]["profile_name"])
        profileselector["values"] = profiles
        return profiles

    ttk.Label(profileframe, text="Profiles", background='#f0f0f0').grid(row=row, column=column, sticky='w')
    profile = tkinter.StringVar()
    profiles = []
    profileselector = ttk.Combobox(profileframe, values=profiles, textvariable=profile, state="readonly", postcommand = updateprofilecombobox)
    profileselector.grid(row=row, column=column+1, sticky='e')
    #when the user selects a profile, the settings are loaded
    profile.trace('w', loadprofile)
    profiles = updateprofilecombobox()
        #change name button
    update_name = tkinter.Button(profileframe, text=lanman("update_name"), state=tkinter.DISABLED, command=syncnames)
    update_name.grid(row=row, column=column+2, sticky='w')
    profile.set(profiles[0])
    row+=1
    savebutton=ttk.Button(buttonframe, text=lanman("save"), command=saveconfig)
    savebutton.grid(row=row, column=column, sticky='e')
    islegal=configlegal(savebutton)
    ttk.Button(buttonframe, text=lanman("delete_profile"), command=deleteprofile).grid(row=row, column=column+1, sticky='e')
    ttk.Button(buttonframe, text=lanman("new_profile"), command=createprofile).grid(row=row, column=column+2, sticky='e')
    ttk.Button(buttonframe, text=lanman("close"), command=window.destroy).grid(row=row, column=column+3, sticky='e')
    config["profile_name"].trace('w', allowsync)
    window.mainloop()

else:
    import time
    print("This program is not compatible with your operating system.")
    print("Please use a Linux or Windows operating system.")
    print("Or it's probaby easiest to just edit etc/settings.json yourself.")
    def editprofile(total_profiles):
            print("Select a profile:")
            while True:
                try:
                    profile_number = int(input())
                    profile_name = total_profiles[profile_number-1]
                    break
                except Exception as e:
                    print("Invalid profile number.")
                    continue
            print("")
            print("Profile:", profile_name)
            print("")
            print("Settings:")
            for key in settings[profile_name].keys():
                print(key, ":", lanman(settings[profile_name][key]))
            print("")
            #select a setting to change
            while True:
                if input(lanman("change_value_?")) == any([lanman("no")[0], lanman("no"), "no"]):
                    break
                while True:
                    selection = 0

                    for item in list(settings[profile_name].keys()):
                        selection += 1
                        print(str(selection) + " ->  "+ lanman(item))
                    print ("")
                    while True:
                        selection = input(lanman("select_string_to_edit"))
                        try:
                            if not 0>=int(selection)<=len(settings[profile_name]):
                                break
                        except:
                            selection = "exit"
                            break
                    if selection == "exit":
                        break
                    if config_schema[list(settings[profile_name].keys())[int(selection)-1]]["type"] == "string":
                        newvalue=input(lanman("new_value"))
                    elif config_schema[settings[profile_name][selection]]["type"] == "bool":
                        while True:
                            newvalue=input(lanman("new_value_int"))
                            try:
                                int(newvalue)
                            except:
                                print(lanman("invalid_value_req_int"))
                    else:
                        print("this field is not editable in teminal")
                    settings[profile_name][list(settings[profile_name].keys())[int(selection)-1]] = newvalue
                    if profile_name != settings[profile_name]["profile_name"]:
                        settings[settings[profile_name]["profile_name"]] = {}
                    for item in settings[profile_name].keys():
                        settings[settings[profile_name]["profile_name"]][item] = settings[profile_name][item]
                    with open ("etc/settings.json", "w") as f:
                        json.dump(settings, f)
                print("")
                print("Done.")
                editloop()
    def editloop():
        total_profiles = []
        for item in settings.keys():
            total_profiles.append(settings[item]["profile_name"])
        while True:
            print("Profiles:")
            #print 1: profile name 2: profile name 3: profile name
            for i in range(len(total_profiles)):
                print(i+1, total_profiles[i])
            print("")
            print ("""
                    1 - %s
                    2 - %s
                    3 - %s
                    """ % (lanman("edit_profile"), lanman("new_profile"), lanman("delete_profile"),))
            action = input (lanman("action")+" ")
            if action == 1:
                editprofile(total_profiles)
            elif action == 2:
                createprofile()
            elif action == 3:
                while True:
                    todelete = input (lanman("select_to_delete")+" ")
                    try:
                        total_profiles[todelete-1]
                        break
                    except:
                        continue
                deleteprofile(total_profiles[todelete-1])
    editloop()
