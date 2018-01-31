# Import statements 
from tkinter import *
from subprocess import Popen, PIPE
import os
import re
import time
import tkinter.messagebox as tkMessageBox
import sys
import subprocess
import webbrowser

#Methods
def exitProgram(error):
    tkMessageBox.showerror("Error!",error)
    sys.exit()

def runAdbCommand(command):
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    stdout = str(stdout,'utf-8')
    if stderr:
        exitProgram("Error occured while trying to execute ADB Command!!")
    return stdout

def isDeviceConnected():
    stdout = runAdbCommand("adb devices");
    if not ("\t" in stdout and "device" in stdout):
        exitProgram("No devices connected. Please check the connection and try a gain.")

def disconnect():
    stdout = runAdbCommand("adb usb")
    time.sleep(2)
    button_wireless_start['state'] = "active";
    button_wireless_stop['state'] = "disabled";

# Method to execute commands to view logs Wirelessly
def adbOverWifi():
    isDeviceConnected()
    getIp = "adb shell ip route"
    print("Command being executed: "+getIp)
    stdout = runAdbCommand(getIp)
    print("Output: "+stdout)
    ipAdd = re.findall("src(.+)$",stdout)
    ip = str(ipAdd).split(" ")[1]
    print("IP of mobile: "+ip)
    # tkMessageBox.showinfo( "IP Address",ip)
    stdout = runAdbCommand("adb usb")
    time.sleep(2)
    stdout = runAdbCommand("adb tcpip 5556")
    time.sleep(2)
    stdout = runAdbCommand("adb connect "+ip+":5556")
    time.sleep(2)
    tkMessageBox.showinfo("Quiver", "Remove your device from USB now.")
    button_wireless_start['state'] = "disabled";
    button_wireless_stop['state'] = "active";

# Method to launch Monkey Tool
def monkeyTool():
    p = subprocess.Popen("python monkeyTool.py", shell=True, stdout=subprocess.PIPE)

def startLogs():
    global processIdLogs, adbLogsFileName
    localtime = time.localtime(time.time())
    button_logs_stop['state'] = 'active';
    button_logs_start['state'] = 'disabled';
    adbLogsFileName = "adbLogs_"+str(localtime.tm_mday)+"_"+str(localtime.tm_mon)+"_"+str(localtime.tm_year)+"_"+str(localtime.tm_hour)+"_"+str(localtime.tm_min)+"_"+str(localtime.tm_sec)+".txt"
    p1 = subprocess.Popen("adb logcat|findstr \"ytlog\">"+cd+"\\AdbLogs\\"+adbLogsFileName, shell=True, stdout=subprocess.PIPE)
    processIdLogs = p1.pid

def stopLogs():
    button_logs_stop['state'] = 'disabled';
    button_logs_start['state'] = 'active';
    Popen("TASKKILL /F /PID {pid} /T".format(pid=processIdLogs))
    tkMessageBox.showinfo( "Quiver", "Logs Saved: "+adbLogsFileName)

def startRecord():
    global processIdVid, videoFileName
    localtime = time.localtime(time.time())
    button_vid_stop['state'] = 'active';
    button_vid_start['state'] = 'disabled';
    videoFileName = "video_"+str(localtime.tm_mday)+"_"+str(localtime.tm_mon)+"_"+str(localtime.tm_year)+"_"+str(localtime.tm_hour)+"_"+str(localtime.tm_min)+"_"+str(localtime.tm_sec)+".mp4"
    p2 = subprocess.Popen("adb shell screenrecord /sdcard/"+videoFileName, stdout=subprocess.PIPE)
    processIdVid = p2.pid
    # print("1. Process Id for Video Recording: "+str(processIdVid))
    # print("Name of file: "+videoFileName)

def stopRecord():
    global videoFileName, processIdVid
    # print("2. Process Id for Video Recording: "+str(processIdVid))
    button_vid_stop['state'] = 'disabled'
    button_vid_start['state'] = 'active'
    Popen("TASKKILL /F /PID {pid} /T".format(pid=processIdVid))
    time.sleep(2)
    p3 = runAdbCommand("adb pull /sdcard/"+videoFileName+" "+cd+"\\Videos\\"+videoFileName)
    print(p3)
    tkMessageBox.showinfo( "Quiver", "Video Saved: "+videoFileName)

def takeScreenshot():
    localtime = time.localtime(time.time())
    imgName = "Img_"+str(localtime.tm_mday)+"_"+str(localtime.tm_mon)+"_"+str(localtime.tm_year)+"_"+str(localtime.tm_hour)+"_"+str(localtime.tm_min)+"_"+str(localtime.tm_sec)+".png"
    button_takePic['state'] = 'disabled';
    p4 = runAdbCommand("adb shell screencap -p /sdcard/"+imgName)
    p5 = runAdbCommand("adb pull /sdcard/"+imgName+" "+cd+"\\Screenshots\\"+imgName)
    print (p5)
    tkMessageBox.showinfo( "Quiver", "Screenshot Saved: "+imgName)
    button_takePic['state'] = 'active'

def openBugzilla():
    osName = "iOS"
    if chk_android.get()==1:
        osName = "Android"
    sprintName = entry_sprintName.get()
    url = ("http://bug.yatra.com/report.cgi?bug_severity=blocker&bug_severity=critical&bug_severity=major"
        "&bug_severity=normal&bug_severity=minor&bug_severity=trivial&bug_severity=enhancement&bug_status=APPROVED&"
        "bug_status=DEFERRED&bug_status=Enhancement&bug_status=New&bug_status=UNCONFIRMED&bug_status=CONFIRMED&"
        "bug_status=ASSIGNED&bug_status=RESOLVED&bug_status=REOPENED&bug_status=VERIFIED&"
        "bug_status=COMPLETED&op_sys="+osName+"&product=B2C%20Mobile%20App&version="+sprintName+"&x_axis_field=bug_severity"
        "&y_axis_field=bug_status&format=table&action=wrap")
    webbrowser.open(url, new=0, autoraise=True)


def clearData():
    p6 = runAdbCommand("adb shell pm clear com.yatra.base")
    tkMessageBox.showinfo( "Quiver", "Done!")


cd = runAdbCommand("cd")
# print("cd: "+cd)
cd = cd.rstrip()
ls = os.listdir()
if not("AdbLogs" in ls):
    createLogsFolder = runAdbCommand("mkdir AdbLogs")
if not ("Videos" in ls):
    createVideosFolder = runAdbCommand("mkdir Videos")
if not ("Screenshots" in ls):
    createScreenshotsFolder = runAdbCommand("mkdir Screenshots")
if not ("MonkeyToolLogs" in ls):
    createMonkeyToolFolder = runAdbCommand("mkdir MonkeyToolLogs")

top = Tk()
top.geometry("300x700") #wXh
top.resizable(width=False, height=False)
top.title("Quiver")

top.grid_rowconfigure(0, minsize=10)
top.grid_columnconfigure(0, minsize=10)

label_wifi_adb = Label(top, text="Connect your Android device to PC with WiFi : ",padx="10",pady="10")
label_wifi_adb.grid(row=1, column=1, sticky="NW", columnspan=6)

button_wireless_start = Button(top, text ="Connect", command = adbOverWifi, padx=5, pady=5, bd=5)
button_wireless_start.grid(row=2,column=1, columnspan=2,sticky="NEWS", padx=5, pady=5)

button_wireless_stop = Button(top, text ="Disconnect", command = disconnect, padx=5, pady=5, bd=5)
button_wireless_stop.grid(row=2,column=4, columnspan=2,sticky="NEWS", padx=5, pady=5)
button_wireless_stop['state'] = "disabled";

top.grid_rowconfigure(3, minsize=10)

label_logs = Label(top, text="Save logs for yatra app in a text file: ",padx="10",pady="10")
label_logs.grid(row=4, column=1,sticky="NW", columnspan=6)

button_logs_start = Button(top, text ="Start", command = startLogs, padx=5, pady=5, bd=5)
button_logs_start.grid(row=5,column=1, columnspan=2,sticky="NEWS")

button_logs_stop = Button(top, text ="Stop", command = stopLogs, padx=5, pady=5, bd=5)
button_logs_stop.grid(row=5,column=4, columnspan=2,sticky="NEWS")
button_logs_stop['state'] = "disabled";

top.grid_rowconfigure(6, minsize=10)

label_record = Label(top, text="Record the screen of your Android device: ",padx="10",pady="10")
label_record.grid(row=7, column=1,sticky="NW", columnspan=6)

button_vid_start = Button(top, text ="Record", command = startRecord, padx=5, pady=5, bd=5)
button_vid_start.grid(row=8,column=1, columnspan=2,sticky="NEWS")

button_vid_stop = Button(top, text ="Stop", command = stopRecord, padx=5, pady=5, bd=5)
button_vid_stop.grid(row=8,column=4, columnspan=2,sticky="NEWS")
button_vid_stop['state'] = "disabled";

top.grid_rowconfigure(9, minsize=10)

label_monkey = Label(top, text="Launch the Monkey Testing Tool: ",padx="10",pady="10")
label_monkey.grid(row=10, column=1,sticky="NW", columnspan=6)

button_monkey = Button(top, text ="Monkey Tool", command = monkeyTool, padx=5, pady=5, bd=5)
button_monkey.grid(row=11,column=2, columnspan=4, sticky="NEWS")

top.grid_rowconfigure(12, minsize=10)

label_pic = Label(top, text="Take the screenshot: ",padx="10",pady="10")
label_pic.grid(row=13, column=1,sticky="NW", columnspan=6)

button_takePic = Button(top, text ="Screenshot", command = takeScreenshot, padx=5, pady=5, bd=5)
button_takePic.grid(row=14,column=2, columnspan=4, sticky="NEWS") 

top.grid_rowconfigure(15, minsize=10)

label_bug = Label(top, text="Bugzilla total Bugs: ",padx="10",pady="10")
label_bug.grid(row=16, column=1,sticky="NW", columnspan=6)

chk_android = IntVar()
chk_ios = IntVar()

chkBtn_android = Checkbutton(top, text="Android", variable=chk_android)
chkBtn_android.grid(row=17, column=1,columnspan=3, sticky="NEWS")

chkBtn_iOS = Checkbutton(top, text="iOS", variable=chk_ios)
chkBtn_iOS.grid(row=17, column=4, columnspan=2,sticky="NEWS")

label_sprint = Label(top, text="Sprint Name: ",padx="10",pady="10")
label_sprint.grid(row=18, column=1,sticky="NW", columnspan=2)

entry_sprintName = Entry(top)
entry_sprintName.grid(row=18, column=3, columnspan=2, padx="10",pady="10",)

button_bugs = Button(top, text ="Go", command = openBugzilla, padx=2, pady=2)
button_bugs.grid(row=18, column=5, sticky="NEWS")

# --------------------------------- 

top.grid_rowconfigure(19, minsize=10)

label_data = Label(top, text="Clear App Data: ",padx="10",pady="10")
label_data.grid(row=20, column=1,sticky="NW", columnspan=6)

button_data = Button(top, text ="Clear App Data", command = clearData, padx=5, pady=5, bd=5)
button_data.grid(row=21,column=2, columnspan=4, sticky="NEWS")



# # ---------------------------------------------------------------------------

label_version = Label(top, text="Version: 2.1\n(Developed by: Mobile QA Team)", padx="10", pady="10")
label_version.grid(row=22, column=1,sticky="NEWS", columnspan=6)

top.mainloop()