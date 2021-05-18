import requests
import json
from datetime import datetime, timedelta  
from random import randint
from time import sleep
import os
import pickle

__version__ = "0.1"
__author__ = "SBP"

URL_GET_STATE_CODES = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
URL_GET_DIST_COES = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}"
URL_GET_FIND_PIN = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date}"
URL_GET_FIND_DST = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={dst_id}&date={date}"

HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
PATH_VACCINE_NAMES = "./.fmv_vaccine_names.dat"

REFRESH_INTERVAL_MIN = 4 # Choice is arbitrary!
REFRESH_INTERVAL_MAX = 13 # Choice is arbitrary!

if os.path.exists(PATH_VACCINE_NAMES):
    VACCINE_NAMES = pickle.load(open(PATH_VACCINE_NAMES, "rb"))
else:
    VACCINE_NAMES = ["Covishield", "Covaxin"]
    pickle.dump(VACCINE_NAMES, open(PATH_VACCINE_NAMES, "wb"))

def testConnection():
    resp = requests.get(URL_GET_STATE_CODES, headers=HEADERS)
    return resp.status_code == 200

def getStateCodes():
    resp = requests.get(URL_GET_STATE_CODES, headers=HEADERS)
    if resp.status_code != 200:
        raise Exception("Server not reachable!")
    
    resp_dict = json.loads(resp.text)
    states = resp_dict["states"]
    state_id2name = dict()
    state_name2id = dict()
    for elem in states:
        state_id2name.update({elem["state_id"]:elem["state_name"]})
        # state_name2id.update({elem["state_name"]:elem["state_id"]})
    return state_id2name

def getDistrictCodes(state_id: int):
    url = URL_GET_DIST_COES.replace("{state_id}",str(state_id))
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        raise Exception("PROBLEM: Server not reachable!")
    
    resp_dict = json.loads(resp.text)
    dists = resp_dict["districts"]
    dist_id2name = dict()
    dist_name2id = dict()
    for elem in dists:
        dist_id2name.update({elem["district_id"]:elem["district_name"]})
        # dist_name2id.update({elem["district_name"]:elem["district_id"]})
    return dist_id2name

def isPinValid(pin: str):
    if type(pin) != str:
        return False
    if len(pin) !=6:
        return False
    return pin.isnumeric()


def getCentersByPin(pin: str, startdate: datetime, weeks=1, randomize=True):
    if not isPinValid(pin):
        raise Exception("PROBLEM:Invalid PIN")
    
    if type(startdate) != datetime:
        return []
    
    center_list = []
    dates = [(startdate+timedelta(days=7*i)).strftime("%d-%m-%Y") for i in range(weeks)]
    for idx, date in enumerate(dates):
        url = URL_GET_FIND_PIN.replace("{pin}",pin)
        url = url.replace("{date}",date)
        
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code !=200:
            raise Exception("PROBLEM: Server not reachable!")
        
        resp_dict = json.loads(resp.text)
        centers = resp_dict.get("centers",[])
        center_list.extend(centers)
        
        # Prevent blacklisting, add random delay before next request
        if randomize and idx < len(dates)-1:
            sleep(randint(REFRESH_INTERVAL_MIN, REFRESH_INTERVAL_MAX))
    return center_list

def getCentersByDist(district_id: str, startdate: datetime, weeks=1, randomize=True):
    if type(startdate) != datetime:
        return []
    
    center_list = []
    dates = [(startdate+timedelta(days=7*i)).strftime("%d-%m-%Y") for i in range(weeks)]
    for idx, date in enumerate(dates):
        url = URL_GET_FIND_DST.replace("{dst_id}",district_id)
        url = url.replace("{date}",date)
        
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code !=200:
            raise Exception("PROBLEM: Server not reachable!")
        
        resp_dict = json.loads(resp.text)
        centers = resp_dict.get("centers",[])
        center_list.extend(centers)
        
        # Prevent blacklisting, add random delay before next request
        if randomize and idx < len(dates)-1:
            sleep(randint(REFRESH_INTERVAL_MIN, REFRESH_INTERVAL_MAX))
    return center_list

def filterSessions(center_list: list, age: int, vaccine_name: str, exclude_list: list):
    vaccine_name = vaccine_name.lower()
    slots = []
    exclude_list = list(map(str.lower,exclude_list))
    vaccine_names = list(map(str.lower,VACCINE_NAMES))
    
    for center in center_list:
        sessions = center["sessions"]
        for session in sessions:
            if center["name"].lower() in exclude_list:
                continue
            
            if vaccine_name == "any":
                matched_vaccine = True
            elif vaccine_name == "other":
                matched_vaccine = all([(elem not in center["name"].lower()) and (elem not in session["vaccine"].lower()) for elem in vaccine_names])
            else:
                matched_vaccine = ((vaccine_name in center["name"].lower()) or (vaccine_name in session["vaccine"].lower()))
            
            matched_age = True if session["min_age_limit"] <= age else False
            
            if (matched_vaccine and matched_age and session["available_capacity"]>0):
                slots.append({"name":center["name"], 
                              "address": center["address"], 
                              "pin":center["pincode"],
                              "date": session["date"],
                              "remaining": session["available_capacity"],
                              "fee":"free" if center["fee_type"]=="Free" else "paid",
                              "vaccine": session["vaccine"]
                              })
    return slots