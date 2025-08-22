#request
import requests as r


# UI related
import tkinter as tk
from tkinter import messagebox

#Utils
import os
import json

GeoBlockURL = "https://raw.githubusercontent.com/ItsMeDevRoland/NexulonNetworkIntPage/refs/heads/main/GeoBlocklisted.json"
IPLinkProvider = "http://ip-api.com/json/"
ApplicationName = "GeoBlocker"

filename = os.path.basename(GeoBlockURL)

UpdatedGeoBlacklist = None #empty for now
HasUpdatedGeoBlacklist = False

WhatNationIsTheUser = None

#for performance, ensure one loop is only triggered
HasTriggered = False


#-===========STEP 1=================-#
def InitializeTheBlocker():
    print("GeoBlocker is initated, We'll finish shortly : STEP 1'")
    if HasUpdatedGeoBlacklist == False:
        response = r.get(GeoBlockURL)
        if response.status_code == 200:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            UpdateGeoBlacklistFunction()
        else:
            tk.messagebox.showerror(ApplicationName, "Error, the Geoblocker Has hi an invalid error, This error returns a value 'Sebastian', Report to the Dev if this is a mistake")
            return None
    else:
        tk.messagebox.showerror(ApplicationName, "An Invalid Error occured, GeoBlocker has Initialized Again, This is not How you use GeoBlocker API, please read the documentations")
        return None

def UpdateGeoBlacklistFunction():
    global UpdatedGeoBlacklist, HasUpdatedGeoBlacklist
   # Step 2: Read/parse the JSON
    with open(filename, "r", encoding="utf-8") as f:
        UpdatedGeoBlacklist = json.load(f)
        HasUpdatedGeoBlacklist = True
    FinalCleanup()

def FinalCleanup():
    os.remove(filename)
    print("Successfully Update Definitions, The Second Step is now Initiated")
    ObtainUsersCountry()

#-===========STEP 2=================-#
def ObtainUsersCountry():
    print("Step 2 Started, Comparing Location")
    global WhatNationIsTheUser
    obtainedresponse = r.get(IPLinkProvider)
    jasonizedtheobtainedresponse = obtainedresponse.json()
    WhatNationIsTheUser = jasonizedtheobtainedresponse.get("countryCode")
    DecisionPoint()


#-===========STEP 3=================-#
def DecisionPoint():
    print("Step 3 Started")
    for i in UpdatedGeoBlacklist:
        if i == WhatNationIsTheUser:
            tk.messagebox.showerror(ApplicationName, "⚠️WARNING⚠️, \n Your Country Code is included on Our Blacklisted Nations! \n To Protect Our Service, we decided to Blacklist your nation: " + WhatNationIsTheUser + ", \n if this is a mistake, please remove your VPN or stop using this application")
            print("BLACKLISTED")
        else:
            print("SAFE")
            return None


#-===========Init=================-#
#loop lagic
if __name__ == "__main__":
    if HasTriggered == False:
        HasTriggered = True
        InitializeTheBlocker()
