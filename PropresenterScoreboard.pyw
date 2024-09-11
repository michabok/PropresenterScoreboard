"""
+++ Propresenter Scoreboard by Micha Bokelmann +++
---------------------

hi this is my testfeature

KNOWN ISSUES:

IDEAS:
- Leaderboard als Fenster öffnen (im counter)
- show-Buttons in #view verschieben
- Menu-Bar: Guide, Updates
- Right-Click to rename a Column on the Counter Page
- Freeze Counter Output

WIP:

EDIT FOR EVERY VERSION:
- About-Menu
- Export suggested Name
- data["software_version"] =  in exportPreset
+++ SEARCH FOR: +++
    - presetContent["software_version"] = "8.1.0"
    - heading = ctk.CTkLabel(innerFrame, text="Scoreboard 8.1.0", font=("Helvetica", 22, "bold"))
    - file = tk.filedialog.asksaveasfile(initialfile=presetContent["name"]+"_ScoreboardPreset_V8-1-0", defaultextension='.json', filetypes=[("json file", "*.json")])

"""
import customtkinter as ctk
import tkinter as tk
import sys
import os
import json
from CTkMenuBar import *
from tkinter import messagebox
import datetime
import socket

class MenuBarFrame(ctk.CTkFrame):
    def __init__(self, master, app_ref):
        super().__init__(master)

        self.app_ref = app_ref

        self.fileLabel = ctk.CTkButton(self, text="File", command=self.openFileSubmenu, width=34, height=24, fg_color="transparent", hover_color=("#36719f", "#144870"), text_color=("#333333", "#F7F7F7"), border_spacing=0, border_width=0)
        self.shortcutsLabel = ctk.CTkButton(self, text="Shortcuts",command=self.showShortcuts, width=68, height=24, fg_color="transparent", hover_color=("#36719f", "#144870"), text_color=("#333333", "#F7F7F7"), border_spacing=0, border_width=0)
        self.aboutLabel = ctk.CTkButton(self, text="About", command=self.showAbout, width=46, height=24, fg_color="transparent", hover_color=("#36719f", "#144870"), text_color=("#333333", "#F7F7F7"), border_spacing=0, border_width=0)
        self.fileLabel.grid(row=0, column=0, sticky="ne")
        self.shortcutsLabel.grid(row=0, column=1, sticky="ne")
        self.aboutLabel.grid(row=0, column=2, sticky="ne")
   
    def openFileSubmenu(self):
        self.fileSubmenu = tk.Menu(self, tearoff = 0) 
        self.fileSubmenu.add_command(label ="import Preset", command=self.importPreset) 
        self.fileSubmenu.add_command(label ="export Preset", command=self.openExportSubSubMenu)
        self.fileSubmenu.add_separator() 
        self.fileSubmenu.add_command(label ="quit app", command=self.quit) 

        self.fileSubmenu.tk_popup(app.winfo_x() + 13, app.winfo_y() + 65) 
    
    def openExportSubSubMenu(self):
        self.exportSubSubMenu = tk.Menu(self.app_ref, tearoff = 0) 
        
        with open(self.app_ref.SettingsFrame.SettingsScrollableFrame.settingsFilePath, 'r') as f:
            data = json.load(f)

        for i in range (len(data["presets"])):
            self.exportSubSubMenu.add_command(label=data["presets"][str(i)]["name"], command=lambda i=i: self.exportPreset(i))  # Use lambda to delay execution
 
        self.exportSubSubMenu.add_separator() 
        self.exportSubSubMenu.add_command(label ="cancel") 

        self.exportSubSubMenu.tk_popup(app.winfo_x() + 13, app.winfo_y() + 65) 

    def showShortcuts(self):
        self.app_ref.openShortcutsWindow(app_ref=self.app_ref)
    
    def showAbout(self):
        self.app_ref.openAboutWindow(app_ref=self.app_ref)
    
    def importPreset(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[("json file", "*.json")])
        file_name, file_extension = os.path.splitext(str(file_path))
        if file_path == "":
            return
        if(file_extension == ".json"):
            self.app_ref.SettingsFrame.SettingsScrollableFrame.createNewPresetFromJsonFileForImport(file_path)

    def exportPreset(self, id):
        with open(self.app_ref.SettingsFrame.SettingsScrollableFrame.settingsFilePath, 'r') as f:
            data = json.load(f)
        presetContent = data["presets"][str(id)]

        presetContent["software_version"] = "8.1.0"
        ct = datetime.datetime.now()
        presetContent["timestamp"] = str(ct.timestamp())
        presetContent["datetime"] = str(ct)
        presetContent["hostname"] = str(socket.gethostname())
        file = tk.filedialog.asksaveasfile(initialfile=presetContent["name"]+"_ScoreboardPreset_V8-1-0", defaultextension='.json', filetypes=[("json file", "*.json")])
        if file is None:
            return
        with open(file.name, 'w') as f:
            json.dump(presetContent, f, indent=4)

    def quit(self):
        self.app_ref.destroy()
        

class OuterFrameForSettings(ctk.CTkFrame):
    def __init__(self, master, app_ref):
        super().__init__(master)

        self.SettingsScrollableFrame = Settings(master=self, app_ref=app_ref)
        self.SettingsScrollableFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.rowconfigure((0), weight=1)
        self.columnconfigure(0, weight=1)

class Settings(ctk.CTkScrollableFrame):
    def __init__(self, master, app_ref):
        super().__init__(master)
        self.app_ref = app_ref

        self.settingsFilePath = os.path.join(self.app_ref.get_script_folder(),'config', 'Settings.json')
        self.names_Vars = []
        
        self.fixSettingsFileIfNeeded()
        
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        self.skipSettings_Var = ctk.StringVar(value=data["Settings"]["SkipSettings"])
        self.enableQuickRecall_Var = ctk.StringVar(value=data["Settings"]["EnableQuickRecall"])

        self.fillOptionsWhithFileValues(data["Settings"]["CallOnStartup_id"])
        self.createTabview()

        #create Widgets
            #basic tab
        self.createCulumnsOption()
        self.createAlwaysOnTopOption()
        self.createQuickRecallOtion()
            #advanced tab
        self.createResetShownOnlyOption()
        self.createHotkeysOption()
        self.createCustomRow1Option()
        self.createCustomRow2Option()
        self.createLockOption()
        self.createInvertLeaderboardOption()
        self.createDoFreezeLeaderboardOption()
        self.createShowFreezeButtonOption()
        self.createExcludeFromLeaderboardOption()
            #names-tab
        self.createNamesTab()
            #view-tab
        self.createHighlightOption()
        self.createSeparatorOption()
        self.createShowNamesOption()
        self.createShowLeadersOption()
            #design tab
        self.createColorModeOption()
        self.createMonochromeOption()
        self.createGeneralFontSizeOption()
        self.createNamesFontSizeOption()
            #presets tab
        self.createPresetsTab()
            #other-tab
        self.createSkipSettingsOption()
        self.createEnableQuickRecallOption()
        self.createWarningLabel()
            #go button
        self.createGoBtn()
        
        #configure
        self.configureSettingsFrame()
        self.runUpdateOptionCommands()

    def skipSettingsIfTrue(self):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)

        if data["Settings"]["SkipSettings"] == "on": 
            try:
                self.ReturnGo("")
            except:
                pass

        
    #json
    def fixSettingsFileIfNeeded(self):
        #create or correct Settings.json
        self.defaultSettingsContent = {
            "Settings": {
                "QuickRecall_id": "0",
                "CallOnStartup_id": "0",
                "SkipSettings": "off",
                "EnableQuickRecall": "off"
            },
            "presets": {
                "0": {
                    "name": "default",
                    "columns_Var": "",
                    "resetShownOnly_Var": "on",
                    "highlight_Var": "",
                    "separator_Var": "",
                    "showNames_Var": "off",
                    "showLeaders_Var": "off",
                    "colorMode_Var": "system",
                    "monochrom_Var": "off",
                    "generalFontSize_Var": "20",
                    "namesFontSize_Var": "general size",
                    "alwaysOnTop_Var": "off",
                    "hotkeys_Var": "on",
                    "customRow1_Type": "hide",
                    "customRow2_Type": "hide",
                    "customRow1Parameter_Var": "",
                    "customRow2Parameter_Var": "",
                    "lock_Var": "off",
                    "invertLeaderboard_Var": "off",
                    "doFreezeLeaderboard_Var": "off",
                    "showFreezeLeaderboard_Var": "off",
                    "excludeFromLeaderboard_Var": "",
                    "names_Vars": {
                        "A": "A",
                        "B": "B",
                        "C": "C",
                        "D": "D",
                        "E": "E",
                        "F": "F",
                        "G": "G",
                        "H": "H",
                        "I": "I",
                        "J": "J",
                        "K": "K",
                        "L": "L",
                        "M": "M",
                        "N": "N",
                        "O": "O",
                        "P": "P",
                        "Q": "Q",
                        "R": "R",
                        "S": "S",
                        "T": "T",
                        "U": "U",
                        "V": "V",
                        "W": "W",
                        "X": "X",
                        "Y": "Y",
                        "Z": "Z"
                    }
                }
            }
        }

        # Ensure the Settings.json file exists, if not, create it and ensure the file has no errors and the default-preset is correct 
        if not os.path.exists(self.settingsFilePath):
            with open(self.settingsFilePath, 'w') as f:
                json.dump(self.defaultSettingsContent, f, indent=4)
        else:
            with open(self.settingsFilePath, 'r') as f:
                try:
                    data = json.load(f)
                    if data["presets"]["0"] != self.defaultSettingsContent["presets"]["0"]:
                        data["presets"]["0"] = self.defaultSettingsContent["presets"]["0"]
                    if not(data["Settings"]["QuickRecall_id"] in data["presets"]):
                        data["Settings"]["QuickRecall_id"] = "0"
                    if not(data["Settings"]["CallOnStartup_id"] in data["presets"]):
                        data["Settings"]["CallOnStartup_id"] = "0"
                    if not(data["Settings"]["SkipSettings"] == "on" or data["Settings"]["SkipSettings"] == "off"):
                        data["Settings"]["SkipSettings"] = "off"
                    if not(data["Settings"]["EnableQuickRecall"] == "on" or data["Settings"]["EnableQuickRecall"] == "off"):
                        data["Settings"]["EnableQuickRecall"] = "off"
                    with open(self.settingsFilePath, 'w') as f:
                        json.dump(data, f, indent=4)
                except:
                    with open(self.settingsFilePath, 'w') as f:
                        json.dump(self.defaultSettingsContent, f, indent=4)

    def fillOptionsWhithFileValues(self, id):
        #read Settings.json
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        if id in data["presets"]:
            selPreset = data['presets'][id]
        else:
            selPreset = data['presets']["0"]

        #fill options with values from Settings.json
        try:
            self.columns_Var = ctk.StringVar(value=selPreset['columns_Var'])
            self.resetShownOnly_Var = ctk.StringVar(value=selPreset['resetShownOnly_Var'])
            self.highlight_Var = ctk.StringVar(value=selPreset['highlight_Var'])
            self.separator_Var = ctk.StringVar(value=selPreset['separator_Var'])
            self.showNames_Var = ctk.StringVar(value=selPreset['showNames_Var'])
            self.showLeaders_Var = ctk.StringVar(value=selPreset['showLeaders_Var'])
            self.colorMode_Var = ctk.StringVar(value=selPreset['colorMode_Var'])
            self.monochrom_Var = ctk.StringVar(value=selPreset['monochrom_Var'])
            self.generalFontSize_Var = ctk.StringVar(value=selPreset['generalFontSize_Var'])
            self.namesFontSize_Var = ctk.StringVar(value=selPreset['namesFontSize_Var'])
            self.alwaysOnTop_Var = ctk.StringVar(value=selPreset['alwaysOnTop_Var'])
            self.hotkeys_Var = ctk.StringVar(value=selPreset['hotkeys_Var'])
            self.customRow1_Type = ctk.StringVar(value=selPreset['customRow1_Type'])
            self.customRow2_Type = ctk.StringVar(value=selPreset['customRow2_Type'])
            self.customRow1Parameter_Var = ctk.StringVar(value=selPreset['customRow1Parameter_Var'])
            self.customRow2Parameter_Var = ctk.StringVar(value=selPreset['customRow2Parameter_Var'])
            self.lock_Var = ctk.StringVar(value=selPreset['lock_Var'])
            self.doFreezeLeaderboard_Var = ctk.StringVar(value=selPreset['doFreezeLeaderboard_Var'])
            self.showFreezeLeaderboard_Var = ctk.StringVar(value=selPreset['showFreezeLeaderboard_Var'])
            self.excludeFromLeaderboard_Var = ctk.StringVar(value=selPreset['excludeFromLeaderboard_Var'])
            self.invertLeaderboard_Var = ctk.StringVar(value=selPreset['invertLeaderboard_Var'])
            for i in range (26):
               try:
                self.names_Vars[i] = (ctk.StringVar(value=selPreset['names_Vars'][str(chr(ord('A') + i))]))
               except:
                self.names_Vars.append(ctk.StringVar(value=selPreset['names_Vars'][str(chr(ord('A') + i))]))
            
        except:
            self.app_ref.open_errorWindow(app_ref = self.app_ref, msg="An error occurred.\nYou can try to reset all Settings.", type=0)


        self.activePreset = str(id)

    #name-files
    def saveNameToFile(self, column):
        name = self.names_Vars[column].get()
        script_dir = self.app_ref.get_script_folder()
        column_FilePath = os.path.join(script_dir, "names", "name-{}.txt".format(chr(ord('A') + column)))
        with open(column_FilePath, "w") as file:
            file.write(name)
    
    def saveAllNames(self):
        for i in range (26):
            self.saveNameToFile(i)
    
    #presets
    def createNewPreset(self):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
            
        new_preset = {
            "name": "New Preset",
            "columns_Var": self.columns_Var.get(),
            "resetShownOnly_Var": self.resetShownOnly_Var.get(),
            "highlight_Var": self.highlight_Var.get(),
            "separator_Var": self.separator_Var.get(),
            "showNames_Var": self.showNames_Var.get(),
            "showLeaders_Var": self.showLeaders_Var.get(),
            "colorMode_Var": self.colorMode_Var.get(),
            "monochrom_Var": self.monochrom_Var.get(),
            "generalFontSize_Var": self.generalFontSize_Var.get(),
            "namesFontSize_Var": self.namesFontSize_Var.get(),
            "alwaysOnTop_Var": self.alwaysOnTop_Var.get(),
            "hotkeys_Var": self.hotkeys_Var.get(),
            "customRow1_Type": self.customRow1_Type.get(),
            "customRow2_Type": self.customRow2_Type.get(),
            "customRow1Parameter_Var": self.customRow1Parameter_Var.get(),
            "customRow2Parameter_Var": self.customRow2Parameter_Var.get(),
            "lock_Var": self.lock_Var.get(),
            "doFreezeLeaderboard_Var": self.doFreezeLeaderboard_Var.get(),
            "showFreezeLeaderboard_Var": self.showFreezeLeaderboard_Var.get(),
            "excludeFromLeaderboard_Var": self.excludeFromLeaderboard_Var.get(),
            "invertLeaderboard_Var": self.invertLeaderboard_Var.get(),
            "names_Vars": {
                "A": self.names_Vars[0].get(),
                "B": self.names_Vars[1].get(),
                "C": self.names_Vars[2].get(),
                "D": self.names_Vars[3].get(),
                "E": self.names_Vars[4].get(),
                "F": self.names_Vars[5].get(),
                "G": self.names_Vars[6].get(),
                "H": self.names_Vars[7].get(),
                "I": self.names_Vars[8].get(),
                "J": self.names_Vars[9].get(),
                "K": self.names_Vars[10].get(),
                "L": self.names_Vars[11].get(),
                "M": self.names_Vars[12].get(),
                "N": self.names_Vars[13].get(),
                "O": self.names_Vars[14].get(),
                "P": self.names_Vars[15].get(),
                "Q": self.names_Vars[16].get(),
                "R": self.names_Vars[17].get(),
                "S": self.names_Vars[18].get(),
                "T": self.names_Vars[19].get(),
                "U": self.names_Vars[20].get(),
                "V": self.names_Vars[21].get(),
                "W": self.names_Vars[22].get(),
                "X": self.names_Vars[23].get(),
                "Y": self.names_Vars[24].get(),
                "Z": self.names_Vars[25].get()
            }
        }
        id = max(map(int, data["presets"].keys()), default=-1) + 1

        data["presets"][str(id)] = new_preset

        with open(self.settingsFilePath, 'w') as f:
            json.dump(data, f, indent=4)
        self.presetsTab_addRow(id)

        self.activePreset = str(id)
        self.showOrHideQuickRecall()
    
    def createNewPresetFromJsonFileForImport(self, file_path):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)

        with open(file_path, 'r') as f:
            presetFile = json.load(f)

        try:  
            new_preset = {
                "name": presetFile["name"],
                "columns_Var": presetFile['columns_Var'],
                "resetShownOnly_Var": presetFile['resetShownOnly_Var'],
                "highlight_Var": presetFile['highlight_Var'],
                "separator_Var": presetFile['separator_Var'],
                "showNames_Var": presetFile['showNames_Var'],
                "showLeaders_Var": presetFile['showLeaders_Var'],
                "colorMode_Var": presetFile['colorMode_Var'],
                "monochrom_Var": presetFile['monochrom_Var'],
                "generalFontSize_Var": presetFile['generalFontSize_Var'],
                "namesFontSize_Var": presetFile['namesFontSize_Var'],
                "alwaysOnTop_Var": presetFile['alwaysOnTop_Var'],
                "hotkeys_Var": presetFile['hotkeys_Var'],
                "customRow1_Type": presetFile['customRow1_Type'],
                "customRow2_Type": presetFile['customRow2_Type'],
                "customRow1Parameter_Var": presetFile['customRow1Parameter_Var'],
                "customRow2Parameter_Var": presetFile['customRow2Parameter_Var'],
                "lock_Var": presetFile['lock_Var'],
                "doFreezeLeaderboard_Var": presetFile['doFreezeLeaderboard_Var'],
                "showFreezeLeaderboard_Var": presetFile['showFreezeLeaderboard_Var'],
                "excludeFromLeaderboard_Var": presetFile['excludeFromLeaderboard_Var'],
                "invertLeaderboard_Var": presetFile['invertLeaderboard_Var'],
                "names_Vars": {
                    "A": presetFile['names_Vars']['A'],
                    "B": presetFile['names_Vars']['B'],
                    "C": presetFile['names_Vars']['C'],
                    "D": presetFile['names_Vars']['D'],
                    "E": presetFile['names_Vars']['E'],
                    "F": presetFile['names_Vars']['F'],
                    "G": presetFile['names_Vars']['G'],
                    "H": presetFile['names_Vars']['H'],
                    "I": presetFile['names_Vars']['I'],
                    "J": presetFile['names_Vars']['J'],
                    "K": presetFile['names_Vars']['K'],
                    "L": presetFile['names_Vars']['L'],
                    "M": presetFile['names_Vars']['M'],
                    "N": presetFile['names_Vars']['N'],
                    "O": presetFile['names_Vars']['O'],
                    "P": presetFile['names_Vars']['P'],
                    "Q": presetFile['names_Vars']['Q'],
                    "R": presetFile['names_Vars']['R'],
                    "S": presetFile['names_Vars']['S'],
                    "T": presetFile['names_Vars']['T'],
                    "U": presetFile['names_Vars']['U'],
                    "V": presetFile['names_Vars']['V'],
                    "W": presetFile['names_Vars']['W'],
                    "X": presetFile['names_Vars']['X'],
                    "Y": presetFile['names_Vars']['Y'],
                    "Z": presetFile['names_Vars']['Z']
                }
            }
        
        except:
            self.app_ref.open_errorWindow(app_ref = self.app_ref, msg="An error occurred.\nThe file might be corrupted or\nfrom an older software version.", type=1)

        id = max(map(int, data["presets"].keys()), default=-1) + 1

        data["presets"][str(id)] = new_preset

        with open(self.settingsFilePath, 'w') as f:
            json.dump(data, f, indent=4)
        self.presetsTab_addRow(id)

    def loadPreset(self, id):
        self.fillOptionsWhithFileValues(str(id))
        self.updateOptionVisibility()
        self.runUpdateOptionCommands()
        self.showOrHideQuickRecall()
        self.disableAndEndblaRecallButtons()
        self.traceEntryBoxes()
    
    def disableAndEndblaRecallButtons(self):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        for i in range (len(data["presets"])):
            if list(data["presets"].keys())[i] == self.activePreset:
                self.presetLoad_Buttons[i].configure(state="disabled")
            else:
                self.presetLoad_Buttons[i].configure(state="normal")

    def showOrHideQuickRecall(self):        
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        if str(self.activePreset) == data["Settings"]["QuickRecall_id"] or data["Settings"]["EnableQuickRecall"] == "off":
            try:
                self.quickRecall_Label.grid_forget()
                self.quickRecall_Button.grid_forget()
            except:
                pass
        else:
            self.quickRecall_Label.grid(row=2, column=0, sticky="e", pady=5)
            self.quickRecall_Button.grid(row=2, column=1, sticky="w", padx=10, pady=5)

    def saveExistingPreset(self, id):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)

        new_preset = {
            "name": data["presets"][str(id)]["name"],
            "columns_Var": self.columns_Var.get(),
            "resetShownOnly_Var": self.resetShownOnly_Var.get(),
            "highlight_Var": self.highlight_Var.get(),
            "separator_Var": self.separator_Var.get(),
            "showNames_Var": self.showNames_Var.get(),
            "showLeaders_Var": self.showLeaders_Var.get(),
            "colorMode_Var": self.colorMode_Var.get(),
            "monochrom_Var": self.monochrom_Var.get(),
            "generalFontSize_Var": self.generalFontSize_Var.get(),
            "namesFontSize_Var": self.namesFontSize_Var.get(),
            "alwaysOnTop_Var": self.alwaysOnTop_Var.get(),
            "hotkeys_Var": self.hotkeys_Var.get(),
            "customRow1_Type": self.customRow1_Type.get(),
            "customRow2_Type": self.customRow2_Type.get(),
            "customRow1Parameter_Var": self.customRow1Parameter_Var.get(),
            "customRow2Parameter_Var": self.customRow2Parameter_Var.get(),
            "lock_Var": self.lock_Var.get(),
            "doFreezeLeaderboard_Var": self.doFreezeLeaderboard_Var.get(),
            "showFreezeLeaderboard_Var": self.showFreezeLeaderboard_Var.get(),
            "excludeFromLeaderboard_Var": self.excludeFromLeaderboard_Var.get(),
            "invertLeaderboard_Var": self.invertLeaderboard_Var.get(),
            "names_Vars": {
                "A": self.names_Vars[0].get(),
                "B": self.names_Vars[1].get(),
                "C": self.names_Vars[2].get(),
                "D": self.names_Vars[3].get(),
                "E": self.names_Vars[4].get(),
                "F": self.names_Vars[5].get(),
                "G": self.names_Vars[6].get(),
                "H": self.names_Vars[7].get(),
                "I": self.names_Vars[8].get(),
                "J": self.names_Vars[9].get(),
                "K": self.names_Vars[10].get(),
                "L": self.names_Vars[11].get(),
                "M": self.names_Vars[12].get(),
                "N": self.names_Vars[13].get(),
                "O": self.names_Vars[14].get(),
                "P": self.names_Vars[15].get(),
                "Q": self.names_Vars[16].get(),
                "R": self.names_Vars[17].get(),
                "S": self.names_Vars[18].get(),
                "T": self.names_Vars[19].get(),
                "U": self.names_Vars[20].get(),
                "V": self.names_Vars[21].get(),
                "W": self.names_Vars[22].get(),
                "X": self.names_Vars[23].get(),
                "Y": self.names_Vars[24].get(),
                "Z": self.names_Vars[25].get()
            }
        }

        data["presets"][str(id)] = new_preset

        with open(self.settingsFilePath, 'w') as f:
            json.dump(data, f, indent=4)
        
        self.activePreset = str(id)
        self.showOrHideQuickRecall()

    def setPresetName(self, id, newName):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        
        data["presets"][str(id)]["name"] = newName

        with open(self.settingsFilePath, 'w') as f:
            json.dump(data, f, indent=4)

    def deletePreset(self, id):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        
        del data["presets"][str(id)]
           
        with open(self.settingsFilePath, 'w') as f:
            json.dump(data, f, indent=4)   

        if data["Settings"]["QuickRecall_id"] == str(id): 
            self.presetQuickRecall_RadioButtons[0].select()
            self.presetQuickRecallAction(0)
        if data["Settings"]["CallOnStartup_id"] == str(id): 
            self.presetStartUp_RadioButtons[0].select()
            self.presetStartUpAction(0)

    #Layout and config
    def createTabview(self):
        self.tabview = ctk.CTkTabview(master=self, height=100, anchor="n", border_color="#4a4a4a", border_width=1)
        self.tabview.add("Basic")
        self.tabview.add("Advanced")
        self.tabview.add("Names")
        self.tabview.add("View")
        self.tabview.add("Design")
        self.tabview.add("Presets")
        self.tabview.add("Other")
        self.tabview.tab("Basic").columnconfigure((0,1), weight=1)
        self.tabview.tab("Advanced").columnconfigure((0,1), weight=1)
        self.tabview.tab("Names").columnconfigure((1), weight=1)
        self.tabview.tab("View").columnconfigure((0,1), weight=1)
        self.tabview.tab("Design").columnconfigure((0,1), weight=1)
        self.tabview.tab("Presets").columnconfigure((0,1,2,3,4,5), weight=1)
        self.tabview.tab("Other").columnconfigure((0,1), weight=1)
        self.tabview.grid(row=0, column=0, sticky="e", pady=0, padx=0)
    
    def configureSettingsFrame(self):
        #configure
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.configure(fg_color=("gray95", "gray10"))

        #trace and bind for Go-Action
        self.traceEntryBoxes()
        self.bindEntryBoxes()

        self.columns_Entry.focus_set()
    
    def traceEntryBoxes(self):
        self.columns_Var.trace('w', self.validateGoBtn)
        self.customRow1Parameter_Var.trace('w', self.validateGoBtn)
        self.customRow2Parameter_Var.trace('w', self.validateGoBtn)
    
    def bindEntryBoxes(self): #only return bindings
        self.columns_Entry.bind("<Return>", self.ReturnGo)
        self.columns_Entry.bind("<Control-Return>", self.ReturnGo)
        self.highlight_Entry.bind("<Return>", self.ReturnGo)
        self.highlight_Entry.bind("<Control-Return>", self.ReturnGo)
        self.separator_Entry.bind("<Return>", self.ReturnGo)
        self.separator_Entry.bind("<Control-Return>", self.ReturnGo)
        self.customRow1Parameter_Entry.bind("<Return>", self.ReturnGo)
        self.customRow1Parameter_Entry.bind("<Control-Return>", self.ReturnGo)
        self.customRow2Parameter_Entry.bind("<Return>", self.ReturnGo)
        self.customRow2Parameter_Entry.bind("<Control-Return>", self.ReturnGo)
        self.excludeFromLeaderboard_Entry.bind("<Return>", self.ReturnGo)
        self.excludeFromLeaderboard_Entry.bind("<Control-Return>", self.ReturnGo)
        for i in range (26):
            self.names_entryFields[i].bind("<Control-Return>", self.ReturnGo)


    def runUpdateOptionCommands(self):
        self.updateAlwaysOnTop()
        self.updateCustomRow1(self.customRow1_Type.get())
        self.updateCustomRow2(self.customRow2_Type.get())
        self.updateColorMode(self.colorMode_Var.get())
        self.updateMonochromatic()
    
    def updateOptionVisibility(self):
        self.columns_Entry.configure(textvariable=self.columns_Var)
        self.resetShownOnly_Switch.configure(variable=self.resetShownOnly_Var)
        self.highlight_Entry.configure(textvariable=self.highlight_Var)
        self.separator_Entry.configure(textvariable=self.separator_Var)
        self.showNames_Switch.configure(variable=self.showNames_Var)
        self.showLeaders_Switch.configure(variable=self.showLeaders_Var)
        self.colorMode_OptionMenu.configure(variable=self.colorMode_Var)
        self.monochromatic_Switch.configure(variable=self.monochrom_Var)
        self.generalFontSize_OptionMenu.configure(variable=self.generalFontSize_Var)
        self.namesFontSize_OptionMenu.configure(variable=self.namesFontSize_Var)
        self.alwaysOnTop_Switch.configure(variable=self.alwaysOnTop_Var)
        self.hotkeys_Switch.configure(variable=self.hotkeys_Var)
        self.customRow1_OptionMenu.configure(variable=self.customRow1_Type)
        self.customRow2_OptionMenu.configure(variable=self.customRow2_Type)
        self.customRow1Parameter_Entry.configure(textvariable=self.customRow1Parameter_Var)
        self.customRow2Parameter_Entry.configure(textvariable=self.customRow2Parameter_Var)
        self.lock_Switch.configure(variable=self.lock_Var)
        self.invertLeaderboard_Switch.configure(variable=self.invertLeaderboard_Var)
        self.doFreezeLeaderboard_Switch.configure(variable=self.doFreezeLeaderboard_Var)
        self.showFreezeLeaderboard_Switch.configure(variable=self.showFreezeLeaderboard_Var)
        self.excludeFromLeaderboard_Entry.configure(textvariable=self.excludeFromLeaderboard_Var)
        for i in range (26):
            self.names_entryFields[i].configure(textvariable=self.names_Vars[i])

    def removeActivePresetValue(self):
        self.activePreset = ""
        self.showOrHideQuickRecall()
        self.disableAndEndblaRecallButtons()

#---CREATE OPTIONS---
    #basic-tab
    def createCulumnsOption(self):
        self.columns_Label = ctk.CTkLabel(self.tabview.tab("Basic"), text="Number of columns", font=("Helvetica", 16, "bold"))
        self.columns_Label.grid(row=0, column=0, sticky="e", pady=5)
        
        self.columns_Entry = ctk.CTkEntry(self.tabview.tab("Basic"), textvariable=self.columns_Var, width=100, font=("Helvetica", 14, "bold"))
        self.columns_Entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.columns_Entry.bind("<Key>", lambda event: self.removeActivePresetValue())

    def createAlwaysOnTopOption(self):
        self.alwaysOnTop_Label = ctk.CTkLabel(self.tabview.tab("Basic"), text="Always on top", font=("Helvetica", 16, "bold"))
        self.alwaysOnTop_Label.grid(row=1, column=0, sticky="e", pady=5)
        
        self.alwaysOnTop_Switch = ctk.CTkSwitch(self.tabview.tab("Basic"), command=self.updateAlwaysOnTop, variable=self.alwaysOnTop_Var, text="", onvalue="on", offvalue="off", width=100)
        self.alwaysOnTop_Switch.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.alwaysOnTop_Switch.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())

    def createQuickRecallOtion(self):
        self.quickRecall_Label = ctk.CTkLabel(self.tabview.tab("Basic"), text="Quick Recall Preset", font=("Helvetica", 16, "bold"))

        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        id = data["Settings"]["QuickRecall_id"]
        name = data["presets"][id]["name"]
        self.quickRecall_Button = ctk.CTkButton(self.tabview.tab("Basic"), command=lambda id=id: self.loadPreset(id), text=name, state="normal", font=("Helvetica", 16, "bold"))
        
        self.showOrHideQuickRecall()

    #advanced-tab
    def createResetShownOnlyOption(self):
        self.resetShownOnly_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="Only reset shown", font=("Helvetica", 16, "bold"))
        self.resetShownOnly_Label.grid(row=0, column=0, sticky="e", pady=5)
        
        self.resetShownOnly_Switch = ctk.CTkSwitch(self.tabview.tab("Advanced"), text="", variable=self.resetShownOnly_Var, onvalue="on", offvalue="off")
        self.resetShownOnly_Switch.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.resetShownOnly_Switch.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())

    def createHotkeysOption(self):
        self.hotkeys_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="Hotkeys", font=("Helvetica", 16, "bold"))
        self.hotkeys_Label.grid(row=1, column=0, sticky="e", pady=5)
        
        self.hotkeys_Switch = ctk.CTkSwitch(self.tabview.tab("Advanced"), variable=self.hotkeys_Var, text="", onvalue="on", offvalue="off", width=100)
        self.hotkeys_Switch.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.hotkeys_Switch.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())

    def createCustomRow1Option(self):
        self.customRow1_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="Custom row 1", font=("Helvetica", 16, "bold"))
        self.customRow1_Label.grid(row=2, column=0, sticky="e", pady=5)
        
        self.customRow1_OptionMenu = ctk.CTkOptionMenu(self.tabview.tab("Advanced"), variable=self.customRow1_Type, command=self.updateCustomRow1, values=["hide", "+10", "-10", "+ custom", "add entry", "set entry", "reset"], width=100, font=("Helvetica", 14, "bold"))
        self.customRow1_OptionMenu.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        self.customRow1Parameter_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="custom parameter 1", font=("Helvetica", 16, "bold"))
        if self.customRow1_Type.get() == "+ custom":
            self.customRow1Parameter_Label.grid(row=3, column=0, sticky="e", pady=5)
        
        self.customRow1Parameter_Entry = ctk.CTkEntry(self.tabview.tab("Advanced"), textvariable=self.customRow1Parameter_Var, width=100, font=("Helvetica", 14, "bold"))
        if self.customRow1_Type.get() == "+ custom":
            self.customRow1Parameter_Entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
            self.customRow1Parameter_Entry.configure(state="normal")
        else:
            self.customRow1Parameter_Entry.configure(state="readonly")
        self.customRow1_OptionMenu.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())

    def createCustomRow2Option(self):
        self.customRow2_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="Custom row 2", font=("Helvetica", 16, "bold"))
        self.customRow2_Label.grid(row=4, column=0, sticky="e", pady=5)
        
        self.customRow2_OptionMenu = ctk.CTkOptionMenu(self.tabview.tab("Advanced"), variable=self.customRow2_Type, command=self.updateCustomRow2, values=["hide", "+10", "-10", "+ custom", "add entry", "set entry", "reset"], width=100, font=("Helvetica", 14, "bold"))
        self.customRow2_OptionMenu.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        
        self.customRow2Parameter_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="custom parameter 2", font=("Helvetica", 16, "bold"))
        if self.customRow2_Type.get() == "+ custom":
            self.customRow2Parameter_Label.grid(row=5, column=0, sticky="e", pady=5)

        self.customRow2Parameter_Entry = ctk.CTkEntry(self.tabview.tab("Advanced"), textvariable=self.customRow2Parameter_Var, width=100, font=("Helvetica", 14, "bold"))
        if self.customRow2_Type.get() == "+ custom":
            self.customRow2Parameter_Entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)
            self.customRow2Parameter_Entry.configure(state="normal")
        else:
            self.customRow2Parameter_Entry.configure(state="readonly")
        self.customRow2_OptionMenu.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())

    def createLockOption(self):
        self.Lock_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="enable Lock", font=("Helvetica", 16, "bold"))
        self.Lock_Label.grid(row=6, column=0, sticky="e", pady=5)

        self.lock_Switch = ctk.CTkSwitch(self.tabview.tab("Advanced"), variable=self.lock_Var, text="", onvalue="on", offvalue="off", width=100)
        self.lock_Switch.grid(row=6, column=1, sticky="w", padx=10, pady=5)
        self.lock_Switch.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())
    
    def createInvertLeaderboardOption(self):
        self.invertLeaderboard_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="invert Leaderboard", font=("Helvetica", 16, "bold"))
        self.invertLeaderboard_Label.grid(row=7, column=0, sticky="e", pady=5)

        self.invertLeaderboard_Switch = ctk.CTkSwitch(self.tabview.tab("Advanced"), variable=self.invertLeaderboard_Var, text="", onvalue="on", offvalue="off", width=100)
        self.invertLeaderboard_Switch.grid(row=7, column=1, sticky="w", padx=10, pady=5)
        self.invertLeaderboard_Switch.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())

    def createDoFreezeLeaderboardOption(self):
        self.doFreezeLeaderboard_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="freeze Leaderboard", font=("Helvetica", 16, "bold"))
        self.doFreezeLeaderboard_Label.grid(row=8, column=0, sticky="e", pady=5)

        self.doFreezeLeaderboard_Switch = ctk.CTkSwitch(self.tabview.tab("Advanced"), variable=self.doFreezeLeaderboard_Var, text="", onvalue="on", offvalue="off", width=100)
        self.doFreezeLeaderboard_Switch.grid(row=8, column=1, sticky="w", padx=10, pady=5)
        self.doFreezeLeaderboard_Switch.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())

    def createShowFreezeButtonOption(self):
        self.showFreezeLeaderboard_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="show freeze button", font=("Helvetica", 16, "bold"))
        self.showFreezeLeaderboard_Label.grid(row=9, column=0, sticky="e", pady=5)

        self.showFreezeLeaderboard_Switch = ctk.CTkSwitch(self.tabview.tab("Advanced"), variable=self.showFreezeLeaderboard_Var, text="", onvalue="on", offvalue="off", width=100)
        self.showFreezeLeaderboard_Switch.grid(row=9, column=1, sticky="w", padx=10, pady=5)
        self.showFreezeLeaderboard_Switch.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())
    
    def createExcludeFromLeaderboardOption(self):
        self.excludeFromLeaderboard_Label = ctk.CTkLabel(self.tabview.tab("Advanced"), text="exclude from leaderboard", font=("Helvetica", 16, "bold"))
        self.excludeFromLeaderboard_Label.grid(row=10, column=0, sticky="e", pady=5)

        self.excludeFromLeaderboard_Entry = ctk.CTkEntry(self.tabview.tab("Advanced"), textvariable=self.excludeFromLeaderboard_Var, width=100, font=("Helvetica", 14, "bold"))
        self.excludeFromLeaderboard_Entry.grid(row=10, column=1, sticky="w", padx=10, pady=5)
        self.excludeFromLeaderboard_Entry.bind("<Key>", lambda event: self.removeActivePresetValue())

    
    #names-Tab
    def createNamesTab(self):
        self.names_labels = []
        self.names_entryFields = []

        self.namesNotice_label = ctk.CTkLabel(self.tabview.tab("Names"), text="Press <Enter> inside a text field to save the value in the\ncorresponding names-File. The names for the leaderboard\nwill automatically be updated after pressing the 'Go'-Button.", font=("Helvetica", 12, "bold"))
        self.namesNotice_label.grid(row=0, column=0, columnspan=2)

        self.safeAllNames_Button = ctk.CTkButton(self.tabview.tab("Names"), command=self.saveAllNames, text="save all Names", font=("Helvetiva", 14, "bold"))
        self.safeAllNames_Button.grid(row=1, column=0, sticky="ew", padx=10, pady=7, columnspan=2)

        for i in range (26):
            self.names_labels.append(ctk.CTkLabel(self.tabview.tab("Names"), text=chr(ord('A') + i), width=100, font=("Helvetiva", 14, "bold"), fg_color="#1a1a1a", corner_radius=5))
            self.names_labels[i].grid(row=i+2, column=0, sticky="ew", padx=10, pady=3)

            self.names_entryFields.append(ctk.CTkEntry(self.tabview.tab("Names"),  textvariable=self.names_Vars[i], font=("Helvetica", 14, "bold")))
            self.names_entryFields[i].grid(row=i+2, column=1, sticky="ew", padx=10, pady=3)
            self.names_entryFields[i].bind("<Key>", lambda event: self.removeActivePresetValue())
            self.names_entryFields[i].bind("<Return>", lambda event, column=i: self.saveNameToFile(column))

        self.rowconfigure

    #view-tab
    def createHighlightOption(self):
        self.highlight_Label = ctk.CTkLabel(self.tabview.tab("View"), text="Highlighted Columns", font=("Helvetica", 16, "bold"))
        self.highlight_Label.grid(row=0, column=0, sticky="e", pady=5)
        self.highlight_Entry = ctk.CTkEntry(self.tabview.tab("View"), textvariable=self.highlight_Var, width=100, font=("Helvetica", 14, "bold"))

        self.highlight_Entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.highlight_Entry.bind("<Key>", lambda event: self.removeActivePresetValue())

    def createSeparatorOption(self):
        self.separator_Label = ctk.CTkLabel(self.tabview.tab("View"), text="separator after", font=("Helvetica", 16, "bold"))
        self.separator_Label.grid(row=1, column=0, sticky="e", pady=5)

        self.separator_Entry = ctk.CTkEntry(self.tabview.tab("View"), textvariable=self.separator_Var, width=100, font=("Helvetica", 14, "bold"))
        self.separator_Entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.separator_Entry.bind("<Key>", lambda event: self.removeActivePresetValue())

    def createShowNamesOption(self):
        self.showNames_Label = ctk.CTkLabel(self.tabview.tab("View"), text="show Names", font=("Helvetica", 16, "bold"))
        self.showNames_Label.grid(row=2, column=0, sticky="e", pady=5)

        self.showNames_Switch = ctk.CTkSwitch(self.tabview.tab("View"), variable=self.showNames_Var, text="", onvalue="on", offvalue="off", width=100)
        self.showNames_Switch.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.showNames_Switch.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())
    
    def createShowLeadersOption(self):
        self.showLeaders_Label = ctk.CTkLabel(self.tabview.tab("View"), text="show Leaders", font=("Helvetica", 16, "bold"))
        self.showLeaders_Label.grid(row=3, column=0, sticky="e", pady=5)

        self.showLeaders_Switch = ctk.CTkSwitch(self.tabview.tab("View"), variable=self.showLeaders_Var, text="", onvalue="on", offvalue="off", width=100)
        self.showLeaders_Switch.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        self.showLeaders_Switch.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())

    #design-tab
    def createColorModeOption(self):
        self.colorMode_Label = ctk.CTkLabel(self.tabview.tab("Design"), text="Color mode", font=("Helvetica", 16, "bold"))
        self.colorMode_Label.grid(row=0, column=0, sticky="e", pady=5)
        
        self.colorMode_OptionMenu = ctk.CTkOptionMenu(self.tabview.tab("Design"), variable=self.colorMode_Var, command=self.updateColorMode, values=["system", "dark", "light"], width=100, font=("Helvetica", 14, "bold"))
        self.colorMode_OptionMenu.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.colorMode_OptionMenu.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())

    def createMonochromeOption(self):
        self.monochromatic_Label = ctk.CTkLabel(self.tabview.tab("Design"), text="Monochrome", font=("Helvetica", 16, "bold"))
        self.monochromatic_Label.grid(row=1, column=0, sticky="e", pady=5)
        
        self.monochromatic_Switch = ctk.CTkSwitch(self.tabview.tab("Design"), command=self.updateMonochromatic, variable=self.monochrom_Var, text="", onvalue="on", offvalue="off", width=100)
        self.monochromatic_Switch.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.monochromatic_Switch.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())
    
    def createGeneralFontSizeOption(self):
        self.generalFontSize_Label = ctk.CTkLabel(self.tabview.tab("Design"), text="general font size", font=("Helvetica", 16, "bold"))
        self.generalFontSize_Label.grid(row=2, column=0, sticky="e", pady=5)
        
        self.generalFontSize_OptionMenu = ctk.CTkOptionMenu(self.tabview.tab("Design"), variable=self.generalFontSize_Var, values=["10", "12", "14", "16", "18", "20", "24", "28", "32", "36", "48"], width=100, font=("Helvetica", 14, "bold"))
        self.generalFontSize_OptionMenu.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.generalFontSize_OptionMenu.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())

    def createNamesFontSizeOption(self):
        self.namesFontSize_Label = ctk.CTkLabel(self.tabview.tab("Design"), text="names font size", font=("Helvetica", 16, "bold"))
        self.namesFontSize_Label.grid(row=3, column=0, sticky="e", pady=5)

        self.namesFontSize_OptionMenu = ctk.CTkOptionMenu(self.tabview.tab("Design"), variable=self.namesFontSize_Var, values=["general size", "10", "12", "14", "16", "18", "20", "24", "28", "32", "36", "48"], width=100, font=("Helvetica", 14, "bold"))
        self.namesFontSize_OptionMenu.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        self.namesFontSize_OptionMenu.bind("<ButtonRelease-1>", lambda event: self.removeActivePresetValue())


    #preset-tab
    def createPresetsTab(self):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)

        self.presetName_Var = []
        self.presetName_Entrys = []
        self.presetLoad_Buttons = []
        self.presetStore_Buttons = []
        self.presetQuickRecall_RadioButtons = []
        self.presetStartUp_RadioButtons = []
        self.presetDelete_Buttons = []

        self.presetQuickRecall_RadioVar = ctk.IntVar(value=0)
        self.presetStartup_RadioVar = ctk.IntVar(value=0)

        for i in range (len(data["presets"])):
            id = list(data["presets"].keys())[i]
            self.presetName_Var.append(ctk.StringVar(value=data["presets"][str(id)]["name"]))
            self.presetName_Entrys.append(ctk.CTkEntry(self.tabview.tab("Presets"), textvariable=self.presetName_Var[i], font=("Helvetica", 14, "bold")))
            self.presetName_Entrys[i].bind('<KeyRelease>', lambda event, id=id, index=i: self.presetNameEntryAction(event, id, index))
            self.presetLoad_Buttons.append(ctk.CTkButton(self.tabview.tab("Presets"), command=lambda id=id: self.loadPreset(id), text="recall", width=110, font=("Helvetiva", 14, "bold")))
            self.presetStore_Buttons.append(ctk.CTkButton(self.tabview.tab("Presets"), command=lambda id=id: self.saveExistingPreset(id), text="store", width=110, font=("Helvetiva", 14, "bold")))
            self.presetQuickRecall_RadioButtons.append(ctk.CTkRadioButton(self.tabview.tab("Presets"), command=lambda id=id: self.presetQuickRecallAction(id), variable=self.presetQuickRecall_RadioVar, value=id, text="", font=("Helvetiva", 14, "bold")))
            self.presetStartUp_RadioButtons.append(ctk.CTkRadioButton(self.tabview.tab("Presets"), command=lambda id=id: self.presetStartUpAction(id), variable=self.presetStartup_RadioVar, value=id, text="", font=("Helvetiva", 14, "bold")))
            self.presetDelete_Buttons.append(ctk.CTkButton(self.tabview.tab("Presets"), command=lambda id=id, index=i: self.presetDeleteAction(id, index), text="DEL", width=100, font=("Helvetiva", 14, "bold")))

            if data["Settings"]["QuickRecall_id"] == id: self.presetQuickRecall_RadioButtons[i].select()
            if data["Settings"]["CallOnStartup_id"] == id: self.presetStartUp_RadioButtons[i].select()

            self.presetName_Entrys[i].grid(row=i+1, column=0, padx=5, pady=5)
            self.presetLoad_Buttons[i].grid(row=i+1, column=1, padx=5, pady=5)
            self.presetStore_Buttons[i].grid(row=i+1, column=2, padx=5, pady=5)
            self.presetQuickRecall_RadioButtons[i].grid(row=i+1, column=3, padx=5, pady=5)
            self.presetStartUp_RadioButtons[i].grid(row=i+1, column=4, padx=5, pady=5)
            self.presetDelete_Buttons[i].grid(row=i+1, column=5, padx=5, pady=5)

        #adjust for the default-Preset
        self.presetName_Entrys[0].configure(state="disabled", text_color=("grey40", "grey60"))
        self.presetDelete_Buttons[0].configure(state="disabled")
        self.presetStore_Buttons[0].configure(state="disabled")
        self.presetDelete_Buttons[0].grid_forget()
        self.presetStore_Buttons[0].grid_forget()

        self.Quick_Label = ctk.CTkLabel(self.tabview.tab("Presets"), text="Quick", font=("Helvetiva", 14, "bold"))
        self.Quick_Label.grid(row=0, column=3, sticky="w")
        self.StartUp_Label = ctk.CTkLabel(self.tabview.tab("Presets"), text="StartUp", font=("Helvetiva", 14, "bold"))
        self.StartUp_Label.grid(row=0, column=4, sticky="w")

        self.newPreset_Button = ctk.CTkButton(self.tabview.tab("Presets"), command=lambda: self.createNewPreset(), text="Create New Preset", state="normal", font=("Helvetica", 16, "bold"))
        self.newPreset_Button.grid(row=len(self.presetLoad_Buttons)+1, column=0, padx=2, pady=2, columnspan=3, sticky="w")
    
    """def presetsTab_updateWhole(self):
        for i in range (len(self.presetName_Var)):
            try:
                self.presetName_Entrys[i].destroy()
                self.presetLoad_Buttons[i].destroy()
                self.presetStore_Buttons[i].destroy()
                self.presetQuickRecall_RadioButtons[i].destroy()
                self.presetStartUp_RadioButtons[i].destroy()
                self.presetDelete_Buttons[i].destroy()
            except:
                pass
        self.newPreset_Button.destroy()
        self.createPresetsTab()"""

    def presetsTab_deleteRow(self, index):
            self.presetName_Entrys[index].grid_forget()
            self.presetLoad_Buttons[index].grid_forget()
            self.presetStore_Buttons[index].grid_forget()
            self.presetQuickRecall_RadioButtons[index].grid_forget()
            self.presetStartUp_RadioButtons[index].grid_forget()
            self.presetDelete_Buttons[index].grid_forget()
    
    def presetsTab_addRow(self, id):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)

        index = len(self.presetLoad_Buttons)
        self.presetName_Var.append(ctk.StringVar(value=data["presets"][str(id)]["name"]))
        self.presetName_Entrys.append(ctk.CTkEntry(self.tabview.tab("Presets"), textvariable=self.presetName_Var[index], font=("Helvetica", 14, "bold")))
        self.presetName_Entrys[index].bind('<KeyRelease>', lambda event, id=id, index=index: self.presetNameEntryAction(event, id, index))
        self.presetLoad_Buttons.append(ctk.CTkButton(self.tabview.tab("Presets"), command=lambda id=id: self.loadPreset(id), text="recall", width=110, font=("Helvetiva", 14, "bold")))
        self.presetStore_Buttons.append(ctk.CTkButton(self.tabview.tab("Presets"), command=lambda id=id: self.saveExistingPreset(id), text="store", width=110, font=("Helvetiva", 14, "bold")))
        self.presetQuickRecall_RadioButtons.append(ctk.CTkRadioButton(self.tabview.tab("Presets"), command=lambda id=id: self.presetQuickRecallAction(id), variable=self.presetQuickRecall_RadioVar, value=id, text="", font=("Helvetiva", 14, "bold")))
        self.presetStartUp_RadioButtons.append(ctk.CTkRadioButton(self.tabview.tab("Presets"), command=lambda id=id: self.presetStartUpAction(id), variable=self.presetStartup_RadioVar, value=id, text="", font=("Helvetiva", 14, "bold")))
        self.presetDelete_Buttons.append(ctk.CTkButton(self.tabview.tab("Presets"), command=lambda id=id, index=index: self.presetDeleteAction(id, index), text="DEL", width=100, font=("Helvetiva", 14, "bold")))

        self.presetName_Entrys[index].grid(row=index+1, column=0, padx=5, pady=5)
        self.presetLoad_Buttons[index].grid(row=index+1, column=1, padx=5, pady=5)
        self.presetStore_Buttons[index].grid(row=index+1, column=2, padx=5, pady=5)
        self.presetQuickRecall_RadioButtons[index].grid(row=index+1, column=3, padx=5, pady=5)
        self.presetStartUp_RadioButtons[index].grid(row=index+1, column=4, padx=5, pady=5)
        self.presetDelete_Buttons[index].grid(row=index+1, column=5, padx=5, pady=5)

        self.newPreset_Button.grid_forget()
        self.newPreset_Button.grid(row=(len(self.presetLoad_Buttons)+1), column=0, padx=2, pady=2, columnspan=3, sticky="w")

    #other-tab
    def createSkipSettingsOption(self):
        self.skipSettings_Label = ctk.CTkLabel(self.tabview.tab("Other"), text="Skip Settings on startup", font=("Helvetica", 16, "bold"))
        self.skipSettings_Label.grid(row=0, column=0, sticky="e", pady=5)

        self.skipSettings_Switch = ctk.CTkSwitch(self.tabview.tab("Other"), variable=self.skipSettings_Var, command=self.skipSettingsAction, text="", onvalue="on", offvalue="off")
        self.skipSettings_Switch.grid(row=0, column=1, sticky="w", padx=10, pady=5)

    def createEnableQuickRecallOption(self):
        self.enableQuickRecall_Label = ctk.CTkLabel(self.tabview.tab("Other"), text="enable Quick Recall", font=("Helvetica", 16, "bold"))
        self.enableQuickRecall_Label.grid(row=1, column=0, sticky="e", pady=5)

        self.enableQuickRecall_Switch = ctk.CTkSwitch(self.tabview.tab("Other"), variable=self.enableQuickRecall_Var, command=self.enableQuickRecallAction, text="", onvalue="on", offvalue="off")
        self.enableQuickRecall_Switch.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    def createWarningLabel(self):
        self.skipSettingsWarning_Label = ctk.CTkLabel(self.tabview.tab("Other"), 
            text="The 'Skip-Settings' option will only work if all fields are filled \nout correctly in the preset set as the 'Startup Preset'. \nIf not, the preset will be loaded, and you will land \non the Settings Page.\n \nThe options on this page are saved globally. \nLoading or storing presets\nwill not change this options.",
            font=("Helvetica", 12, "bold"))

        self.skipSettingsWarning_Label.grid(row=2, column=0, columnspan=2, pady=5)
    
    #Go Button
    def createGoBtn(self):
        self.go_Button = ctk.CTkButton(self, command=self.showCounter, text="Go!", state="disabled", width=150, font=("Helvetica", 20, "bold"))
        self.go_Button.grid(row=1, column=0, columnspan=2, pady=5)
    
#---OPTION ACTIONS---
    #basic
    def updateAlwaysOnTop(self):
        if self.alwaysOnTop_Var.get() == "on":
            self.app_ref.set_always_on_top(True)
        else:
            self.app_ref.set_always_on_top(False)

    #advanced
    def updateCustomRow1(self, choice):
        if choice == "+ custom":
            self.customRow1Parameter_Label.grid(row=3, column=0, sticky="e", pady=5)
            self.customRow1Parameter_Entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
            self.customRow1Parameter_Entry.configure(state="normal")
        else:
            self.customRow1Parameter_Label.grid_forget()
            self.customRow1Parameter_Entry.grid_forget()
            self.customRow1Parameter_Entry.configure(state="readonly")
        self.validateGoBtn()

    def updateCustomRow2(self, choice):
        if choice == "+ custom":
            self.customRow2Parameter_Label.grid(row=5, column=0, sticky="e", pady=5)
            self.customRow2Parameter_Entry.grid(row=5, column=1, sticky="w", padx=10, pady=5)
            self.customRow2Parameter_Entry.configure(state="normal")
        else:
            self.customRow2Parameter_Label.grid_forget()
            self.customRow2Parameter_Entry.grid_forget()
            self.customRow2Parameter_Entry.configure(state="readonly")
        self.validateGoBtn()

    #design
    def updateColorMode(self, choice):
        if choice == "system":
            ctk.set_appearance_mode("system")
        elif choice == "dark":
            ctk.set_appearance_mode("dark")
        elif choice == "light":
            ctk.set_appearance_mode("light")

    def updateMonochromatic(self):
        global color_entryField_fg
        global color_Label
        global color_emphasis
        global color_highlight
        global color_increaseButton #[Text, fg_color, hover, disabled_color]
        global color_decreaseButton #[Text, fg_color, hover, disabled_color]
        global color_CustomButton #[Text, fg_color, hover, disabled_color]
        global color_resetButton #[Text, fg_color, hover, disabled_color]
        global color_lockButton #[open Text, open fg, open hover, locked text, locked fg, locked hover]
        global color_freezeButton #[open Text, open fg, open hover, frozen text, frozen fg, frozen hover]
        
        if self.monochrom_Var.get() == "off":
            color_entryField_fg = ("#f9f9fa", "#343638")
            color_Label = ("#333333", "#F7F7F7")
            color_emphasis = ("#BBBBBB", "#444444")
            color_highlight = ("#FFAC05", "#E49800")
            color_increaseButton = [("#333333", "#333333"), ("#48D948", "#35A035"), ("#35A035", "#48D948"), ("#6ee066", "#5aaf53")]
            color_decreaseButton = [("#333333", "#333333"), ("#E84141", "#AE3131"), ("#AE3131", "#E84141"), ("#ef6259", "#be524b")]
            color_CustomButton = [("#DCE4EE", "#DCE4EE"), ("#3a7ebf", "#1f538d"), ("#325882", "#14375e"), ("#5e90c8", "#47699e")]
            color_resetButton = [("#F7F7F7", "#333333"), ("#444444", "#B0B0B0"), ("#555555", "#CCCCCC"), ("#5d5d5d", "#bbbbbb")]
            color_lockButton = [("#F7F7F7", "#333333"), ("#444444", "#B0B0B0"), ("#555555", "#CCCCCC"), ("#333333", "#333333"), ("#E84141", "#E84141"), ("#AE3131", "#AE3131")]
            color_freezeButton = [("#F7F7F7", "#333333"), ("#444444", "#B0B0B0"), ("#555555", "#CCCCCC"), ("#333333", "#333333"), ("#48A7E2", "#48A7E2"), ("#368AB4", "#368AB4")]
        else:
            color_entryField_fg = ("#f9f9fa", "#343638")
            color_Label = ("gray14", "gray84")
            color_emphasis = ("#BBBBBB", "#444444")
            color_highlight = ("#FFAC05", "#E49800")
            color_increaseButton = [("#DCE4EE", "#DCE4EE"), ("#3a7ebf", "#1f538d"), ("#325882", "#14375e"), ("#5e90c8", "#47699e")]
            color_decreaseButton = [color_increaseButton[0], color_increaseButton[1], color_increaseButton[2], color_increaseButton[3]]
            color_CustomButton = [color_increaseButton[0], color_increaseButton[1], color_increaseButton[2], color_increaseButton[3]]
            color_resetButton = [color_increaseButton[0],color_increaseButton[2], color_increaseButton[1], color_increaseButton[3]]
            color_lockButton = [color_increaseButton[0],color_increaseButton[2], color_increaseButton[1], ("#333333", "#333333"), ("#E84141", "#E84141"), ("#AE3131", "#AE3131")]
            color_freezeButton = [color_increaseButton[0],color_increaseButton[2], color_increaseButton[1], ("#333333", "#333333"), ("#E84141", "#E84141"), ("#AE3131", "#AE3131")]
    
    #presets
    def presetNameEntryAction(self, e, id, index):
        newName = self.presetName_Entrys[index].get()
        self.setPresetName(id, newName)

    def presetQuickRecallAction(self, id):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        
        data["Settings"]["QuickRecall_id"] = str(id)
        name = data["presets"][str(id)]["name"]
        self.quickRecall_Button.configure(command=lambda id=id: self.loadPreset(id), text=name)

        with open(self.settingsFilePath, 'w') as f:
            json.dump(data, f, indent=4)

        self.showOrHideQuickRecall()

    def presetStartUpAction(self, id):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        
        data["Settings"]["CallOnStartup_id"] = str(id)

        with open(self.settingsFilePath, 'w') as f:
            json.dump(data, f, indent=4)

    def presetDeleteAction(self, id, index):
        self.deletePreset(id)
        self.presetsTab_deleteRow(index)

    #other
    def skipSettingsAction(self):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        
        data["Settings"]["SkipSettings"] = self.skipSettings_Var.get()

        with open(self.settingsFilePath, 'w') as f:
            json.dump(data, f, indent=4)

    def enableQuickRecallAction(self):
        with open(self.settingsFilePath, 'r') as f:
            data = json.load(f)
        
        data["Settings"]["EnableQuickRecall"] = self.enableQuickRecall_Var.get()

        with open(self.settingsFilePath, 'w') as f:
            json.dump(data, f, indent=4)

        self.showOrHideQuickRecall()

#---ACTION OF GO---
    def validateGoBtn(self, *args):#validates entrys and enables or disables the Go-Button
        if self.validateGoAction(): 
            self.go_Button.configure(state="normal")
        else: 
            self.go_Button.configure(state="disabled")

    def ReturnGo(self, e):#checks if the condition for the GoButton to be normal is met when return is pressed
        if self.validateGoAction(): self.showCounter()
    
    def validateGoAction(self):
        clVar = self.columns_Var.get()
        cr1Var = self.customRow1Parameter_Var.get()
        cr2Var = self.customRow2Parameter_Var.get()
        cr1Entry = self.customRow1Parameter_Entry
        cr2Entry = self.customRow2Parameter_Entry
        if ((clVar.isdigit() and 0 <= int(clVar) <= 26) and
            ((cr1Var.lstrip("+-").isdigit() and cr1Var.count('+') + cr1Var.count('-') <= 1) or cr1Entry.cget('state') == "readonly") and
            ((cr2Var.lstrip("+-").isdigit() and cr2Var.count('+') + cr2Var.count('-') <= 1) or cr2Entry.cget('state') == "readonly") and
            self.app_ref.currentPage=="Settings"):
            return True
        else:
            return False
        
    def showCounter(self):
        self.app_ref.hideSettingsFrame()
        self.app_ref.showWorkFrames(columns_Var = int(self.columns_Var.get()))
    
class Counter(ctk.CTkFrame):
    number_label = []

    def __init__(self, master, num_columns):
        super().__init__(master)

        self.number_label = []
        self.increase_buttons = []
        self.decrease_buttons = []
        self.label_a = []
        self.custom_button_1 = []
        self.custom_button_2 = []
        self.counterLeaderboard_Labels = []
        self.column_key_mapping = {}  # Mapping between columns and keys


        self.Settings_ref = self.master.SettingsFrame.SettingsScrollableFrame

        self.generalFontSize = int(self.Settings_ref.generalFontSize_Var.get())
        if(self.Settings_ref.namesFontSize_Var.get() == "general size"):
            self.namesFontSize = self.generalFontSize
        else: self.namesFontSize = int(self.Settings_ref.namesFontSize_Var.get())
        self.lock_state = False

        #create widgets
        for i in range(num_columns):
            key = chr(ord('A') + i)  # Assigning keys A, B, C, ...
            self.column_key_mapping[key] = i  # Mapping key to column index

            columnFilePath = os.path.join(self.master.get_script_folder(), "values", "num-{}.txt".format(chr(ord('A') + i)))

             # increase buttons
            self.increase_buttons.append(
                ctk.CTkButton(self, command=lambda i=i: self.increaseNum(i, 1), text="+", font=("Helvetiva", self.generalFontSize, "bold"),
                              text_color=color_increaseButton[0], hover_color=color_increaseButton[2],
                              fg_color=color_increaseButton[1]))
            self.increase_buttons[i].grid(row=0, column=i*2, sticky="nsew", padx=2, pady=2)

            # number label; check if file already exists and read from it/create new
            if os.path.exists(columnFilePath):
                f = open(columnFilePath, "r")
                self.number_label.append(
                    ctk.CTkLabel(self, text=f.read(), font=("Helvetiva", self.generalFontSize, "bold"), text_color=color_Label))
            else:
                self.number_label.append(
                    ctk.CTkLabel(self, text="0", font=("Helvetiva", self.generalFontSize, "bold"), text_color=color_Label))
                self.saveToFile("0", chr(ord('A') + i))
            self.number_label[i].grid(row=1, column=i*2, sticky="nsew", padx=2, pady=2)

            # decrease buttons
            self.decrease_buttons.append(
                ctk.CTkButton(self, command=lambda i=i: self.decreaseNum(i, 1), text="-", font=("Helvetiva", int(self.generalFontSize*1.1), "bold"),
                              text_color=color_decreaseButton[0], hover_color=color_decreaseButton[2],
                              fg_color=color_decreaseButton[1]))
            self.decrease_buttons[i].grid(row=2, column=i*2, sticky="nsew", padx=2, pady=2)

            #custom Button 1
            self.createCustomButton(i, self.custom_button_1, self.Settings_ref.customRow1_Type.get(), 1, self.Settings_ref.customRow1Parameter_Var.get())
            
            #custom Buttom 2
            self.createCustomButton(i, self.custom_button_2, self.Settings_ref.customRow2_Type.get(), 2, self.Settings_ref.customRow2Parameter_Var.get())

            #leaderboard
            self.counterLeaderboard_Labels.append(ctk.CTkLabel(self))
            if(self.Settings_ref.showLeaders_Var.get() != "off"): 
                self.counterLeaderboard_Labels[i].grid(row=6, column=i*2, sticky="nsew", padx=2, pady=2)

            # Column Name Label
            if self.Settings_ref.showNames_Var.get() == "on":
                self.label_a.append(ctk.CTkLabel(self, text=self.Settings_ref.names_Vars[i].get(), font=("Helvetiva", self.namesFontSize, "bold"), fg_color=color_emphasis, corner_radius=5, text_color=color_Label))
            else:
                self.label_a.append(ctk.CTkLabel(self, text=chr(ord('A') + i), font=("Helvetiva", self.namesFontSize, "bold"), fg_color=color_emphasis, corner_radius=5, text_color=color_Label))
            self.label_a[i].grid(row=3, column=i*2, sticky="nsew", padx=2, pady=10)

            #highlight
            if((chr(ord('A') + i)) in self.Settings_ref.highlight_Var.get()):
                self.number_label[i].configure(fg_color=color_highlight, corner_radius=7)
                self.decrease_buttons[i].configure(border_color=color_highlight, border_width=2)
                self.increase_buttons[i].configure(border_color=color_highlight, border_width=2)
                self.label_a[i].configure(fg_color=color_highlight, corner_radius=7)
                if(self.Settings_ref.customRow1_Type.get() != "hide"):
                    self.custom_button_1[i].configure(border_color=color_highlight, border_width=2)
                if(self.Settings_ref.customRow2_Type.get() != "hide"):
                    self.custom_button_2[i].configure(border_color=color_highlight, border_width=2)
            
            #separator
            if(chr(ord('A') + i)) in self.Settings_ref.separator_Var.get():
                rspan = 4
                if(self.Settings_ref.customRow1_Type.get() != "hide"): rspan = 5
                if(self.Settings_ref.customRow2_Type.get() != "hide"): rspan = 6
                separator = ctk.CTkFrame(self, width=2, fg_color=color_Label)
                separator.grid(column=(i*2)+1, row=0, rowspan=rspan, sticky='ns', padx=0, pady=5)

            # configure
            self.columnconfigure(i*2, weight=1)

        # configure
        self.rowconfigure((0, 1, 2, 3), weight=1)
        if(self.Settings_ref.customRow1_Type.get() != "hide"): self.rowconfigure(4, weight=1)
        if(self.Settings_ref.customRow2_Type.get() != "hide"): self.rowconfigure(5, weight=1)
        if(self.Settings_ref.showLeaders_Var.get() != "off"): 
            self.rowconfigure(6, weight=1)
        self.configure(fg_color="transparent")

        self.updateCounterLeaderboard()
        self.saveLeaderboardToFiles()

        # Event binding for keys
        master.bind('<KeyPress>', lambda event, index="", customRowIndex="", mode=0: self.on_key_pressed(event, index, customRowIndex, mode))
    
    def createCustomButton(self, i, buttonArray, rowType, CustomRowIndex, parameterVar):
        if (rowType == "hide"):
                buttonArray.append("")
        elif (rowType == "+10"):
            buttonArray.append(ctk.CTkButton(self, command=lambda i=i: self.increaseNum(i, 10), text="+10", font=("Helvetiva", int(self.generalFontSize*0.9), "bold"),
                                text_color=color_CustomButton[0], hover_color=color_CustomButton[2], fg_color=color_CustomButton[1]))
        elif (rowType == "-10"):
            buttonArray.append(ctk.CTkButton(self, command=lambda i=i: self.decreaseNum(i, 10), text="-10", font=("Helvetiva", int(self.generalFontSize*0.9), "bold"),
                                text_color=color_CustomButton[0], hover_color=color_CustomButton[2], fg_color=color_CustomButton[1]))
        elif (rowType == "+ custom"):
            if (int(parameterVar) >= 0) and not("+" in parameterVar):
                buttonArray.append(ctk.CTkButton(self, command=lambda i=i: self.increaseNum(i, int(parameterVar)), text="+" +str(parameterVar), font=("Helvetiva", int(self.generalFontSize*0.9), "bold"),
                                text_color=color_CustomButton[0], hover_color=color_CustomButton[2], fg_color=color_CustomButton[1]))
            else:
                buttonArray.append(ctk.CTkButton(self, command=lambda i=i: self.increaseNum(i, int(parameterVar)), text=str(parameterVar), font=("Helvetiva", int(self.generalFontSize*0.9), "bold"),
                                text_color=color_CustomButton[0], hover_color=color_CustomButton[2], fg_color=color_CustomButton[1]))
        elif (rowType == "add entry"):
            buttonArray.append(ctk.CTkEntry(self, placeholder_text="add", font=("Helvetica", int(self.generalFontSize*0.7), "bold")))
            buttonArray[i].bind('<Key>', lambda event, index=i, customRowIndex=CustomRowIndex, mode=1: self.on_key_pressed(event, index, customRowIndex, mode))
        elif (rowType == "set entry"):
            buttonArray.append(ctk.CTkEntry(self, placeholder_text="set", font=("Helvetica", int(self.generalFontSize*0.7), "bold")))
            buttonArray[i].bind('<Key>', lambda event, index=i, customRowIndex=CustomRowIndex, mode=3: self.on_key_pressed(event, index, customRowIndex, mode))
        elif (rowType == "reset"):
            buttonArray.append(ctk.CTkButton(self, command=lambda i=i: self.reset_singleColumn(i), text="=0", font=("Helvetiva", int(self.generalFontSize*0.9), "bold"),
                                text_color=color_CustomButton[0], hover_color=color_CustomButton[2], fg_color=color_CustomButton[1]))
        if rowType != "hide": buttonArray[i].grid(row=3+CustomRowIndex, column=i*2, sticky="nsew", padx=2, pady=5)

    def on_key_pressed(self, e, index, customRowIndex, mode): #mode: 0:Empty, 1:add, 2:substract, 3:set
        char = e.char
        keysym = e.keysym
        keysymUpper = e.keysym.upper()
        state = e.state
        special_keysyms = [ "Control_L", "Alt_L", "Tab", "Shift_L", "Return", "Escape", "BackSpace", "Delete", "Up", "Down", "Left", "Right", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Home", "End", "Page_Up", "Page_Down", "Insert", "Print", "Pause", "Caps_Lock", "Num_Lock", "Scroll_Lock"]

        shift = False
        crtl = False
        alt = False

        if e.state & (1 << 0):  # Shift
            shift = True
        if e.state & (1 << 2) or e.state & (1 << 6):  # Control #Bit 6 ist AltGr
            crtl = True
        if e.state & (1 << 3) or e.state & (1 << 17) or e.state & (1 << 6):  # Alt
            alt = True
        

        if (crtl and not(shift) and not(alt) and self.master.currentPage == "Counter"): #Control-Shortcuts
            if keysymUpper == 'COMMA': # Ctrl, Komma -> Settings
                self.master.ControlsFrame.showSettings()
                return 'break'
            elif keysymUpper == 'L': # Crtl + L -> Lock
                self.toggleLock()
                return 'break'

        #Hotkeys
        if not(char.isdigit() or keysym in special_keysyms or keysym=="plus" or keysym=="minus") and self.master.currentPage == "Counter" and self.Settings_ref.hotkeys_Var.get() == "on":
            if keysymUpper in self.column_key_mapping:
                column_index = self.column_key_mapping[keysymUpper]  # Get the corresponding column index

                if not(crtl) and not(shift) and not(alt): #Increase 1
                        self.increaseNum(column_index, 1) 
                elif not(crtl) and shift and not(alt):  #Decrease 1
                        self.decreaseNum(column_index, 1)
                elif crtl and shift and not(alt): #Reset Single
                    self.reset_singleColumn(column_index)
                elif not(crtl) and alt: #Custom Buttons
                    if not(shift): #Custom Button 1
                        rowType = self.Settings_ref.customRow1_Type.get()
                        parameterVar = self.Settings_ref.customRow1Parameter_Var.get()
                        customButtonObj = self.custom_button_1[column_index]
                    else: #Custom Button 2
                        rowType = self.Settings_ref.customRow2_Type.get()
                        parameterVar = self.Settings_ref.customRow2Parameter_Var.get()
                        customButtonObj = self.custom_button_2[column_index]

                    if (rowType == "hide"):
                         pass
                    elif (rowType == "+10"):
                        self.increaseNum(column_index, 10)
                    elif (rowType == "-10"):
                        self.decreaseNum(column_index, 10)
                    elif (rowType == "+ custom"):
                        self.increaseNum(column_index, int(parameterVar))
                    elif (rowType == "add entry"):
                        customButtonObj.focus()
                    elif (rowType == "set entry"):
                        customButtonObj.focus_set()
                    elif (rowType == "reset"):
                        self.reset_singleColumn(column_index)
            else:
                if crtl and shift and not(alt) and (keysymUpper == 'period' or keysymUpper == 'COLON'):
                    self.master.ControlsFrame.reset()
            return 'break'
        
                        
        #Entry Box
        elif index != "":
            if keysym=="Return":
                if isinstance(index, int):
                    if   customRowIndex == 1: entered_number = int(self.custom_button_1[index].get())
                    elif customRowIndex == 2: entered_number = int(self.custom_button_2[index].get())

                    if   mode == 1: self.increaseNum(index, entered_number)
                    elif mode == 2: self.decreaseNum(index, entered_number)
                    elif mode == 3: self.setValue(index, entered_number)
            elif keysym=="BackSpace" and state == 0x4:
                self.custom_button_1[index].delete(0, self.custom_button_1[index].index(ctk.INSERT))
            elif keysym=="Delete" and state == 0x4:
                self.custom_button_1[index].delete(self.custom_button_1[index].index(ctk.INSERT), ctk.END)

    def reset_singleColumn(self, i):
        if(not(self.lock_state)):
            self.number_label[i].configure(text="0")
            self.saveToFile("0", chr(ord('A') + i))
            self.saveLeaderboardToFiles()

    def resetAll(self):
        if(not(self.lock_state)):
            if self.Settings_ref.resetShownOnly_Var.get() == "on":
                for i, label in enumerate(self.number_label):
                    label.configure(text="0")
                    self.saveToFile("0", chr(ord('A') + i))
            else:
                for i, label in enumerate(self.number_label):
                    label.configure(text="0")
                j = 0
                while os.path.exists(os.path.join(self.master.get_script_folder(), "values", "num-{}.txt".format(chr(ord('A') + j)))):
                    self.saveToFile("0", chr(ord('A') + j))
                    j+=1
            self.saveLeaderboardToFiles()
    
    def increaseNum(self, i, Num):
        if(not(self.lock_state)):
            current_number = int(self.number_label[i].cget("text"))
            current_number += Num
            self.number_label[i].configure(text=str(current_number))
            self.saveToFile(str(current_number), chr(ord('A') + i))
            self.saveLeaderboardToFiles()

    def decreaseNum(self, i, Num):
        if(not(self.lock_state)):
            current_number = int(self.number_label[i].cget("text"))
            current_number -= Num
            self.number_label[i].configure(text=str(current_number))
            self.saveToFile(str(current_number), chr(ord('A') + i))
            self.saveLeaderboardToFiles()
    
    def setValue(self, i, Num):
        if(not(self.lock_state)):
            current_number = Num
            self.number_label[i].configure(text=str(current_number))
            self.saveToFile(str(current_number), chr(ord('A') + i))
            self.saveLeaderboardToFiles()

    def saveToFile(self, current_number, column):
        script_dir = self.master.get_script_folder()
        column_FilePath = os.path.join(script_dir, "values", "num-{}.txt".format(column))
        with open(column_FilePath, "w") as file:
            file.write(current_number)
    
    def saveLeaderboardToFiles(self):
        self.updateCounterLeaderboard()
        if(self.Settings_ref.doFreezeLeaderboard_Var.get() != "on"):
            script_dir = self.master.get_script_folder()
            columnValues = []
            columnNames = self.Settings_ref.names_Vars
            
            # Read values from files into columnValues
            for i in range(int(self.Settings_ref.columns_Var.get())):
                column_FilePath = os.path.join(script_dir, "values", "num-{}.txt".format(chr(ord('A') + i)))
                with open(column_FilePath, 'r') as f:
                    columnValues.append(f.read().strip())

            # Create and sort the 2D array, then write the leaderboard files
            self.columns_sorted_array = self.createSortedLeaderboardArray(columnNames, columnValues)
            self.writeLeaderboardFiles(self.columns_sorted_array, script_dir)

    def createSortedLeaderboardArray(self, columnNames, columnValues):#creates a 2D-Array containing the index, Name and Score sorted after the Score; written by chat-GPT
        # Create the 2D array
        mergedArray = []
        excludedCUlumnNumbers = []

        for char in self.Settings_ref.excludeFromLeaderboard_Var.get():
            if char.isalpha():  # Check if the character is a letter
                position = ord(char.lower()) - ord('a')
                excludedCUlumnNumbers.append([position])    	

        for index, (name, points) in enumerate(zip(columnNames, columnValues)):
            if(not([index] in excludedCUlumnNumbers)):
                mergedArray.append([index, name, int(points)])
    
        # Determine the sorting order based on invertLeaderboard_Var
        invert = self.Settings_ref.invertLeaderboard_Var.get() == "on"
        
        # Sort the array by score in the required order
        mergedArray.sort(key=lambda x: x[2], reverse=not invert)

        # Calculate ranks and add them to the array
        ranked_result = []
        current_rank = 1
        previous_points = None
        for rank_count, (index, name, points) in enumerate(mergedArray, start=1):
            if points != previous_points:
                current_rank = rank_count
            previous_points = points
            ranked_result.append([index, name, points, current_rank])
    
        return ranked_result

    def writeLeaderboardFiles(self, sorted_array, script_dir):#written by chat-GPT
        base_path = os.path.join(script_dir, "leaderboard")
        names_path = os.path.join(base_path, "names")
        ranks_path = os.path.join(base_path, "ranks")
        scores_path = os.path.join(base_path, "scores")
        
        # Create directories if they do not exist
        os.makedirs(names_path, exist_ok=True)
        os.makedirs(ranks_path, exist_ok=True)
        os.makedirs(scores_path, exist_ok=True)

        for index, (original_index, name, points, rank) in enumerate(sorted_array):
            with open(os.path.join(names_path, f"place{index+1}_name.txt"), "w") as f:
                f.write(name.get())
            
            with open(os.path.join(ranks_path, f"place{index+1}_rank.txt"), "w") as f:
                f.write(str(rank))
            
            with open(os.path.join(scores_path, f"place{index+1}_score.txt"), "w") as f:
                f.write(str(points))

    def toggleLock(self):
        if(self.Settings_ref.lock_Var.get() == "on"):
            if(self.lock_state):
                self.lock_state = False
                self.master.ControlsFrame.lock_button.configure(text="\U0001F513", text_color=color_lockButton[0], fg_color=color_lockButton[1], hover_color=color_lockButton[2])
                for i, label in enumerate(self.number_label):
                    self.increase_buttons[i].configure(state = "normal", fg_color=color_increaseButton[1])
                    self.decrease_buttons[i].configure(state = "normal", fg_color=color_decreaseButton[1])
                    if(self.Settings_ref.customRow1_Type.get() != "hide"): 
                        self.custom_button_1[i].configure(state = "normal", fg_color=color_CustomButton[1])
                        if(self.Settings_ref.customRow1_Type.get() == "add entry" or self.Settings_ref.customRow1_Type.get() ==  "set entry"): 
                            self.custom_button_1[i].configure(state = "normal", fg_color=color_entryField_fg)
                    if(self.Settings_ref.customRow2_Type.get() != "hide"): 
                        self.custom_button_2[i].configure(state = "normal", fg_color=color_CustomButton[1])
                        if(self.Settings_ref.customRow2_Type.get() == "add entry" or self.Settings_ref.customRow2_Type.get() ==  "set entry"): 
                            self.custom_button_2[i].configure(state = "normal", fg_color=color_entryField_fg)
            else:
                self.lock_state = True
                self.master.ControlsFrame.lock_button.configure(text="\U0001F512", text_color=color_lockButton[3], fg_color=color_lockButton[4], hover_color=color_lockButton[5])
                for i, label in enumerate(self.number_label):
                    self.increase_buttons[i].configure(state = "disabled", hover_color=color_increaseButton[2], fg_color=color_increaseButton[3])
                    self.decrease_buttons[i].configure(state = "disabled", hover_color=color_decreaseButton[2], fg_color=color_decreaseButton[3])
                    if(self.Settings_ref.customRow1_Type.get() != "hide"): self.custom_button_1[i].configure(state = "disabled", fg_color=color_CustomButton[3])
                    if(self.Settings_ref.customRow2_Type.get() != "hide"): self.custom_button_2[i].configure(state = "disabled", fg_color=color_CustomButton[3])

    def toggleFreezeLeaderboard(self):
         if(self.Settings_ref.showFreezeLeaderboard_Var.get() == "on"):
            if(self.Settings_ref.doFreezeLeaderboard_Var.get() == "on"):
                self.Settings_ref.doFreezeLeaderboard_Var = ctk.StringVar(value="off")
                self.master.ControlsFrame.freezeLeaderboard_button.configure(text_color=color_freezeButton[0], fg_color=color_freezeButton[1], hover_color=color_freezeButton[2])
            else:
                self.Settings_ref.doFreezeLeaderboard_Var = ctk.StringVar(value="on")
                self.master.ControlsFrame.freezeLeaderboard_button.configure(text_color=color_freezeButton[3], fg_color=color_freezeButton[4], hover_color=color_freezeButton[5])
                self.saveLeaderboardToFiles()
    
    def updateCounterLeaderboard(self):
        script_dir = self.master.get_script_folder()
        sortedColumns = []
        columnValues = []
            
        # Read values from files into columnValues
        for i in range(int(self.Settings_ref.columns_Var.get())):
            column_FilePath = os.path.join(script_dir, "values", "num-{}.txt".format(chr(ord('A') + i)))
            with open(column_FilePath, 'r') as f:
                columnValues.append(f.read().strip())

        sortedColumns = self.createSortedLeaderboardArray(self.Settings_ref.names_Vars, columnValues)
        
        for i in range (int(self.Settings_ref.columns_Var.get())):
            index = self.search_value_in_first_column(sortedColumns, i) #get index of the column in the sorted Array
            try:
                rank=int(sortedColumns[index][3])
            except:
                rank=""
            if (rank == 1): self.counterLeaderboard_Labels[i].configure(text="\U0001F947",font=("Helvetiva", int(self.generalFontSize*1.35)), text_color="#FFD700")
            elif (rank == 2):self.counterLeaderboard_Labels[i].configure(text="\U0001F948", font=("Helvetiva", int(self.generalFontSize*1.35)), text_color="#C0C0C0")
            elif (rank == 3):self.counterLeaderboard_Labels[i].configure(text="\U0001F949", font=("Helvetiva", int(self.generalFontSize*1.35)), text_color="#CD7F32")
            else: self.counterLeaderboard_Labels[i].configure(text=str(rank), font=("Helvetiva", int(self.generalFontSize*0.8), "bold"), text_color=color_Label)
    
    def search_value_in_first_column(self, array, value):
        for index, row in enumerate(array):
            if row[0] == value:
                return index
        
class Controls(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        #reset-Button
        reset_button = ctk.CTkButton(self, command=self.reset, text="Reset", font=("Helvetiva", 16, "bold"), text_color=color_resetButton[0], fg_color=color_resetButton[1], hover_color=color_resetButton[2])
        reset_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=(0,5))

        #settings-Button
        settings_button = ctk.CTkButton(self, command=self.showSettings, text="Settings", font=("Helvetiva", 16, "bold"), text_color=color_resetButton[0], fg_color=color_resetButton[1], hover_color=color_resetButton[2])
        settings_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=(0,5))

        #lock-Button
        if(self.master.SettingsFrame.SettingsScrollableFrame.lock_Var.get() == "on"):
            self.lock_button = ctk.CTkButton(self, command=self.master.CounterFrame.toggleLock, text="\U0001F513", font=("Helvetiva", 21, "bold"), width=30, text_color=color_freezeButton[0], fg_color=color_freezeButton[1], hover_color=color_freezeButton[2])
            self.lock_button.grid(row=0, column=3, sticky="nsew", padx=5, pady=(0,5))

        #freezeLeaderboard-Button
        if(self.master.SettingsFrame.SettingsScrollableFrame.showFreezeLeaderboard_Var.get() == "on"):
            if(self.master.SettingsFrame.SettingsScrollableFrame.doFreezeLeaderboard_Var.get() == "off"):
                self.freezeLeaderboard_button = ctk.CTkButton(self, command=self.master.CounterFrame.toggleFreezeLeaderboard, text="\u2744\U0001F4CA", font=("Helvetiva", 21), width=30, text_color=color_freezeButton[0], fg_color=color_freezeButton[1], hover_color=color_freezeButton[2])
            else:
                self.freezeLeaderboard_button = ctk.CTkButton(self, command=self.master.CounterFrame.toggleFreezeLeaderboard, text="\u2744\U0001F4CA", font=("Helvetiva", 21), width=30, text_color=color_freezeButton[3], fg_color=color_freezeButton[4], hover_color=color_freezeButton[5])
            self.freezeLeaderboard_button.grid(row=0, column=2, sticky="nsew", padx=5, pady=(0,5))

        #configure
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(fg_color="transparent")
    
    def showSettings(self):
        self.master.hideWorkFrames()
        self.master.showSettingsFrame()

    def reset(self):
        self.master.CounterFrame.resetAll()


class ErrorWindow(ctk.CTkToplevel):
    def __init__(self, master, message, type): #type :  0: Quit, Reset - 1: OK
        super().__init__(master)
        self.geometry("300x150")
        self.title("Error")
        self.protocol("WM_DELETE_WINDOW", disallowClosing)

        self.action = ""
        self.app_ref = master

        label = ctk.CTkLabel(self, text=message, font=("Helvetica", 16, "bold"))
        quitButton = ctk.CTkButton(self, text="Quit", command=self.quit, font=("Helvetica", 16, "bold"))
        resetButton = ctk.CTkButton(self, text="Reset to default settings and quit", command=self.resetToDefault, font=("Helvetica", 16, "bold"))
        okButton = ctk.CTkButton(self, text="Ok", command=self.exit, font=("Helvetica", 16, "bold"))

        label.grid(row=0, column=0)
        if type == 0: quitButton.grid(row=1, column=0)
        if type == 0: resetButton.grid(row=2, column=0)
        if type == 1: okButton.grid(row=2, column=0)

        self.rowconfigure((0,1,2), weight=1)
        self.columnconfigure(0, weight=1)
    
    def quit(self):
        self.action = "quit"
        self.destroy()
    
    def resetToDefault(self):
        self.action = "reset"
        self.defaultSettingsContent = {
            "Settings": {
                "QuickRecall_id": "0",
                "CallOnStartup_id": "0",
                "SkipSettings": "off",
                "EnableQuickRecall": "off"
            },
            "presets": {
                "0": {
                    "name": "default",
                    "columns_Var": "",
                    "resetShownOnly_Var": "on",
                    "highlight_Var": "",
                    "separator_Var": "",
                    "showNames_Var": "off",
                    "showLeaders_Var": "off",
                    "colorMode_Var": "system",
                    "monochrom_Var": "off",
                    "generalFontSize_Var": "20",
                    "namesFontSize_Var": "general size",
                    "alwaysOnTop_Var": "off",
                    "hotkeys_Var": "on",
                    "customRow1_Type": "hide",
                    "customRow2_Type": "hide",
                    "customRow1Parameter_Var": "",
                    "customRow2Parameter_Var": "",
                    "lock_Var": "off",
                    "doFreezeLeaderboard_Var": "off",
                    "showFreezeLeaderboard_Var": "off",
                    "invertLeaderboard_Var": "off",
                    "excludeFromLeaderboard_Var": "",
                    "names_Vars": {
                        "A": "A",
                        "B": "B",
                        "C": "C",
                        "D": "D",
                        "E": "E",
                        "F": "F",
                        "G": "G",
                        "H": "H",
                        "I": "I",
                        "J": "J",
                        "K": "K",
                        "L": "L",
                        "M": "M",
                        "N": "N",
                        "O": "O",
                        "P": "P",
                        "Q": "Q",
                        "R": "R",
                        "S": "S",
                        "T": "T",
                        "U": "U",
                        "V": "V",
                        "W": "W",
                        "X": "X",
                        "Y": "Y",
                        "Z": "Z"
                    }
                }
            }
        }

        with open(os.path.join(self.app_ref.get_script_folder(),'config', 'Settings.json'), 'w') as f:
            json.dump(self.defaultSettingsContent, f, indent=4)

        self.destroy()
    
    def exit(self):
        self.action = "exit"
        self.destroy()
            
    
class ShortcutsWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("500x300")
        self.minsize(350, 200)
        self.title("Shortcuts")

        self.app_ref = master

        innerFrame = ctk.CTkScrollableFrame(master=self)
        innerFrame.grid(row=0, column=0, sticky="nsew")


        self.shortcutLabel_keys_1 = ctk.CTkLabel(innerFrame, text="[letter]", font=("Helvetica", 14, "bold"), fg_color=("#3b8ed0", "#1f6aa5"),corner_radius=3)
        self.shortcutLabel_keys_2 = ctk.CTkLabel(innerFrame, text="Shift + [letter]", font=("Helvetica", 14, "bold"), fg_color=("#3b8ed0", "#1f6aa5"),corner_radius=3)
        self.shortcutLabel_keys_3 = ctk.CTkLabel(innerFrame, text="Alt + [letter]", font=("Helvetica", 14, "bold"), fg_color=("#3b8ed0", "#1f6aa5"),corner_radius=3)
        self.shortcutLabel_keys_4 = ctk.CTkLabel(innerFrame, text="Alt + Shift + [letter]",font=("Helvetica", 14, "bold"), fg_color=("#3b8ed0", "#1f6aa5"),corner_radius=3)
        self.shortcutLabel_keys_5 = ctk.CTkLabel(innerFrame, text="Crtl + Shift + [letter]", font=("Helvetica", 14, "bold"), fg_color=("#3b8ed0", "#1f6aa5"),corner_radius=3)
        self.shortcutLabel_keys_6 = ctk.CTkLabel(innerFrame, text="Crtl + Shift + [period]", font=("Helvetica", 14, "bold"), fg_color=("#3b8ed0", "#1f6aa5"),corner_radius=3)
        self.shortcutLabel_keys_7 = ctk.CTkLabel(innerFrame, text="Crtl + [comma]", font=("Helvetica", 14, "bold"), fg_color=("#3b8ed0", "#1f6aa5"),corner_radius=3)
        self.shortcutLabel_keys_8 = ctk.CTkLabel(innerFrame, text="Crtl + L", font=("Helvetica", 14, "bold"), fg_color=("#3b8ed0", "#1f6aa5"),corner_radius=3)

        self.shortcutLabel_functions_1 = ctk.CTkLabel(innerFrame, text="Increase column by 1*",font=("Helvetica", 14, "bold"))
        self.shortcutLabel_functions_2 = ctk.CTkLabel(innerFrame, text="Decrease column by 1*", font=("Helvetica", 14, "bold"))
        self.shortcutLabel_functions_3 = ctk.CTkLabel(innerFrame, text="Do Custom Action 1*", font=("Helvetica", 14, "bold"))
        self.shortcutLabel_functions_4 = ctk.CTkLabel(innerFrame, text="Do Custom Action 1*", font=("Helvetica", 14, "bold"))
        self.shortcutLabel_functions_5 = ctk.CTkLabel(innerFrame, text="Reset Column*", font=("Helvetica", 14, "bold"))
        self.shortcutLabel_functions_6 = ctk.CTkLabel(innerFrame, text="Reset all*", font=("Helvetica", 14, "bold"))
        self.shortcutLabel_functions_7 = ctk.CTkLabel(innerFrame, text="Settings", font=("Helvetica", 14, "bold"))
        self.shortcutLabel_functions_8 = ctk.CTkLabel(innerFrame, text="Lock Surface**", font=("Helvetica", 14, "bold"))

        self.shortcutLabel_note = ctk.CTkLabel(innerFrame, text="Note that the Scoreboard-Window needs to\nbe in the foreground for the shortcuts to work.\n\n*only works when the 'Hotkeys'-function is enabled.\n**only works when the 'enable Lock'-function is enabled.", font=("Helvetica", 12, "bold"))
        
        self.shortcutLabel_keys_1.grid(row=0, column=0, sticky="e", pady=2, padx=5)
        self.shortcutLabel_keys_2.grid(row=1, column=0, sticky="e", pady=2, padx=5)
        self.shortcutLabel_keys_3.grid(row=2, column=0, sticky="e", pady=2, padx=5)
        self.shortcutLabel_keys_4.grid(row=3, column=0, sticky="e", pady=2, padx=5)
        self.shortcutLabel_keys_5.grid(row=4, column=0, sticky="e", pady=2, padx=5)
        self.shortcutLabel_keys_6.grid(row=5, column=0, sticky="e", pady=2, padx=5)
        self.shortcutLabel_keys_7.grid(row=6, column=0, sticky="e", pady=2, padx=5)
        self.shortcutLabel_keys_8.grid(row=7, column=0, sticky="e", pady=2, padx=5)

        separator = ctk.CTkFrame(innerFrame, width=2, fg_color=("#333333", "#F7F7F7"))
        separator.grid(column=1, row=0, rowspan=8, sticky='nse', padx=0, pady=5)

        self.shortcutLabel_functions_2.grid(row=1, column=2, sticky="w", pady=0, padx=10)
        self.shortcutLabel_functions_1.grid(row=0, column=2, sticky="w", pady=0, padx=10)
        self.shortcutLabel_functions_3.grid(row=2, column=2, sticky="w", pady=0, padx=10)
        self.shortcutLabel_functions_4.grid(row=3, column=2, sticky="w", pady=0, padx=10)
        self.shortcutLabel_functions_5.grid(row=4, column=2, sticky="w", pady=0, padx=10)
        self.shortcutLabel_functions_6.grid(row=5, column=2, sticky="w", pady=0, padx=10)
        self.shortcutLabel_functions_7.grid(row=6, column=2, sticky="w", pady=0, padx=10)
        self.shortcutLabel_functions_8.grid(row=7, column=2, sticky="w", pady=0, padx=10)
        
        self.shortcutLabel_note.grid(row=8, column=0, columnspan=3, pady=5, padx=0)

        exitButton = ctk.CTkButton(innerFrame, text="exit", command=self.exit, font=("Helvetica", 16, "bold"))
        exitButton.grid(row=10, column=0, columnspan=3, sticky="n")



        innerFrame.columnconfigure((0,2), weight=1)
        innerFrame.columnconfigure(1, weight=0)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def exit(self):
        if self.app_ref.shortcuts_window:
            self.app_ref.shortcuts_window.destroy()
            self.app_ref.shortcuts_window = None

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x250")
        self.minsize(350, 200)
        self.title("About")

        self.app_ref = master

        innerFrame = ctk.CTkScrollableFrame(master=self)
        innerFrame.grid(row=0, column=0, sticky="nsew")

        heading = ctk.CTkLabel(innerFrame, text="Scoreboard 8.1.0", font=("Helvetica", 22, "bold"))
        heading.grid(row=0, column=0)

        subheading = ctk.CTkLabel(innerFrame, text="Propresenter 7 extension by Micha Bokelmann", font=("Helvetica", 14, "bold"))
        subheading.grid(row=1, column=0, sticky="n")

        separator = ctk.CTkFrame(innerFrame, height=2, fg_color=color_Label)
        separator.grid(row=2, column=0, sticky='ew', padx=20, pady=0)

        text = ctk.CTkLabel(innerFrame, text="\nThis software is designed for\nchurches to enhance the functionality\nof ProPresenter. Churches are welcome to use\nit freely for their events.\n\nTo learn more about its usage, receive updates,\naccess free resources, report issues,\nor request new features, please visit\nhttps://556f.short.gy/ScoreboardEN.\n", font=("Helvetica", 14))
        text.grid(row=3, column=0, sticky="n")

        exitButton = ctk.CTkButton(innerFrame, text="exit", command=self.exit, font=("Helvetica", 16, "bold"))
        exitButton.grid(row=5, column=0, columnspan=3, sticky="n")
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        innerFrame.columnconfigure(0, weight=1)

    def exit(self):
        if self.app_ref.about_window:
            self.app_ref.about_window.destroy()
            self.app_ref.about_window = None

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x260")
        self.title("Scoreboard")

        # Ensure folders exists, if not, create it
        if not os.path.exists(os.path.join(self.get_script_folder(), 'config')): os.makedirs(os.path.join(self.get_script_folder(), 'config'))
        if not os.path.exists(os.path.join(self.get_script_folder(), 'values')): os.makedirs(os.path.join(self.get_script_folder(), 'values'))
        if not os.path.exists(os.path.join(self.get_script_folder(), 'names')): os.makedirs(os.path.join(self.get_script_folder(), 'names'))
        if not os.path.exists(os.path.join(self.get_script_folder(), 'leaderboard')): os.makedirs(os.path.join(self.get_script_folder(), 'leaderboard'))
        if not os.path.exists(os.path.join(self.get_script_folder(), 'leaderboard\\names')): os.makedirs(os.path.join(self.get_script_folder(), 'leaderboard\\names'))
        if not os.path.exists(os.path.join(self.get_script_folder(), 'leaderboard\\ranks')): os.makedirs(os.path.join(self.get_script_folder(), 'leaderboard\\ranks'))
        if not os.path.exists(os.path.join(self.get_script_folder(), 'leaderboard\\scores')): os.makedirs(os.path.join(self.get_script_folder(), 'leaderboard\\scores'))

        self.error_window = None
        self.shortcuts_window = None
        self.about_window = None

        self.menuBarFrame = MenuBarFrame(master=self, app_ref=self)
        self.menuBarFrame.configure(fg_color=("#dbdbdb", "#2b2b2b"), corner_radius=0)

        self.currentPage = "Settings"
        self.SettingsFrame = OuterFrameForSettings(master=self, app_ref=self)
        self.showSettingsFrame()
        self.SettingsFrame.SettingsScrollableFrame.skipSettingsIfTrue()
        
        #focus the Entry Box for Number of Columns
        self.bind("<Map>", lambda event: self.SettingsFrame.SettingsScrollableFrame.columns_Entry.focus_set())
    
    def showSettingsFrame(self):
        self.menuBarFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nwe")
        self.SettingsFrame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.setButtonStatesAndValuesOnShowingSettings()
        self.currentPage = "Settings"
        self.title("Scoreboard")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def setButtonStatesAndValuesOnShowingSettings(self):
        self.SettingsFrame.SettingsScrollableFrame.columns_Entry.configure(state="normal")

        if self.SettingsFrame.SettingsScrollableFrame.customRow1_Type.get() == "+ custom": self.SettingsFrame.SettingsScrollableFrame.customRow1Parameter_Entry.configure(state="normal")
        else: self.SettingsFrame.SettingsScrollableFrame.customRow1Parameter_Entry.configure(state="readonly")

        if self.SettingsFrame.SettingsScrollableFrame.customRow2_Type.get() == "+ custom": self.SettingsFrame.SettingsScrollableFrame.customRow2Parameter_Entry.configure(state="normal")
        else: self.SettingsFrame.SettingsScrollableFrame.customRow2Parameter_Entry.configure(state="readonly")

        self.SettingsFrame.SettingsScrollableFrame.doFreezeLeaderboard_Switch.configure(variable=self.SettingsFrame.SettingsScrollableFrame.doFreezeLeaderboard_Var)
    
    def showWorkFrames(self, columns_Var):
        self.CounterFrame = Counter(master=self, num_columns=columns_Var)
        self.CounterFrame.grid(row=0, column=0, padx=10, pady=2, sticky="nsew")
        self.ControlsFrame = Controls(master=self)
        self.ControlsFrame.grid(row=1, column=0, padx=10, pady=2, sticky="nsew")

        self.SettingsFrame.SettingsScrollableFrame.columns_Entry.configure(state="readonly")
        self.SettingsFrame.SettingsScrollableFrame.customRow1Parameter_Entry.configure(state="readonly")
        self.SettingsFrame.SettingsScrollableFrame.customRow2Parameter_Entry.configure(state="readonly")

        self.currentPage = "Counter"

        #configure
        self.rowconfigure(0, weight=20)
        self.rowconfigure(1, weight=1)

        with open(self.SettingsFrame.SettingsScrollableFrame.settingsFilePath, 'r') as f:
            data = json.load(f)
        if self.SettingsFrame.SettingsScrollableFrame.activePreset != "":
            self.title("Scoreboard [" + data["presets"][str(self.SettingsFrame.SettingsScrollableFrame.activePreset)]["name"] +"]")
    
    def hideSettingsFrame(self):
        self.SettingsFrame.grid_forget()
        self.menuBarFrame.grid_forget()

    def hideWorkFrames(self):
        self.CounterFrame.grid_forget()
        self.ControlsFrame.grid_forget()

    def set_always_on_top(self, state):
        if state:
            self.wm_attributes("-topmost", True)
        else:
            self.wm_attributes("-topmost", False)

    def get_script_folder(self):
        # path of main .py or .exe when converted with pyinstaller
        if getattr(sys, 'frozen', False):
            script_path = os.path.dirname(sys.executable)
        else:
            script_path = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        return script_path

    def open_errorWindow(self, app_ref, msg, type):
        if self.error_window is None or not self.error_window.winfo_exists():
            self.error_window = ErrorWindow(app_ref, message=msg, type=type)  # create window if its None or destroyed
        else:
            self.error_window.focus()  # if window exists focus it
        self.error_window.attributes("-topmost", True)

        self.error_window.wait_window()
        if (self.error_window.action == "quit"):
            quit()
        elif (self.error_window.action == "reset"):
            quit()
        elif (self.error_window.action == "exit"):
            self.error_window.destroy()
            self.error_window = None


    def openShortcutsWindow(self, app_ref):
        if self.shortcuts_window is None or not self.shortcuts_window.winfo_exists():
            self.shortcuts_window = ShortcutsWindow(app_ref)  # create window if its None or destroyed
        self.shortcuts_window.attributes("-topmost", True)
        self.after(100, lambda: self.shortcuts_window.focus())

    def openAboutWindow(self, app_ref):
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = AboutWindow(app_ref)  # create window if its None or destroyed
        self.about_window.attributes("-topmost", True)
        self.after(100, lambda: self.about_window.focus())



def disallowClosing():
    pass

app = App()
app.mainloop()