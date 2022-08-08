#from ast import openErr()
from tkinter import *
import WindowsTimer
import time
# import missd

# Known issues:
# SOLVED 1) runTimer() method calculates difference between desired time and the current time every second
# SOLVED 2) desired time is being set up only by pushing the timer button
# whereas desired time should change right after changing values in user input fields
# which leads to corrupted time difference when user inputs lesser time without pushing an appropriate button

# 3) WindowsTimer.py should be rewritten with oop approach

lastClickX = 0
lastClickY = 0
updateWindow = 1000
clockFlag = True
alarmFlag = False
timerFlag = False
capFlag = False
geoFlag = True
onTopFlag = True
fontSize = 35
width_r = 40
height_r = 15
colors = ['#0FFF50','#FFFF00','#00FFFF','#FF00FF']
color = colors[0]
transparencies = [0.1, 0.3, 0.5, 0.7, 1]
transparency = transparencies[1]
timerEndTime = []
 # get the screen dimension

# missd.sendMessage()

def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

def Dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x , y))

def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()

def findScreenCenter(screen_size, win_size):
    return int(screen_size/2 - win_size/2)

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root_width = 170
root_height = 86
root_big_width = 1400
root_big_height = 600
center_x = findScreenCenter(screen_width, root_width)
center_y = findScreenCenter(screen_height, root_height)
big_center_x = findScreenCenter(screen_width, root_big_width)
big_center_y = findScreenCenter(screen_height, root_big_height)

root.overrideredirect(True)
root.attributes('-alpha', 0.3, '-topmost', True)
root.wm_attributes('-transparentcolor', '#add123')
root.geometry(f'{root_width}x{root_height}+{center_x}+{center_y}')
root.eval('tk::PlaceWindow . center')
#root.resizable(1,1)

hour = IntVar()
min = IntVar()
sec = IntVar()
txt = StringVar()

hour.set(0)
min.set(0)
sec.set(0)
txt.set(' ')

root.bind('<Button-1>', SaveLastClickPos)
root.bind('<B1-Motion>', Dragging)
root.bind('<Double-Button-1>', lambda e: changeColor())
root.bind('<Button-2>', lambda e: switchTransp())

def switchTransp():
    global transparency
    transNum = transparencies.index(transparency)
    transNum += 1
    if transNum == len(transparencies):
        transNum = 0
    transparency = transparencies[transNum]
    root.attributes('-alpha', transparency)
    
def changeColor():
    global color
    colorNum = colors.index(color)
    colorNum += 1
    if colorNum == len(colors):
        colorNum = 0
    color = colors[colorNum]
    resetView()

def oTimer():
    global Timer, fontSize
    timerSwitch()
    WindowsTimer.ended = False
    Timer = Label(root, font=("Digital-7", fontSize), fg=color, bg='#add123', width=width_r, height=height_r)
    Timer.bind("<Button-3>", do_popup)

def oAlarm():
    alarmSwitch()
    global Alarm, fontSize
    WindowsTimer.ended = False
    Alarm = Label(root, font=("Digital-7", fontSize), fg=color, bg='#add123', width=width_r, height=height_r)
    Alarm.bind("<Button-3>", do_popup)

def oClock():
    clockSwitch()
    global Clock, fontSize
    Clock = Label(root, font=("Digital-7", fontSize), fg=color, bg='#add123', width=width_r, height=height_r)
    Clock.bind("<Button-3>", do_popup)

def oCap():
    capSwitch()
    global Cap, fontSize
    Cap = Label(root, font=("Digital-7", fontSize), fg='#000', bg='#FFF', width=width_r, height=height_r)
    Cap.bind("<Button-3>", do_popup)

Text = Label(root, font=("Digital-7", int(fontSize * 0.5)), text=txt.get(), fg=color, bg='#add123', width=width_r)
Text.bind("<Button-3>", do_popup)


m = Menu(root, tearoff=0)
m.add_command(label="Settings", command = lambda: openNewwin())
m.add_command(label="Clock", command = lambda: turnClockIfCan())
m.add_command(label="Bigger", command = lambda: changeGeo())
m.add_command(label="Off top", command = lambda: switchOnTop())
m.add_command(label="Close", command = root.destroy)

def turnClockIfCan():
    if not clockFlag:
        clockSwitch(), openClock()

def switchOnTop():
    global onTopFlag
    if not onTopFlag:
        root.attributes('-topmost', True)
        m.entryconfigure(3, label="Off top")
        onTopFlag = True
    else:
        root.attributes('-topmost', False)
        m.entryconfigure(3, label="On top")
        onTopFlag = False

def changeGeo():
    if geoFlag:
        bigger()
    else:
        smaller()

def resetView():

    Text.config(fg=color)

    if clockFlag:
        Clock.destroy()
        oClock()
        Clock.pack()
        runClock()

    elif alarmFlag:
        Alarm.destroy() 
        oAlarm()
        Alarm.pack()
        runAlarm()

    elif capFlag:
        Cap.destroy() 
        oCap()
        Cap.pack()
        runCap()

    else:
        Timer.destroy() 
        oTimer()
        Timer.pack()
        runTimer()

def smaller():
    global geoFlag, fontSize, width_r, height_r
    m.entryconfigure(2, label="Bigger")
    if not onTopFlag:
        switchOnTop()
    fontSize = 35
    width_r = 40
    height_r = 15
    Text.config(font=("Digital-7", int(fontSize * 0.5)), width=width_r)
    resetView()
    root.geometry(f'{root_width}x{root_height}+{center_x}+{center_y}')
    geoFlag = True

def bigger():
    global geoFlag, fontSize, width_r, height_r
    m.entryconfigure(2, label="Smaller")
    if onTopFlag:
        switchOnTop()
    fontSize = 290
    width_r = 170
    height_r = 33
    Text.config(font=("Digital-7", int(fontSize * 0.5)), width=width_r)
    resetView()
    root.geometry(f'{root_big_width}x{root_big_height}+{big_center_x}+{big_center_y}')
    geoFlag = False

def openErr():
    try:
        Timer.destroy()
        Alarm.destroy()
        Clock.destroy()
        oCap()
        Cap.pack()
        runErr()
    except: pass

def openCap():
    try:
        Timer.destroy()
        Alarm.destroy()
        oCap()
        Cap.pack()
        runCap()
    except: openErr()

def openClock():
    try:
        Timer.destroy()
        Alarm.destroy() 
        Cap.destroy()
        oClock()
        Clock.pack()
        runClock()
    except: openErr()

def openAlarm():
    try:
        oAlarm()
        Timer.destroy()
        #WindowsTimer.receiveStartTime(time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        Clock.destroy()
        Cap.destroy()
        Alarm.pack()
        runAlarm()
    except: openErr()

def openTimer():
    try:
        getTimerEndTime()
        oTimer()
        Clock.destroy()
        Cap.destroy()
        Alarm.destroy()
        Timer.pack()
        runTimer()
    except: openErr()
    
def clockSwitch():
    global clockFlag, alarmFlag, timerFlag, capFlag
    clockFlag, alarmFlag, timerFlag, capFlag = True, False, False, False

def alarmSwitch():    
    global clockFlag, alarmFlag, timerFlag, capFlag
    clockFlag, alarmFlag, timerFlag, capFlag = False, True, False, False

def timerSwitch():        
    global clockFlag, alarmFlag, timerFlag, capFlag
    clockFlag, alarmFlag, timerFlag, capFlag = False, False, True, False

def capSwitch():        
    global clockFlag, alarmFlag, timerFlag, capFlag
    clockFlag, alarmFlag, timerFlag, capFlag = False, False, False, True
      

def openNewwin():
    
    def btnSet():
        if clockFlag:
            clockBtn['state'] = DISABLED
            alarmBtn['state'] = NORMAL
            timerBtn['state'] = NORMAL

        if alarmFlag:
            alarmBtn['state'] = DISABLED
            clockBtn['state'] = NORMAL
            timerBtn['state'] = NORMAL

        if timerFlag:
            timerBtn['state'] = DISABLED
            alarmBtn['state'] = NORMAL
            clockBtn['state'] = NORMAL

        
    window_width = 240
    window_height = 145

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2) 

    newwin = Toplevel(root)
    newwin.title("Settings")
    newwin.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    newwin.resizable(False, False)
    Label(newwin, text ="\nAlarm sets countdown until time.\nTimer sets for time. ").pack()

    Entry(newwin,textvariable = hour, width = 4).place(x=45,y=55)
    Entry(newwin,textvariable = min, width = 4).place(x=105,y=55) 
    Entry(newwin,textvariable = sec, width = 4).place(x=165,y=55)
    Entry(newwin,textvariable = txt, width = 24).place(x=45,y=83)


    clockBtn = Button(newwin, text = "Clock", width = 7, command = lambda: [clockSwitch(), btnSet(), openClock()])
    alarmBtn = Button(newwin, text = "Alarm", width = 7, command = lambda: [alarmSwitch(), btnSet(), openAlarm()])
    timerBtn = Button(newwin, text = "Timer", width = 7, command = lambda: [timerSwitch(), btnSet(), openTimer()])
    btnSet()

    clockBtn.place(x=20,y=110)
    alarmBtn.place(x=90,y=110)
    timerBtn.place(x=160,y=110)

def getTimerEndTime():
    global timerEndTime
    timerEndTimeList = getUserInput()
    timerEndTime = WindowsTimer.calculatedTimeEnd(timerEndTimeList[0], timerEndTimeList[1], timerEndTimeList[2])

def addText():
    text_input = txt.get()
    Text.config(text = text_input)
    Text.pack(side=BOTTOM)
    Text.after(1000, addText)

def getUserInput():
    try: h = hour.get()
    except: h = 0
    try: m = min.get()
    except: m = 0
    try: s = sec.get()
    except: s = 0
    return h, m, s

def runErr():
    Cap.config(text = "ERROR")
    if time.localtime().tm_sec % 2 == 0:
        Cap.config(fg='#F00', bg='#add123')
    else: Cap.config(fg='#FFF', bg='#add123')
    Cap.after(1000, runErr)

def runCap():
    Cap.config(text = "time")
    if time.localtime().tm_sec % 2 == 0:
        Cap.config(fg='#FFF', bg='#000')
    else: Cap.config(fg='#000', bg='#FFF')
    Cap.after(1000, runCap)

def runAlarm():
    try:
        hms = getUserInput()
        text_input = WindowsTimer.substractLocalTimeFrom(hms[0],hms[1],hms[2])
        # Alarm.config(text = text_input[0:-3])
        Alarm.config(text = text_input)
        Alarm.after(updateWindow, runAlarm)
        if text_input == 'time':
            openCap()
    except:  openErr()

def runTimer():
    try:
        hms = getUserInput()
        text_input = WindowsTimer.substractLocalTimeFrom(timerEndTime[0],timerEndTime[1],timerEndTime[2])
        # Timer.config(text = text_input[0:-3])
        Timer.config(text = text_input)
        Timer.after(updateWindow, runTimer)
        if text_input == 'time' or hms[0] == 0 and hms[1] == 0 and hms[2] == 0:
            openCap()
    except:  openErr()

def runClock():
    try:
        text_input = WindowsTimer.showClock()
        Clock.config(text = text_input)
        Clock.after(updateWindow, runClock)
    except: openErr()

oTimer()
oAlarm()
oCap()
openClock()
addText()
root.mainloop()


# python documents\timer\main.py
# pyinstaller --onefile -w main.py
# https://www.pythontutorial.net/tkinter/tkinter-after/


# http://t.me/missDiligenceBot
# Use this token to access the HTTP API:
# 5472804874:AAEGGYjTenN7Tbkrr1rroPO_bibtdIY5YKk
# Keep your token secure and store it safely, it can be used by anyone to control your bot.




