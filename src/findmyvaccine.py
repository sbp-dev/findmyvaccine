
# -*- coding: utf-8 -*-
# %% Imports
import os, sys, pickle, json
from time import sleep
from random import randint
from datetime import datetime, timedelta  

import requests

from remi.gui import *
from remi import start, App

from playsound import playsound

from pycowin import *
from notify_run import Notify

__version__ = "0.1"
__author__ = "SBP"

# %% Globals 
PATH_EXCLUDED_CENTERS = "./.fmv_excluded_centers.dat"
REFRESH_INTERVAL_MIN = 300 # Reducing this number to less than 5 mins may lead to IP getting blocked!
REFRESH_INTERVAL_MAX = 900

# Find out if running as a packed executable or directly from script
PATH_RESOURCE_DIR = getattr(sys,"_MEIPASS", os.path.abspath(os.path.join(os.path.dirname(__file__),".resources")))

# %% GUI Class
class FindMyVaccine(App):
    def __init__(self, *args, **kwargs):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        if not 'editing_mode' in kwargs.keys():
            super(FindMyVaccine, self).__init__(*args, static_file_path={'my_res':'./res/'})
        
    @staticmethod
    def construct_ui(self):
        #DON'T MAKE CHANGES HERE, THIS METHOD GETS OVERWRITTEN WHEN SAVING IN THE EDITOR
        containerMain = Container()
        containerMain.attr_class = "Container"
        containerMain.attr_editor_newclass = False
        containerMain.css_height = "720px"
        containerMain.css_left = "0.0px"
        containerMain.css_position = "absolute"
        containerMain.css_top = "0.0px"
        containerMain.css_width = "580px"
        containerMain.variable_name = "containerMain"
        containerSearch = Container()
        containerSearch.attr_class = "Container"
        containerSearch.attr_editor_newclass = False
        containerSearch.css_height = "700px"
        containerSearch.css_left = "0.0px"
        containerSearch.css_position = "absolute"
        containerSearch.css_top = "20px"
        containerSearch.css_visibility = "visible"
        containerSearch.css_width = "580px"
        containerSearch.variable_name = "containerSearch"
        imageBanner = Image()
        imageBanner.attr_class = "Image"
        imageBanner.attr_editor_newclass = False
        imageBanner.attr_src = ""
        imageBanner.css_height = "220.0px"
        imageBanner.css_left = "10.0px"
        imageBanner.css_position = "absolute"
        imageBanner.css_top = "10.0px"
        imageBanner.css_width = "560px"
        imageBanner.variable_name = "imageBanner"
        containerSearch.append(imageBanner,'imageBanner')
        textinputResults = TextInput()
        textinputResults.attr_class = "TextInput"
        textinputResults.attr_editor_newclass = False
        textinputResults.attr_maxlength = "10000"
        textinputResults.attr_title = "If a center is too far, you can copy it's name from here and paste on the exclusion text box."
        textinputResults.css_border_color = "rgb(77,187,247)"
        textinputResults.css_border_radius = "12px"
        textinputResults.css_border_style = "solid"
        textinputResults.css_border_width = "1px"
        textinputResults.css_font_size = "9px"
        textinputResults.css_height = "260px"
        textinputResults.css_left = "310.0px"
        textinputResults.css_position = "absolute"
        textinputResults.css_top = "430px"
        textinputResults.css_width = "260.0px"
        textinputResults.text = ""
        textinputResults.variable_name = "textinputResults"
        containerSearch.append(textinputResults,'textinputResults')
        containerFinish = Container()
        containerFinish.attr_class = "Container"
        containerFinish.attr_editor_newclass = False
        containerFinish.css_border_color = "rgb(77,187,247)"
        containerFinish.css_border_radius = "12px"
        containerFinish.css_border_style = "solid"
        containerFinish.css_border_width = "1px"
        containerFinish.css_height = "130.0px"
        containerFinish.css_left = "10.0px"
        containerFinish.css_position = "absolute"
        containerFinish.css_top = "430.0px"
        containerFinish.css_width = "290.0px"
        containerFinish.variable_name = "containerFinish"
        label8 = Label()
        label8.attr_class = "Label"
        label8.attr_editor_newclass = False
        label8.css_background_color = "rgb(255,255,255)"
        label8.css_font_style = "italic"
        label8.css_font_weight = "700"
        label8.css_height = "20.0px"
        label8.css_left = "10.0px"
        label8.css_position = "absolute"
        label8.css_text_align = "center"
        label8.css_top = "-10.0px"
        label8.css_width = "100.0px"
        label8.text = " When finished: "
        label8.variable_name = "label8"
        containerFinish.append(label8,'label8')
        checkboxlabelNotify = CheckBoxLabel()
        checkboxlabelNotify.attr_class = "CheckBoxLabel"
        checkboxlabelNotify.attr_editor_newclass = False
        checkboxlabelNotify.attr_title = "EXPERIMENTAL! Uses browser based notification services by notify.run. You can use this if you have Chrome or Mozila mobile browsers on your Android / iOS device."
        checkboxlabelNotify.css_align_items = "center"
        checkboxlabelNotify.css_display = "flex"
        checkboxlabelNotify.css_flex_direction = "row"
        checkboxlabelNotify.css_height = "20.0px"
        checkboxlabelNotify.css_justify_content = "space-around"
        checkboxlabelNotify.css_left = "10.0px"
        checkboxlabelNotify.css_position = "absolute"
        checkboxlabelNotify.css_top = "80.0px"
        checkboxlabelNotify.css_width = "130.0px"
        checkboxlabelNotify.text = "Notify on mobile"
        checkboxlabelNotify.variable_name = "checkboxlabelNotify"
        containerFinish.append(checkboxlabelNotify,'checkboxlabelNotify')
        checkboxlabelSound = CheckBoxLabel()
        checkboxlabelSound.attr_class = "CheckBoxLabel"
        checkboxlabelSound.attr_editor_newclass = False
        checkboxlabelSound.css_align_items = "center"
        checkboxlabelSound.css_display = "flex"
        checkboxlabelSound.css_flex_direction = "row"
        checkboxlabelSound.css_height = "20.0px"
        checkboxlabelSound.css_justify_content = "space-around"
        checkboxlabelSound.css_left = "10.0px"
        checkboxlabelSound.css_position = "absolute"
        checkboxlabelSound.css_top = "50.0px"
        checkboxlabelSound.css_width = "150.0px"
        checkboxlabelSound.text = "Play an alert sound"
        checkboxlabelSound.variable_name = "checkboxlabelSound"
        containerFinish.append(checkboxlabelSound,'checkboxlabelSound')
        imageSpeaker = Image()
        imageSpeaker.attr_class = "Image"
        imageSpeaker.attr_editor_newclass = False
        imageSpeaker.attr_src = ""
        imageSpeaker.attr_title = "Click to test how it sounds"
        imageSpeaker.css_height = "20.0px"
        imageSpeaker.css_left = "159px"
        imageSpeaker.css_position = "absolute"
        imageSpeaker.css_top = "50.0px"
        imageSpeaker.css_width = "20.0px"
        imageSpeaker.variable_name = "imageSpeaker"
        containerFinish.append(imageSpeaker,'imageSpeaker')
        checkboxlabelFileSave = CheckBoxLabel()
        checkboxlabelFileSave.attr_class = "CheckBoxLabel"
        checkboxlabelFileSave.attr_editor_newclass = False
        checkboxlabelFileSave.attr_title = "A text file will be created in the same location where this app is running from. The name of the file will have the date and time when search finished."
        checkboxlabelFileSave.css_align_items = "center"
        checkboxlabelFileSave.css_display = "flex"
        checkboxlabelFileSave.css_flex_direction = "row"
        checkboxlabelFileSave.css_height = "20.0px"
        checkboxlabelFileSave.css_justify_content = "space-around"
        checkboxlabelFileSave.css_left = "10.0px"
        checkboxlabelFileSave.css_position = "absolute"
        checkboxlabelFileSave.css_top = "20px"
        checkboxlabelFileSave.css_width = "160.0px"
        checkboxlabelFileSave.text = "Save results to a file"
        checkboxlabelFileSave.variable_name = "checkboxlabelFileSave"
        containerFinish.append(checkboxlabelFileSave,'checkboxlabelFileSave')
        imageQR = Image()
        imageQR.attr_class = "Image"
        imageQR.attr_editor_newclass = False
        imageQR.attr_src = ""
        imageQR.attr_title = "Scan this QR code from your mobile device. Open the link with Chrome / Mozilla mobile browser.  Click on 'Subscribe on this device'. Finally, allow notifications."
        imageQR.css_height = "110px"
        imageQR.css_left = "179px"
        imageQR.css_position = "inherit"
        imageQR.css_top = "10.0px"
        imageQR.css_width = "110px"
        imageQR.variable_name = "imageQR"
        containerFinish.append(imageQR,'imageQR')
        linkNotifyRun = Link()
        linkNotifyRun.attr_class = "Link"
        linkNotifyRun.attr_editor_newclass = False
        linkNotifyRun.attr_href = "https://notify.run/pN8BQS3VT2Q3IaXr"
        linkNotifyRun.attr_title = "This auto-generated link is unique to your PC. Use this or the QR code to register mobile devices with notify.run service."
        linkNotifyRun.css_font_size = "9px"
        linkNotifyRun.css_height = "15.0px"
        linkNotifyRun.css_left = "13px"
        linkNotifyRun.css_position = "absolute"
        linkNotifyRun.css_top = "105.0px"
        linkNotifyRun.css_width = "180.0px"
        linkNotifyRun.text = "https://notify.run/pN8BQS3VT2Q3IaXr"
        linkNotifyRun.variable_name = "linkNotifyRun"
        containerFinish.append(linkNotifyRun,'linkNotifyRun')
        containerSearch.append(containerFinish,'containerFinish')
        buttonStartStop = Button()
        buttonStartStop.attr_class = "Button"
        buttonStartStop.attr_editor_newclass = False
        buttonStartStop.css_background_color = "rgb(75,215,75)"
        buttonStartStop.css_border_radius = "12px"
        buttonStartStop.css_font_size = "20px"
        buttonStartStop.css_font_weight = "bold"
        buttonStartStop.css_height = "60px"
        buttonStartStop.css_left = "10.0px"
        buttonStartStop.css_position = "absolute"
        buttonStartStop.css_top = "575px"
        buttonStartStop.css_width = "290.0px"
        buttonStartStop.text = "START"
        buttonStartStop.variable_name = "buttonStartStop"
        containerSearch.append(buttonStartStop,'buttonStartStop')
        containerFilter = Container()
        containerFilter.attr_class = "Container"
        containerFilter.attr_editor_newclass = False
        containerFilter.css_border_color = "rgb(77,187,247)"
        containerFilter.css_border_radius = "12px"
        containerFilter.css_border_style = "solid"
        containerFilter.css_border_width = "1px"
        containerFilter.css_height = "160.0px"
        containerFilter.css_left = "10px"
        containerFilter.css_position = "absolute"
        containerFilter.css_top = "250px"
        containerFilter.css_width = "560.0px"
        containerFilter.variable_name = "containerFilter"
        listviewLocation = ListView()
        listviewLocation.attr_class = "ListView"
        listviewLocation.attr_editor_newclass = False
        listviewLocation.css_height = "80.0px"
        listviewLocation.css_left = "10.0px"
        listviewLocation.css_position = "absolute"
        listviewLocation.css_top = "0.0px"
        listviewLocation.css_width = "110.0px"
        listviewLocation.variable_name = "listviewLocation"
        containerFilter.append(listviewLocation,'listviewLocation')
        containerPin = Container()
        containerPin.attr_class = "Container"
        containerPin.attr_editor_newclass = False
        containerPin.css_height = "80.0px"
        containerPin.css_left = "130.0px"
        containerPin.css_position = "absolute"
        containerPin.css_top = "15px"
        containerPin.css_visibility = "hidden"
        containerPin.css_width = "420.0px"
        containerPin.variable_name = "containerPin"
        textinputPinCodes = TextInput()
        textinputPinCodes.attr_class = "TextInput"
        textinputPinCodes.attr_editor_newclass = False
        textinputPinCodes.attr_maxlength = "6"
        textinputPinCodes.css_height = "20.0px"
        textinputPinCodes.css_left = "20.0px"
        textinputPinCodes.css_position = "absolute"
        textinputPinCodes.css_top = "20.0px"
        textinputPinCodes.css_width = "70.0px"
        textinputPinCodes.text = ""
        textinputPinCodes.variable_name = "textinputPinCodes"
        containerPin.append(textinputPinCodes,'textinputPinCodes')
        label0 = Label()
        label0.attr_class = "Label"
        label0.attr_editor_newclass = False
        label0.css_height = "20.0px"
        label0.css_left = "20.0px"
        label0.css_position = "absolute"
        label0.css_top = "0.0px"
        label0.css_width = "60.0px"
        label0.text = "Enter PIN"
        label0.variable_name = "label0"
        containerPin.append(label0,'label0')
        containerFilter.append(containerPin,'containerPin')
        label7 = Label()
        label7.attr_class = "Label"
        label7.attr_editor_newclass = False
        label7.css_background_color = "rgb(255,255,255)"
        label7.css_font_style = "italic"
        label7.css_font_weight = "bold"
        label7.css_height = "20.0px"
        label7.css_left = "10.0px"
        label7.css_position = "absolute"
        label7.css_top = "-10.0px"
        label7.css_width = "90.0px"
        label7.text = " Search filters: "
        label7.variable_name = "label7"
        containerFilter.append(label7,'label7')
        containerDist = Container()
        containerDist.attr_class = "Container"
        containerDist.attr_editor_newclass = False
        containerDist.css_height = "80.0px"
        containerDist.css_left = "130.0px"
        containerDist.css_position = "absolute"
        containerDist.css_top = "15px"
        containerDist.css_visibility = "hidden"
        containerDist.css_width = "420.0px"
        containerDist.variable_name = "containerDist"
        label1 = Label()
        label1.attr_class = "Label"
        label1.attr_editor_newclass = False
        label1.css_height = "20.0px"
        label1.css_left = "20px"
        label1.css_position = "absolute"
        label1.css_top = "0px"
        label1.css_width = "80.0px"
        label1.text = "Select state"
        label1.variable_name = "label1"
        containerDist.append(label1,'label1')
        dropdownState = DropDown()
        dropdownState.attr_class = "DropDown"
        dropdownState.attr_editor_newclass = False
        dropdownState.css_height = "30.0px"
        dropdownState.css_left = "20.0px"
        dropdownState.css_position = "absolute"
        dropdownState.css_top = "20.0px"
        dropdownState.css_width = "160.0px"
        dropdownState.variable_name = "dropdownState"
        containerDist.append(dropdownState,'dropdownState')
        label2 = Label()
        label2.attr_class = "Label"
        label2.attr_editor_newclass = False
        label2.css_height = "20.0px"
        label2.css_left = "200.0px"
        label2.css_position = "absolute"
        label2.css_top = "0.0px"
        label2.css_width = "100.0px"
        label2.text = "Select district"
        label2.variable_name = "label2"
        containerDist.append(label2,'label2')
        dropdownDistrict = DropDown()
        dropdownDistrict.attr_class = "DropDown"
        dropdownDistrict.attr_editor_newclass = False
        dropdownDistrict.css_height = "30.0px"
        dropdownDistrict.css_left = "200.0px"
        dropdownDistrict.css_position = "absolute"
        dropdownDistrict.css_top = "20.0px"
        dropdownDistrict.css_width = "220.0px"
        dropdownDistrict.variable_name = "dropdownDistrict"
        containerDist.append(dropdownDistrict,'dropdownDistrict')
        containerFilter.append(containerDist,'containerDist')
        containerExclude = Container()
        containerExclude.attr_class = "Container"
        containerExclude.attr_editor_newclass = False
        containerExclude.css_height = "80.0px"
        containerExclude.css_left = "130.0px"
        containerExclude.css_position = "absolute"
        containerExclude.css_top = "15px"
        containerExclude.css_visibility = "hidden"
        containerExclude.css_width = "420px"
        containerExclude.variable_name = "containerExclude"
        textinputExclusions = TextInput()
        textinputExclusions.attr_class = "TextInput"
        textinputExclusions.attr_editor_newclass = False
        textinputExclusions.attr_maxlength = "2000"
        textinputExclusions.attr_title = "You might want to use this feature if you know that certain centers are too far away. Copy-paste the names of such centers from the 'RESULTS' window below. Use comma to separate multiple center names."
        textinputExclusions.css_font_size = "9px"
        textinputExclusions.css_height = "50.0px"
        textinputExclusions.css_left = "20px"
        textinputExclusions.css_position = "absolute"
        textinputExclusions.css_top = "20px"
        textinputExclusions.css_width = "400.0px"
        textinputExclusions.text = ""
        textinputExclusions.variable_name = "textinputExclusions"
        containerExclude.append(textinputExclusions,'textinputExclusions')
        label3 = Label()
        label3.attr_class = "Label"
        label3.attr_editor_newclass = False
        label3.css_height = "20.0px"
        label3.css_left = "20.0px"
        label3.css_position = "absolute"
        label3.css_top = "0.0px"
        label3.css_width = "210.0px"
        label3.text = "Enter center names to exclude"
        label3.variable_name = "label3"
        containerExclude.append(label3,'label3')
        checkboxlabelRemember = CheckBoxLabel()
        checkboxlabelRemember.attr_class = "CheckBoxLabel"
        checkboxlabelRemember.attr_editor_newclass = False
        checkboxlabelRemember.attr_title = "If this is checked, the center names provided below will be stored when you click the 'START' button. Next time you run this app, these center names will be automatically populated here and excluded from the search."
        checkboxlabelRemember.css_align_items = "center"
        checkboxlabelRemember.css_display = "flex"
        checkboxlabelRemember.css_flex_direction = "row"
        checkboxlabelRemember.css_height = "20.0px"
        checkboxlabelRemember.css_justify_content = "flex-start"
        checkboxlabelRemember.css_left = "320.0px"
        checkboxlabelRemember.css_position = "absolute"
        checkboxlabelRemember.css_top = "0.0px"
        checkboxlabelRemember.css_width = "100.0px"
        checkboxlabelRemember.text = "Remember"
        checkboxlabelRemember.variable_name = "checkboxlabelRemember"
        containerExclude.append(checkboxlabelRemember,'checkboxlabelRemember')
        containerFilter.append(containerExclude,'containerExclude')
        dropdownVaccine = DropDown()
        dropdownVaccine.attr_class = "DropDown"
        dropdownVaccine.attr_editor_newclass = False
        dropdownVaccine.attr_title = "WARNING: You are solely responsible for choosing the correct vaccine, especially for 2nd shot."
        dropdownVaccine.css_height = "30.0px"
        dropdownVaccine.css_left = "150.0px"
        dropdownVaccine.css_position = "absolute"
        dropdownVaccine.css_top = "120.0px"
        dropdownVaccine.css_width = "210.0px"
        dropdownVaccine.variable_name = "dropdownVaccine"
        containerFilter.append(dropdownVaccine,'dropdownVaccine')
        labelVaccine = Label()
        labelVaccine.attr_class = "Label"
        labelVaccine.attr_editor_newclass = False
        labelVaccine.css_height = "20.0px"
        labelVaccine.css_left = "150.0px"
        labelVaccine.css_position = "absolute"
        labelVaccine.css_top = "100.0px"
        labelVaccine.css_width = "110.0px"
        labelVaccine.text = "Vaccine name"
        labelVaccine.variable_name = "labelVaccine"
        containerFilter.append(labelVaccine,'labelVaccine')
        labelAge = Label()
        labelAge.attr_class = "Label"
        labelAge.attr_editor_newclass = False
        labelAge.css_height = "20.0px"
        labelAge.css_left = "390.0px"
        labelAge.css_position = "absolute"
        labelAge.css_top = "100.0px"
        labelAge.css_width = "70.0px"
        labelAge.text = "Age"
        labelAge.variable_name = "labelAge"
        containerFilter.append(labelAge,'labelAge')
        dropdownAge = DropDown()
        dropdownAge.attr_class = "DropDown"
        dropdownAge.attr_editor_newclass = False
        dropdownAge.attr_title = "Enter your age group. E.g. if you are 50 years old, select 45+. All centers with minimum age 18 and 45 will be shown."
        dropdownAge.css_height = "30.0px"
        dropdownAge.css_left = "390.0px"
        dropdownAge.css_position = "absolute"
        dropdownAge.css_top = "120.0px"
        dropdownAge.css_width = "80.0px"
        dropdownAge.variable_name = "dropdownAge"
        containerFilter.append(dropdownAge,'dropdownAge')
        labelWeeks = Label()
        labelWeeks.attr_class = "Label"
        labelWeeks.attr_editor_newclass = False
        labelWeeks.css_height = "20.0px"
        labelWeeks.css_left = "500.0px"
        labelWeeks.css_position = "absolute"
        labelWeeks.css_top = "100.0px"
        labelWeeks.css_width = "50.0px"
        labelWeeks.text = "Weeks"
        labelWeeks.variable_name = "labelWeeks"
        containerFilter.append(labelWeeks,'labelWeeks')
        dropdownWeeks = DropDown()
        dropdownWeeks.attr_class = "DropDown"
        dropdownWeeks.attr_editor_newclass = False
        dropdownWeeks.attr_title = "For how many weeks starting today do you want to search for vaccines?"
        dropdownWeeks.css_height = "30.0px"
        dropdownWeeks.css_left = "500.0px"
        dropdownWeeks.css_position = "absolute"
        dropdownWeeks.css_top = "120.0px"
        dropdownWeeks.css_width = "50.0px"
        dropdownWeeks.variable_name = "dropdownWeeks"
        containerFilter.append(dropdownWeeks,'dropdownWeeks')
        containerSearch.append(containerFilter,'containerFilter')
        labelResults = Label()
        labelResults.attr_class = "Label"
        labelResults.attr_editor_newclass = False
        labelResults.css_background_color = "rgb(255,255,255)"
        labelResults.css_font_style = "italic"
        labelResults.css_font_weight = "bold"
        labelResults.css_height = "20.0px"
        labelResults.css_left = "320.0px"
        labelResults.css_position = "absolute"
        labelResults.css_text_align = "center"
        labelResults.css_top = "420px"
        labelResults.css_width = "70.0px"
        labelResults.text = " RESULTS: "
        labelResults.variable_name = "labelResults"
        containerSearch.append(labelResults,'labelResults')
        labelStatus = Label()
        labelStatus.attr_class = "Label"
        labelStatus.attr_editor_newclass = False
        labelStatus.css_font_size = "12px"
        labelStatus.css_font_style = "italic"
        labelStatus.css_height = "50.0px"
        labelStatus.css_left = "10px"
        labelStatus.css_position = "absolute"
        labelStatus.css_top = "640.0px"
        labelStatus.css_visibility = "hidden"
        labelStatus.css_width = "290px"
        labelStatus.text = "Status:"
        labelStatus.variable_name = "labelStatus"
        containerSearch.append(labelStatus,'labelStatus')
        containerMain.append(containerSearch,'containerSearch')
        containerAbout = Container()
        containerAbout.attr_class = "Container"
        containerAbout.attr_editor_newclass = False
        containerAbout.css_height = "700px"
        containerAbout.css_left = "0.0px"
        containerAbout.css_position = "absolute"
        containerAbout.css_top = "20px"
        containerAbout.css_visibility = "hidden"
        containerAbout.css_width = "580px"
        containerAbout.variable_name = "containerAbout"
        imageBanner = Image()
        imageBanner.attr_class = "Image"
        imageBanner.attr_editor_newclass = False
        imageBanner.attr_src = ""
        imageBanner.css_height = "220px"
        imageBanner.css_left = "10px"
        imageBanner.css_position = "absolute"
        imageBanner.css_top = "10px"
        imageBanner.css_width = "560px"
        imageBanner.variable_name = "imageBanner"
        containerAbout.append(imageBanner,'imageBanner')
        containerInfo = Container()
        containerInfo.attr_class = "Container"
        containerInfo.attr_editor_newclass = False
        containerInfo.css_border_color = "rgb(77,187,247)"
        containerInfo.css_border_radius = "12px"
        containerInfo.css_border_style = "solid"
        containerInfo.css_border_width = "1px"
        containerInfo.css_height = "180.0px"
        containerInfo.css_left = "10.0px"
        containerInfo.css_position = "absolute"
        containerInfo.css_top = "250.0px"
        containerInfo.css_width = "560.0px"
        containerInfo.variable_name = "containerInfo"
        label6 = Label()
        label6.attr_class = "Label"
        label6.attr_editor_newclass = False
        label6.css_height = "100.0px"
        label6.css_left = "10.0px"
        label6.css_position = "absolute"
        label6.css_text_align = "justify"
        label6.css_top = "30.0px"
        label6.css_width = "540.0px"
        label6.text = "This app checks for availability of vaccines in India at regular intervals (every 5-15 mins). It stops automatically when slots are found and can alert you in different ways. If you find eligible vaccination slots, please book immediately using CoWin portal or Aarogya Setu app. This is an open source, personal project based on open APIs provided by API Setu initiative of Government of India. Contributions are welcome!"
        label6.variable_name = "label6"
        containerInfo.append(label6,'label6')
        label4 = Label()
        label4.attr_class = "Label"
        label4.attr_editor_newclass = False
        label4.css_background_color = "rgb(255,255,255)"
        label4.css_font_style = "italic"
        label4.css_font_weight = "bold"
        label4.css_height = "20.0px"
        label4.css_left = "10px"
        label4.css_position = "absolute"
        label4.css_text_align = "center"
        label4.css_top = "-10px"
        label4.css_width = "40.0px"
        label4.text = "Info:"
        label4.variable_name = "label4"
        containerInfo.append(label4,'label4')
        label5 = Label()
        label5.attr_class = "Label"
        label5.attr_editor_newclass = False
        label5.css_height = "20.0px"
        label5.css_left = "10.0px"
        label5.css_position = "absolute"
        label5.css_top = "130.0px"
        label5.css_width = "170.0px"
        label5.text = "Source code, updates, etc."
        label5.variable_name = "label5"
        containerInfo.append(label5,'label5')
        linkGithub = Link()
        linkGithub.attr_class = "Link"
        linkGithub.attr_editor_newclass = False
        linkGithub.attr_href = "https://github.com/sbp-dev/findmyvaccine"
        linkGithub.css_height = "20.0px"
        linkGithub.css_left = "240.0px"
        linkGithub.css_position = "absolute"
        linkGithub.css_top = "130.0px"
        linkGithub.css_width = "280.0px"
        linkGithub.text = "https://github.com/sbp-dev/findmyvaccine"
        linkGithub.variable_name = "linkGithub"
        containerInfo.append(linkGithub,'linkGithub')
        label9 = Label()
        label9.attr_class = "Label"
        label9.attr_editor_newclass = False
        label9.css_height = "20.0px"
        label9.css_left = "10.0px"
        label9.css_position = "absolute"
        label9.css_top = "150.0px"
        label9.css_width = "230.0px"
        label9.text = "Report issues, request features, etc."
        label9.variable_name = "label9"
        containerInfo.append(label9,'label9')
        linkIssues = Link()
        linkIssues.attr_class = "Link"
        linkIssues.attr_editor_newclass = False
        linkIssues.attr_href = "https://github.com/sbp-dev/findmyvaccine/issues"
        linkIssues.css_height = "20.0px"
        linkIssues.css_left = "240.0px"
        linkIssues.css_position = "absolute"
        linkIssues.css_top = "150.0px"
        linkIssues.css_width = "320.0px"
        linkIssues.text = "https://github.com/sbp-dev/findmyvaccine/issues"
        linkIssues.variable_name = "linkIssues"
        containerInfo.append(linkIssues,'linkIssues')
        labelVersion = Label()
        labelVersion.attr_class = "Label"
        labelVersion.attr_editor_newclass = False
        labelVersion.css_font_style = "italic"
        labelVersion.css_font_weight = "bold"
        labelVersion.css_height = "15.0px"
        labelVersion.css_left = "10.0px"
        labelVersion.css_position = "absolute"
        labelVersion.css_top = "10.0px"
        labelVersion.css_width = "255.0px"
        labelVersion.text = "FindMyVaccine (version 0.1)"
        labelVersion.variable_name = "labelVersion"
        containerInfo.append(labelVersion,'labelVersion')
        containerAbout.append(containerInfo,'containerInfo')
        containerAttributions = Container()
        containerAttributions.attr_class = "Container"
        containerAttributions.attr_editor_newclass = False
        containerAttributions.css_border_color = "rgb(77,187,247)"
        containerAttributions.css_border_radius = "12px"
        containerAttributions.css_border_style = "solid"
        containerAttributions.css_border_width = "1px"
        containerAttributions.css_height = "239px"
        containerAttributions.css_left = "10.0px"
        containerAttributions.css_position = "absolute"
        containerAttributions.css_top = "450px"
        containerAttributions.css_width = "560.0px"
        containerAttributions.variable_name = "containerAttributions"
        label11 = Label()
        label11.attr_class = "Label"
        label11.attr_editor_newclass = False
        label11.css_background_color = "rgb(255,255,255)"
        label11.css_font_style = "italic"
        label11.css_font_weight = "bold"
        label11.css_height = "20.0px"
        label11.css_left = "10px"
        label11.css_position = "absolute"
        label11.css_text_align = "center"
        label11.css_top = "-10.0px"
        label11.css_width = "80.0px"
        label11.text = "Attributions:"
        label11.variable_name = "label11"
        containerAttributions.append(label11,'label11')
        link2 = Link()
        link2.attr_class = "Link"
        link2.attr_editor_newclass = False
        link2.attr_href = "https://www.freepik.com/free-vector/vaccine-concept-illustration_13104643.htm"
        link2.css_height = "20.0px"
        link2.css_left = "10.0px"
        link2.css_position = "absolute"
        link2.css_top = "10.0px"
        link2.css_width = "540.0px"
        link2.text = "Banner image credits: People vector created by stories - www.freepik.com"
        link2.variable_name = "link2"
        containerAttributions.append(link2,'link2')
        link4 = Link()
        link4.attr_class = "Link"
        link4.attr_editor_newclass = False
        link4.attr_href = "https://www.flaticon.com/free-icon/vaccine_3027535?term=vaccine&related_id=3027535"
        link4.css_height = "20.0px"
        link4.css_left = "10.0px"
        link4.css_position = "absolute"
        link4.css_top = "50.0px"
        link4.css_width = "460.0px"
        link4.text = "Application icon credits: mavadee from https://www.flaticon.com/"
        link4.variable_name = "link4"
        containerAttributions.append(link4,'link4')
        link5 = Link()
        link5.attr_class = "Link"
        link5.attr_editor_newclass = False
        link5.attr_href = "https://apisetu.gov.in/public/marketplace/api/cowin#/"
        link5.css_height = "20.0px"
        link5.css_left = "10.0px"
        link5.css_position = "absolute"
        link5.css_top = "70.0px"
        link5.css_width = "410.0px"
        link5.text = "Powered by API Setu"
        link5.variable_name = "link5"
        containerAttributions.append(link5,'link5')
        link0 = Link()
        link0.attr_class = "Link"
        link0.attr_editor_newclass = False
        link0.attr_href = "https://icons8.com/icon/12915/speaker"
        link0.css_height = "20.0px"
        link0.css_left = "10.0px"
        link0.css_position = "absolute"
        link0.css_top = "30.0px"
        link0.css_width = "460.0px"
        link0.text = "Speaker icon credits: icons8"
        link0.variable_name = "link0"
        containerAttributions.append(link0,'link0')
        containerAbout.append(containerAttributions,'containerAttributions')
        containerMain.append(containerAbout,'containerAbout')
        containerMain.children['containerSearch'].children['containerFinish'].children['checkboxlabelNotify'].onchange.do(self.onchange_checkboxlabelNotify)
        containerMain.children['containerSearch'].children['containerFinish'].children['imageSpeaker'].onclick.do(self.onclick_imageSpeaker)
        containerMain.children['containerSearch'].children['buttonStartStop'].onclick.do(self.onclick_buttonStartStop)
        containerMain.children['containerSearch'].children['containerFilter'].children['listviewLocation'].onselection.do(self.onselection_listviewLocation)
        containerMain.children['containerSearch'].children['containerFilter'].children['containerDist'].children['dropdownState'].onchange.do(self.onchange_dropdownState)
        containerMain.children['containerSearch'].children['containerFilter'].children['dropdownVaccine'].onchange.do(self.onchange_dropdownVaccine)
        

        self.containerMain = containerMain
        return self.containerMain


    def init_ui(self):
        #### Set favicon ####
        self.page.children['head'].set_icon_file(load_resource(os.path.join(PATH_RESOURCE_DIR,"vaccine_32px.png")))
        #### Internal states and objects ####
        self.isScanning = False
        
        #### Menu bar related initialization ####
        self.m1 = MenuItem('Search', width=100, height=30)
        self.m2 = MenuItem('About', width=100, height=30)
        menu = Menu(width='100%', height='30px')
        menu.append([self.m1, self.m2])
        menubar = MenuBar(width='100%', height='30px')
        menubar.append(menu)
        self.m1.css_background_color="rgb(50,150,230)"
        self.containerMain.append(menubar,"menubar")
        
        self.m1.onclick.do(self.onclick_m1)
        self.m2.onclick.do(self.onclick_m2)
        
        #### Notification service related ####
        self.notify = Notify()
        # Temporarily save SVG file
        self.notify.info()._qr().svg(os.path.join(PATH_RESOURCE_DIR,".temp_qr.svg")) if self.notify.config_file_exists else self.notify.register()._qr().svg(os.path.join(PATH_RESOURCE_DIR,".temp_qr.svg")) 
        
        #### Load all images ####
        self.containerMain.get_child("containerSearch").get_child("containerFinish").get_child("imageQR").attr_src=load_resource(os.path.join(PATH_RESOURCE_DIR,'.temp_qr.svg'))
        os.remove(os.path.join(PATH_RESOURCE_DIR,'.temp_qr.svg')) # Get rid of the temporary file as soon as its loaded!
        self.containerMain.get_child("containerSearch").get_child("containerFinish").get_child("imageSpeaker").attr_src=load_resource(os.path.join(PATH_RESOURCE_DIR,'speaker.PNG'))
        self.containerMain.get_child("containerSearch").get_child("imageBanner").attr_src=load_resource(os.path.join(PATH_RESOURCE_DIR,'5150374_2.jpg'))
        self.containerMain.get_child("containerAbout").get_child("imageBanner").attr_src=load_resource(os.path.join(PATH_RESOURCE_DIR,'5150374_2.jpg'))
        self.imageQR = self.containerMain.get_child("containerSearch").get_child("containerFinish").get_child("imageQR")
        
        #### Initialize dropdowns and other elements ####
        self.dropdownVaccine = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("dropdownVaccine")
        self.dropdownVaccine.append(VACCINE_NAMES+["Other", "Any"])
        
        self.dropdownAge = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("dropdownAge")
        self.dropdownAge.append({18:"18+", 45:"45+", 60:"60+"})
        
        self.dropdownWeeks = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("dropdownWeeks")
        self.dropdownWeeks.append({1:"1", 2:"2", 3:"3", 4:"4"})
        
        self.dropdownState = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("containerDist").get_child("dropdownState")
        self.textinputResults = self.containerMain.get_child("containerSearch").get_child("textinputResults")
        self.dropdownDistrict = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("containerDist").get_child("dropdownDistrict")
        self.textinputPinCodes = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("containerPin").get_child("textinputPinCodes")
        self.textinputExclusions = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("containerExclude").get_child("textinputExclusions")
        self.checkboxlabelRemember = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("containerExclude").get_child("checkboxlabelRemember")
        self.checkboxlabelFileSave = self.containerMain.get_child("containerSearch").get_child("containerFinish").get_child("checkboxlabelFileSave")
        self.checkboxlabelSound = self.containerMain.get_child("containerSearch").get_child("containerFinish").get_child("checkboxlabelSound")
        self.checkboxlabelNotify = self.containerMain.get_child("containerSearch").get_child("containerFinish").get_child("checkboxlabelNotify")
        self.linkNotifyRun = self.containerMain.get_child("containerSearch").get_child("containerFinish").get_child("linkNotifyRun")
        self.buttonStartStop = self.containerMain.get_child("containerSearch").get_child("buttonStartStop")
        self.labelStatus = self.containerMain.get_child("containerSearch").get_child("labelStatus")
        self.labelVersion = self.containerMain.get_child("containerAbout").get_child("containerInfo").get_child("labelVersion")
        
        self.labelVersion.set_text(f"FindMyVaccine (v{__version__})")
        
        self.searchOptions = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("listviewLocation")
        self.searchOptions.append({"dst":"Search by district", "pin":"Search by PIN", "exc":"Exclusions"})
        self.searchOptions.select_by_key("dst")
        
        self.linkNotifyRun.text = self.notify.endpoint
        self.linkNotifyRun.attr_href = self.notify.endpoint
                
        self.containerDist = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("containerDist")
        self.containerDist.css_visibility="visible"
        self.containerPin = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("containerPin")
        self.containerPin.css_visibility="hidden"
        self.containerExclude = self.containerMain.get_child("containerSearch").get_child("containerFilter").get_child("containerExclude")
        self.containerExclude.css_visibility="hidden"
        self.imageQR.css_visibility = "hidden"
        self.linkNotifyRun.css_visibility = "hidden"
        
        excluded_centers = pickle.load(open(PATH_EXCLUDED_CENTERS, "rb"))
        self.textinputExclusions.set_text(", ".join(excluded_centers))            
        
        #### Populate initial values from Cowin APIs
        try:
            self.states_id2name = getStateCodes()
            self.dropdownState.append(self.states_id2name)
            
            self.dist_id2name = getDistrictCodes(1)
            self.dropdownDistrict.append(self.dist_id2name)
        except Exception as e:
            self.update_status("PROBLEM: Server unreachable",color="error")

    def find_vaccine(self):
        searchOption = self.searchOptions.get_key()
        pin = self.textinputPinCodes.get_text()
        state_id = self.dropdownState.get_key()
        district_id = self.dropdownDistrict.get_key()
        exclude = self.textinputExclusions.get_text()
        
        isRemember = self.checkboxlabelRemember.get_value()
        isSaveFile = self.checkboxlabelFileSave.get_value()
        isPlaySound = self.checkboxlabelSound.get_value()
        isNotify = self.checkboxlabelNotify.get_value()
        
        vaccine = self.dropdownVaccine.get_value()
        age = self.dropdownAge.get_key()
        weeks = self.dropdownWeeks.get_key()

        excluded_centers = exclude.split(',')
        excluded_centers = [elem.rstrip().lstrip() for elem in excluded_centers]
        if excluded_centers == [""]: 
                excluded_centers = []
        
        try:
            start_date = datetime.now()
            if searchOption=="dst":
                center_list = getCentersByDist(str(district_id), start_date, weeks, randomize=False)
            elif searchOption=="pin":
                center_list = getCentersByPin(pin, start_date, weeks, randomize=False)
            elif searchOption == "exc":
                self.update_status("PROBLEM: Please search by district or PIN", color="error")

        except Exception as e:
            self.update_status(str(e), color="error")
            
        slots = filterSessions(center_list, age, vaccine, excluded_centers)
        if len(slots) > 0:
            result_str = "\n\nVACCINE AVAILABLE!"
            for i, slot in enumerate(slots):
                result_str+= f"\n\n################ SLOT #{i+1} #################\n"
                result_str+= f"{slot['name']}\n"
                result_str+= f"{slot['address']},{slot['pin']}\n"
                result_str+= f"{slot['date']}, remaining: {slot['remaining']}\n"
                result_str+= f"Vaccine: {slot['vaccine']}"
                
            timeFound = datetime.now()
            self.update_status(self.statusTxtLine1+" "+f"Found vaccine slot at ............. {timeFound.strftime('%H:%M:%S %d/%m/%Y')}", color="success")
            self.buttonStartStop.set_text("START")
            self.buttonStartStop.css_background_color = "rgb(75,215,75)"
            
            # Save results to text file 
            if isSaveFile:
                fname = f"vaccine_slot_{timeFound.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
                with open(fname,'w') as f:
                    f.write(result_str)
                    
            # Play sound
            if isPlaySound:
                playsound(os.path.join(PATH_RESOURCE_DIR,"TF026.WAV"))
                
            # Send notification to registered mobile devices
            if isNotify:
                self.notify.send(f"Vaccine found! {timeFound.strftime('%Y-%m-%d_%H-%M-%S')}")
                pass
            
            self.isScanning = False
        else:
            result_str = "\n\nSearching ..."
            self.timeScanLast = datetime.now()
            self.timeScanNext = self.timeScanLast + timedelta(seconds=randint(REFRESH_INTERVAL_MIN,REFRESH_INTERVAL_MAX))
            # Don't update status if refreshed within 5 seconds of starting the scan
            if (self.timeScanLast - self.timeScanStart).seconds > 5:
                self.update_status(self.statusTxtLine1+" "+f"Last updated at ...................... { self.timeScanLast.strftime('%H:%M:%S %d/%m/%Y')}")
            
        self.textinputResults.set_text(result_str)      

    def update_status(self, msg: str, color: tuple or str="", visible: bool=True):
        if type(color) == tuple and len(color)==3:
            colorString = f"rgb({color[0]},{color[1]},{color[2]})"
        elif color=="error":
            colorString = "rgb(215,75,75)"
        elif color == "success":
            colorString = "rgb(75,215,75)"
        else:
            colorString = "rgb(0,0,0)"
        
        self.labelStatus.set_text(msg)
        self.labelStatus.css_color = colorString
        self.labelStatus.css_visibility = "visible" if visible else "hidden"
    
    def onchange_checkboxlabelNotify(self, emitter, value):
        if self.checkboxlabelNotify.get_value() == True:
            self.linkNotifyRun.css_visibility = "visible"
            self.imageQR.css_visibility = "visible"
        else:
            self.linkNotifyRun.css_visibility = "hidden"
            self.imageQR.css_visibility = "hidden"
        pass
    
    def onclick_imageSpeaker(self,emitter):
        playsound(os.path.join(PATH_RESOURCE_DIR,"TF026.WAV"))
        pass
    
    def onclick_buttonStartStop(self, emitter):
        if self.searchOptions.get_key() == "exc":
            self.update_status("PROBLEM: Please search by district or PIN", color="error")
            return()
        
        if self.searchOptions.get_key() == "pin" and not isPinValid(self.textinputPinCodes.get_text()):
            self.update_status("PROBLEM: Invalid PIN", color="error")
            return()
        
        self.textinputResults.set_text("")
        self.labelStatus.set_text("")
        
        if self.checkboxlabelRemember.get_value() == True:
            excluded_centers = self.textinputExclusions.get_text()
            excluded_centers = excluded_centers.split(',')
            excluded_centers = [elem.rstrip().lstrip() for elem in excluded_centers]
            if excluded_centers == [""]: 
                excluded_centers = []
            pickle.dump(excluded_centers, open(PATH_EXCLUDED_CENTERS, "wb"))
            
        
        if self.isScanning:
            self.textinputResults.set_text("")     # Reset to clear the Result window
            
            self.buttonStartStop.set_text("START")
            self.buttonStartStop.css_background_color = "rgb(75,215,75)"
            
            self.update_status(self.statusTxtLine1+" "+f"Scan was stopped at ............. {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
            self.isScanning = False
        else:
            self.isScanning = True
            self.buttonStartStop.set_text("STOP")
            self.buttonStartStop.css_background_color = "rgb(215,75,75)"
            
            self.timeScanStart = datetime.now()
            
            self.statusTxtLine1 = f"Scan was started at ............... {self.timeScanStart.strftime('%H:%M:%S %d/%m/%Y')}"
            self.update_status(self.statusTxtLine1)
            
            self.find_vaccine()
        return
    
    def onselection_listviewLocation(self,emitter,selectedKey):
        if selectedKey == "dst":
            self.containerDist.css_visibility="visible"
            self.containerPin.css_visibility="hidden"
            self.containerExclude.css_visibility="hidden"
        elif selectedKey == "pin":
            self.containerDist.css_visibility="hidden"
            self.containerPin.css_visibility="visible"
            self.containerExclude.css_visibility="hidden"            
        elif selectedKey == "exc":
            self.containerDist.css_visibility="hidden"
            self.containerPin.css_visibility="hidden"
            self.containerExclude.css_visibility="visible"  

    def onchange_dropdownState(self,emitter,new_value):
        # Refresh the options available on the other (district) drop-down
        try:
            state_id = self.dropdownState.get_key()
            self.dist_id2name = getDistrictCodes(state_id)
            self.dropdownDistrict.empty() #Clear all codes
            self.dropdownDistrict.append(self.dist_id2name)
        except Exception as e:
            self.update_status("PROBLEM: Server unreachable",color="error")
    
    def onchange_dropdownVaccine(self,emitter,new_value):
        self.update_status("WARNING: Make sure you've selected the correct vaccine, especially if this is for the second dose", color="error")
        pass
    
    def onclick_m1(self,emitter):
        self.containerMain.get_child("containerSearch").css_visibility = "visible"
        self.containerMain.get_child("containerAbout").css_visibility = "hidden"
        self.m1.css_background_color = "rgb(50,150,230)"   # Make slightly lighter color to highlight selected
        self.m2.css_background_color = "rgb(19,108,209)"   # Make the same color as rest of menubar
    
    def onclick_m2(self,emitter):
        self.containerMain.get_child("containerSearch").css_visibility = "hidden"
        self.containerMain.get_child("containerAbout").css_visibility = "visible"
        self.m2.css_background_color = "rgb(50,150,230)"   # Make slightly lighter color to highlight selected
        self.m1.css_background_color = "rgb(19,108,209)"   # Make the same color as rest of menubar

    def idle(self):
        #idle function called every update cycle
        # Exception handling for the odd case when idle() gets called before self.isScanning is defined!
        try:
            if self.isScanning and (datetime.now() > self.timeScanNext):
                self.find_vaccine()
        except:
            pass

    def main(self):
        self.construct_ui(self)
        self.init_ui()
        return self.containerMain

# %% Entry point
if __name__ == "__main__":
    # Make sure .dat file exists for excluded centers
    if not os.path.exists(PATH_EXCLUDED_CENTERS):
        excluded_centers = []
        pickle.dump(excluded_centers, open(PATH_EXCLUDED_CENTERS, "wb"))
        
    start(FindMyVaccine, standalone=True, resizable=False, height=750, width=586)