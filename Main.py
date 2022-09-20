import time
from tkinter import (BOTTOM, DISABLED, NORMAL, Button, Entry, IntVar, Label,
                     Menu, StringVar, Tk, Toplevel)

import WindowsTimer
import Settings
import logging


# import missd
# to do list:
# make a class for a toplevel window
# make a class for a root window

last_click_x = 0
last_click_y = 0
update_window = 1000
clock_flag = True
alarm_flag = False
timer_flag = False
stopwatch_flag = False
cap_flag = False
geo_flag = True
on_top_flag = True
font_size = 35
width_r = 40
height_r = 15
colors = ['#0FFF50', '#FFFF00', '#00FFFF', '#FF00FF']
color = colors[0]
transparencies = [0.1, 0.3, 0.5, 0.7, 1]
transparency = transparencies[1]
timer_end_time = []
start_time = []
txt_log_var = ''

# missd.sendMessage()


def save_last_click_pos(event):
    global last_click_x, last_click_y
    last_click_x = event.x
    last_click_y = event.y


def dragging(event):
    x, y = event.x - last_click_x + root.winfo_x(), event.y - \
        last_click_y + root.winfo_y()
    root.geometry("+%s+%s" % (x, y))


def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()


def find_screen_center(screen_size, win_size):
    return int(screen_size/2 - win_size/2)


root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root_width = 170
root_height = 86
root_big_width = 1400
root_big_height = 600
center_x = find_screen_center(screen_width, root_width)
center_y = find_screen_center(screen_height, root_height)
big_center_x = find_screen_center(screen_width, root_big_width)
big_center_y = find_screen_center(screen_height, root_big_height)


root.overrideredirect(True)
root.attributes('-alpha', 0.3, '-topmost', True)
root.wm_attributes('-transparentcolor', '#add123')
root.geometry(f'{root_width}x{root_height}+{center_x}+{center_y}')
root.eval('tk::PlaceWindow . center')
# root.resizable(1,1)


hour = IntVar()
min = IntVar()
sec = IntVar()
txt = StringVar()


def log_txt(new_txt):
    global txt_log_var
    if txt_log_var != new_txt:
        txt_log_var = new_txt
        logging.info('Text updated: "{}"'.format(txt_log_var))


hour.set(0)
min.set(0)
sec.set(0)
txt.set(' ')

root.bind('<Button-1>', save_last_click_pos)
root.bind('<B1-Motion>', dragging)
root.bind('<Double-Button-1>', lambda e: change_color())
root.bind('<Button-2>', lambda e: switch_transparency())


def switch_transparency():
    global transparency
    transNum = transparencies.index(transparency)
    transNum += 1
    if transNum == len(transparencies):
        transNum = 0
    transparency = transparencies[transNum]
    root.attributes('-alpha', transparency)


def change_color():
    global color
    colorNum = colors.index(color)
    colorNum += 1
    if colorNum == len(colors):
        colorNum = 0
    color = colors[colorNum]
    reset_view()


def open_timer_label():
    global Timer, font_size
    switch_timer()
    WindowsTimer.finished = False
    Timer = Label(root, font=("Digital-7", font_size), fg=color,
                  bg='#add123', width=width_r, height=height_r)
    Timer.bind("<Button-3>", do_popup)

# def open_stopwatch_label():
#     global Stopwatch, font_size
#     switch_stopwatch()
#     WindowsTimer.finished = False
#     Stopwatch = Label(root, font=("Digital-7", font_size), fg=color,
#                   bg='#add123', width=width_r, height=height_r)
#     Stopwatch.bind("<Button-3>", do_popup)


def open_alarm_label():
    switch_alarm()
    global Alarm, font_size
    WindowsTimer.finished = False
    Alarm = Label(root, font=("Digital-7", font_size), fg=color,
                  bg='#add123', width=width_r, height=height_r)
    Alarm.bind("<Button-3>", do_popup)


def open_clock_label():
    switch_clock()
    global Clock, font_size
    Clock = Label(root, font=("Digital-7", font_size), fg=color,
                  bg='#add123', width=width_r, height=height_r)
    Clock.bind("<Button-3>", do_popup)


def open_cap_label():
    switch_cap()
    global Cap, font_size
    Cap = Label(root, font=("Digital-7", font_size), fg='#000',
                bg='#FFF', width=width_r, height=height_r)
    Cap.bind("<Button-3>", do_popup)


Text = Label(root, font=("Digital-7", int(font_size * 0.5)),
             text=txt.get().lstrip().rstrip(), fg=color, bg='#add123', width=width_r)
Text.bind("<Button-3>", do_popup)


m = Menu(root, tearoff=0)
m.add_command(label="Settings", command=lambda: open_new_window())
# m.add_command(label="Stopwatch", command=lambda: turn_on_stopwatch_if_can())
m.add_command(label="Clock", command=lambda: turn_clock_on_if_can())
m.add_command(label="Bigger", command=lambda: change_geoposition())
m.add_command(label="Off top", command=lambda: switch_on_top())
m.add_command(label="Close", command=lambda: destroy())


def destroy():
    logging.info('Closing the instance with text: "{}"'.format(txt_log_var))
    root.destroy()

# this func is not rdy and should be properly tested. use open_new_window() instead


def open_settings():
    Settings(root)


def turn_clock_on_if_can():
    if not clock_flag:
        switch_alarm(), open_clock()

# def turn_on_stopwatch_if_can():
#     get_start_time()
#     if not stopwatch_flag:
#         open_stopwatch()


def switch_on_top():
    global on_top_flag
    if not on_top_flag:
        root.attributes('-topmost', True)
        m.entryconfigure(3, label="Off top")
        on_top_flag = True
    else:
        root.attributes('-topmost', False)
        m.entryconfigure(3, label="On top")
        on_top_flag = False


def change_geoposition():
    if geo_flag:
        bigger()
    else:
        smaller()


def reset_view():

    Text.config(fg=color)

    if clock_flag:
        Clock.destroy()
        open_clock_label()
        Clock.pack()
        run_clock()

    elif alarm_flag:
        Alarm.destroy()
        open_alarm_label()
        Alarm.pack()
        run_alarm()

    elif cap_flag:
        Cap.destroy()
        open_cap_label()
        Cap.pack()
        run_cap()

    # elif stopwatch_flag:
    #     Stopwatch.destroy()
    #     open_cap_label()
    #     Cap.pack()
    #     run_cap()

    else:
        Timer.destroy()
        open_timer_label()
        Timer.pack()
        run_timer()


def smaller():
    global geo_flag, font_size, width_r, height_r
    m.entryconfigure(2, label="Bigger")
    if not on_top_flag:
        switch_on_top()
    font_size = 35
    width_r = 40
    height_r = 15
    Text.config(font=("Digital-7", int(font_size * 0.5)), width=width_r)
    reset_view()
    root.geometry(f'{root_width}x{root_height}+{center_x}+{center_y}')
    geo_flag = True


def bigger():
    global geo_flag, font_size, width_r, height_r
    m.entryconfigure(2, label="Smaller")
    if on_top_flag:
        switch_on_top()
    font_size = 290
    width_r = 170
    height_r = 33
    Text.config(font=("Digital-7", int(font_size * 0.5)), width=width_r)
    reset_view()
    root.geometry(
        f'{root_big_width}x{root_big_height}+{big_center_x}+{big_center_y}')
    geo_flag = False


def open_error():
    try:
        Timer.destroy()
        Alarm.destroy()
        # Stopwatch.destroy()
        Clock.destroy()
        open_cap_label()
        Cap.pack()
        run_error()
    except Exception as e:
        logging.error(e)
        pass


def open_cap():
    try:
        Timer.destroy()
        Alarm.destroy()
        # Stopwatch.destroy()
        open_cap_label()
        Cap.pack()
        run_cap()
    except Exception as e:
        logging.error(e)
        open_error()


def open_clock():
    try:
        Timer.destroy()
        Alarm.destroy()
        Cap.destroy()
        # Stopwatch.destroy()
        open_clock_label()
        Clock.pack()
        run_clock()
    except Exception as e:
        logging.error(e)
        open_error()


def open_alarm():
    try:
        open_alarm_label()
        Timer.destroy()
        Clock.destroy()
        Cap.destroy()
        # Stopwatch.destroy()
        Alarm.pack()
        run_alarm()
    except Exception as e:
        logging.error(e)
        open_error()


def open_timer():
    try:
        get_timer_end_time()
        open_timer_label()
        Clock.destroy()
        Cap.destroy()
        # Stopwatch.destroy()
        Alarm.destroy()
        Timer.pack()
        run_timer()
    except Exception as e:
        logging.error(e)
        open_error()

# def open_stopwatch():
#     try:
#         open_stopwatch_label()
#         Clock.destroy()
#         Cap.destroy()
#         Alarm.destroy()
#         Timer.destroy()
#         Stopwatch.pack()
#         run_stopwatch()
#     except Exception as e:
#         logging.error(e)
#         open_error()


def switch_clock():
    global clock_flag, alarm_flag, timer_flag, cap_flag, stopwatch_flag
    clock_flag, alarm_flag, timer_flag, cap_flag, stopwatch_flag = True, False, False, False, False


def switch_alarm():
    global clock_flag, alarm_flag, timer_flag, cap_flag, stopwatch_flag
    clock_flag, alarm_flag, timer_flag, cap_flag, stopwatch_flag = False, True, False, False, False


def switch_timer():
    global clock_flag, alarm_flag, timer_flag, cap_flag, stopwatch_flag
    clock_flag, alarm_flag, timer_flag, cap_flag, stopwatch_flag = False, False, True, False, False

# def switch_stopwatch():
#     global clock_flag, alarm_flag, timer_flag, cap_flag, stopwatch_flag
#     clock_flag, alarm_flag, timer_flag, cap_flag, stopwatch_flag = False, False, False, False, True


def switch_cap():
    global clock_flag, alarm_flag, timer_flag, cap_flag, stopwatch_flag
    clock_flag, alarm_flag, timer_flag, cap_flag, stopwatch_flag = False, False, False, True, False


def open_new_window():

    def btn_set():

        if clock_flag:
            clockBtn['state'] = DISABLED
            alarmBtn['state'] = NORMAL
            timerBtn['state'] = NORMAL
            logging.info('Pushed btn clockBtn')

        if alarm_flag:
            alarmBtn['state'] = DISABLED
            clockBtn['state'] = NORMAL
            timerBtn['state'] = NORMAL
            logging.info('Pushed btn alarmBtn')

        if timer_flag:
            timerBtn['state'] = DISABLED
            alarmBtn['state'] = NORMAL
            clockBtn['state'] = NORMAL
            logging.info('Pushed btn timerBtn')

    window_width = 240
    window_height = 145

    # find the center point
    center_x = find_screen_center(screen_width, root_width)
    center_y = find_screen_center(screen_height, root_height)

    newwin = Toplevel(root)
    newwin.title("Settings")
    newwin.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    newwin.resizable(False, False)
    Label(newwin, text="\nAlarm sets countdown until time.\nTimer sets for time. ").pack()

    Entry(newwin, textvariable=hour, width=4).place(x=45, y=55)
    Entry(newwin, textvariable=min, width=4).place(x=105, y=55)
    Entry(newwin, textvariable=sec, width=4).place(x=165, y=55)
    Entry(newwin, textvariable=txt, width=24).place(x=45, y=83)

    clockBtn = Button(newwin, text="Clock", width=7, command=lambda: [
                      switch_clock(), btn_set(), open_clock()])
    alarmBtn = Button(newwin, text="Alarm", width=7, command=lambda: [
                      switch_alarm(), btn_set(), open_alarm()])
    timerBtn = Button(newwin, text="Timer", width=7, command=lambda: [
                      switch_timer(), btn_set(), open_timer()])
    btn_set()

    clockBtn.place(x=20, y=110)
    alarmBtn.place(x=90, y=110)
    timerBtn.place(x=160, y=110)


def get_start_time():
    global start_time
    start_time = [time.localtime().tm_hour, time.localtime().tm_min,
                  time.localtime().tm_sec]


def get_timer_end_time():
    global timer_end_time
    timer_end_time_list = get_user_Input()
    timer_end_time = WindowsTimer.add_current_time_to(
        timer_end_time_list[0], timer_end_time_list[1], timer_end_time_list[2])


def add_text():
    text_input = txt.get().lstrip().rstrip()
    log_txt(text_input)
    Text.config(text=text_input)
    Text.pack(side=BOTTOM)
    Text.after(1000, add_text)


def get_user_Input():
    try:
        h = hour.get()
    except Exception as e:
        logging.debug(e)
        h = 0
    try:
        m = min.get()
    except Exception as e:
        logging.debug(e)
        m = 0
    try:
        s = sec.get()
    except Exception as e:
        logging.debug(e)
        s = 0
    logging.debug('Entry: {}:{}:{}'.format(h, m, s))
    return h, m, s


def run_error():
    Cap.config(text="ERROR")
    if time.localtime().tm_sec % 2 == 0:
        Cap.config(fg='#F00', bg='#add123')
    else:
        Cap.config(fg='#FFF', bg='#add123')
    Cap.after(1000, run_error)


def run_cap():
    Cap.config(text="time")
    if time.localtime().tm_sec % 2 == 0:
        Cap.config(fg='#FFF', bg='#000')
    else:
        Cap.config(fg='#000', bg='#FFF')
    Cap.after(1000, run_cap)


def run_alarm():
    try:
        hms = get_user_Input()
        text_input = WindowsTimer.get_countdown(
            hms[0], hms[1], hms[2])
        Alarm.config(text=text_input)
        Alarm.after(update_window, run_alarm)
        if text_input == 'finished':
            open_cap()
    except Exception as e:
        logging.error(e)
        open_error()


def run_timer():
    try:
        user_input = get_user_Input()

        if user_input == (0, 0, 0):
            text_input = WindowsTimer.stopwatch(
                timer_end_time[0], timer_end_time[1], timer_end_time[2])
        else:
            text_input = WindowsTimer.get_countdown(
                timer_end_time[0], timer_end_time[1], timer_end_time[2])

        Timer.config(text=text_input)
        Timer.after(update_window, run_timer)
        if text_input == 'finished':  # or sum(hms) == 0:
            open_cap()
    except Exception as e:
        logging.error(e)
        open_error()

# def run_stopwatch():
#     try:
#         text_input = WindowsTimer.stopwatch(start_time[0], start_time[1], start_time[2])
#         if isinstance(text_input, str):
#             print('YES ' + text_input)
#         Timer.config(text=text_input)
#         Timer.after(update_window, run_timer)
#     except Exception as e:
#         logging.error(e)
#         open_error()


def run_clock():
    try:
        text_input = time.strftime("%H:%M", time.localtime())
        Clock.config(text=text_input)
        Clock.after(update_window, run_clock)
    except Exception as e:
        logging.error(e)
        open_error()


open_timer_label()
# open_stopwatch_label()
open_alarm_label()
open_cap_label()
open_clock()
add_text()
root.mainloop()


# python documents\timer\main.py
# pyinstaller --onefile -w main.py
# Alarm-Timer-Clock
# https://www.pythontutorial.net/tkinter/tkinter-after/


# http://t.me/missDiligenceBot
# Use this token to access the HTTP API:
# 5472804874:AAEGGYjTenN7Tbkrr1rroPO_bibtdIY5YKk
# Keep your token secure and store it safely, it can be used by anyone to control your bot.
