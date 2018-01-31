# Import statements 
from tkinter import *   ## notice lowercase 't' in tkinter here

# import ttk
from subprocess import Popen, PIPE
import os
# import commands
import time
import tkinter.messagebox as tkMessageBox
import sys
import subprocess

#default statements
appPkg = "com.yatra.base"
noOfEvents = "500"
throttle = ""

def exitProgram(error):
    tkMessageBox.showerror("Error!",error)
    sys.exit()

def isDeviceConnected():
    process = Popen("adb devices", stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    stdout = str(stdout,'utf-8')
    if stderr:
        print ("That one ---------------- ")
        exitProgram("Error occured while trying to execute ADB Command!!")
    if not ("\t" in stdout and "device" in stdout):
        exitProgram("No devices connected. Please check the connection and try a gain.")

def captureLogcat(fileName):
    process = subprocess.Popen("adb logcat>"+fileName, shell=True, stdout=subprocess.PIPE)
    Popen("TASKKILL /F /PID {pid} /T".format(pid=process.pid))

def executeCommand():
    logAttr = " -v "
    isDeviceConnected()
    localtime = time.localtime(time.time())
    try:
        logLevel = Lb_logLevel.curselection()[0]
    except:
        logLevel = 2

    if logLevel == 1:
        logAttr+="-v "
    elif logLevel == 2:
        logAttr+= "-v -v "
    fileName = "MoneyLogs_"+entry_pkgName.get()+"_"+str(localtime.tm_mday)+"_"+str(localtime.tm_mon)+"_"+str(localtime.tm_year)+"_"+str(localtime.tm_hour)+"_"+str(localtime.tm_min)+"_"+str(localtime.tm_sec)+".txt"
    logcatFileName = "DeviceLogs_"+entry_pkgName.get()+"_"+str(localtime.tm_mday)+"_"+str(localtime.tm_mon)+"_"+str(localtime.tm_year)+"_"+str(localtime.tm_hour)+"_"+str(localtime.tm_min)+"_"+str(localtime.tm_sec)+".txt"
    fo = open(fileName,"w")
    commandToRun = "adb shell monkey -p "+entry_pkgName.get()+logAttr+entry_noOfEvents.get()
    if entry_throttle.get()!="":
        commandToRun+=" --throttle "+entry_throttle.get()
    if entry_touch.get()!="":
        commandToRun+=" --pct-touch "+entry_motion.get()
    if entry_motion.get()!="":
        commandToRun+=" --pct-motion "+entry_motion.get()
    if entry_trackball.get()!="":
        commandToRun+=" --pct-trackball " +entry_trackball.get()
    if entry_nav.get()!="":
        commandToRun+=" --pct-nav " +entry_nav.get()
    if entry_majornav.get()!="":
        commandToRun+=" --pct-majornav " +entry_majornav.get()
    if entry_syskeys.get()!="":
        commandToRun+=" --pct-syskeys " +entry_syskeys.get()
    if entry_appswitch.get()!="":
        commandToRun+=" --pct-appswitch " +entry_appswitch.get()
    if entry_anyevent.get()!="":
        commandToRun+=" --pct-anyevent " +entry_anyevent.get()

    tkMessageBox.showinfo( "Monkey Testing", "Command being sent: "+commandToRun)
    print("Command being executed: "+commandToRun)
    process = Popen(commandToRun, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    # if stderr:
        # print (stderr)
        # print ("This one ---------------- ")
        # exitProgram("Error occured while trying to execute ADB Command!!")
    stdout = str(stdout,'utf-8')
    fo.write(stdout)
    fo.close()
    captureLogcat(logcatFileName)
    tkMessageBox.showinfo( "Done", "Please check the following log files : \nMonkey Logs: "+fileName+"\nDevice logs: "+logcatFileName)

top = Tk()
top.geometry("600x650")
top.resizable(width=False, height=False)
top.title("Monkey Test Tool")


#Get the package name
label_pkgName = Label(top, text="*Package Name : ",padx="10",pady="10")
label_pkgName.grid(row=0, column=0,sticky="W")
entry_pkgName = Entry(top, bd =5)
entry_pkgName.grid(row=0, column=1,padx="10",pady="10")
entry_pkgName.insert(20, appPkg)
label_pkgNameHelp = Label(top, text="Your package name",padx="10",pady="10")
label_pkgNameHelp.grid(row=0, column=2,sticky="W")

#Get the number of events
label_noOfEvents = Label(top, text="*No. of events : ",padx="10",pady="10")
label_noOfEvents.grid(row=1, column=0,sticky="W")
entry_noOfEvents = Entry(top, bd =5)
entry_noOfEvents.grid(row=1, column=1,padx="10",pady="10")
entry_noOfEvents.insert(20, noOfEvents)
label_noOfEventsHelp = Label(top, text="No. of events you want",padx="10",pady="10")
label_noOfEventsHelp.grid(row=1, column=2,sticky="W")


#Get the log level
label_logLevel = Label(top, text="*Log level : ",padx="10",pady="10")
label_logLevel.grid(row=2, column=0,sticky="W")
Lb_logLevel = Listbox(top,height=3)
Lb_logLevel.insert(1, "0 (Min Logs)")
Lb_logLevel.insert(2, "1")
Lb_logLevel.insert(3, "2 (Max Logs)")
Lb_logLevel.grid(row=2,column=1,padx="10",pady="10")
Lb_logLevel.select_set(2)
label_logLevelHelp = Label(top, text="Log level",padx="10",pady="10")
label_logLevelHelp.grid(row=2, column=2,sticky="W")

#Get the throttle (in ms)
label_throttle = Label(top, text="Throttle(ms) : ",padx="10",pady="10")
label_throttle.grid(row=3, column=0,sticky="W")
entry_throttle = Entry(top, bd =5)
entry_throttle.grid(row=3, column=1,padx="10",pady="10")
label_throttleHelp = Label(top, text="Inserts a fixed delay between events",padx="10",pady="10")
label_throttleHelp.grid(row=3, column=2,sticky="W")

#Get the percentages

#Touch
label_touch = Label(top, text="Touch: ",padx="10",pady="10")
label_touch.grid(row=4, column=0,sticky="W")
entry_touch = Entry(top, bd =5)
entry_touch.grid(row=4, column=1,padx="10",pady="10")
label_touchHelp = Label(top, text="Adjust percentage of touch events",padx="10",pady="10")
label_touchHelp.grid(row=4, column=2,sticky="W")

#Motion
label_motion = Label(top, text="Motion: ",padx="10",pady="10")
label_motion.grid(row=5, column=0,sticky="W")
entry_motion = Entry(top, bd =5)
entry_motion.grid(row=5, column=1,padx="10",pady="10")
label_touchHelp = Label(top, text="Adjust percentage of Motion events",padx="10",pady="10")
label_touchHelp.grid(row=5, column=2,sticky="W")

#Trackball
label_trackball = Label(top, text="Trackball: ",padx="10",pady="10")
label_trackball.grid(row=6, column=0,sticky="W")
entry_trackball = Entry(top, bd =5)
entry_trackball.grid(row=6, column=1,padx="10",pady="10")
label_touchHelp = Label(top, text="Adjust percentage of Trackball events",padx="10",pady="10")
label_touchHelp.grid(row=6, column=2,sticky="W")

#Nav
label_nav = Label(top, text="Nav: ",padx="10",pady="10")
label_nav.grid(row=7, column=0,sticky="W")
entry_nav = Entry(top, bd =5)
entry_nav.grid(row=7, column=1,padx="10",pady="10")
label_touchHelp = Label(top, text="Adjust percentage of \"basic\" navigation events.",padx="10",pady="10")
label_touchHelp.grid(row=7, column=2,sticky="W")

#Major Nav
label_majornav = Label(top, text="Majornav: ",padx="10",pady="10")
label_majornav.grid(row=8, column=0,sticky="W")
entry_majornav = Entry(top, bd =5)
entry_majornav.grid(row=8, column=1,padx="10",pady="10")
label_touchHelp = Label(top, text="Adjust percentage of \"major\" navigation events.",padx="10",pady="10")
label_touchHelp.grid(row=8, column=2,sticky="W")

#Sys Keys
label_syskeys = Label(top, text="Syskeys: ",padx="10",pady="10")
label_syskeys.grid(row=9, column=0,sticky="W")
entry_syskeys = Entry(top, bd =5)
entry_syskeys.grid(row=9, column=1,padx="10",pady="10")
label_touchHelp = Label(top, text="Adjust percentage of \"system\" key events.",padx="10",pady="10")
label_touchHelp.grid(row=9, column=2,sticky="W")

#App Switch
label_appswitch = Label(top, text="Appswitch: ",padx="10",pady="10")
label_appswitch.grid(row=10, column=0,sticky="W")
entry_appswitch = Entry(top, bd =5)
entry_appswitch.grid(row=10, column=1,padx="10",pady="10")
label_touchHelp = Label(top, text="Adjust percentage of activity launches.",padx="10",pady="10")
label_touchHelp.grid(row=10, column=2,sticky="W")

#Any event
label_anyevent = Label(top, text="Anyevent: ",padx="10",pady="10")
label_anyevent.grid(row=11, column=0,sticky="W")
entry_anyevent = Entry(top, bd =5)
entry_anyevent.grid(row=11, column=1,padx="10",pady="10")
label_touchHelp = Label(top, text="Adjust percentage of other types of events.",padx="10",pady="10")
label_touchHelp.grid(row=11, column=2,sticky="W")

button_Run = Button(top, text ="Run", command = executeCommand)
button_Run.grid(row=12,column=1)

top.mainloop()