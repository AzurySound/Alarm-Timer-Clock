from re import S
import time
from ClockHand import *

secondsLimit = 60
minutesLimit = 60
hoursLimit = 24
ended = False

def strval(val):
    if (val < 10) :
        return "0" + str(val)
    return str(val)

def showClock():
    local_h = time.localtime().tm_hour
    local_m = strval(time.localtime().tm_min)
    return(f"{local_h}:{local_m}")

#  Hooray! Commissioned as an oop approach with the ClockHand class!
def calculatedTimeEnd(h, m, s):
    hours = ClockHand(24, time.localtime().tm_hour)
    minutes = ClockHand(60, time.localtime().tm_min)
    seconds = ClockHand(60, time.localtime().tm_sec)
    
    advanced_sec = s
    advanced_min = m + seconds.extraValue(s)
    advanced_hour = h + minutes.extraValue(m)

    seconds.advance(advanced_sec)
    minutes.advance(advanced_min)
    hours.advance(advanced_hour)

    return hours.getValue(), minutes.getValue(), seconds.getValue()



# TO BE COMMISSIONED SOMETIME LATER
# TO BE COMMISSIONED SOMETIME LATER
# TO BE COMMISSIONED SOMETIME LATER
def substractLocalTimeFrom(h, m, s):
    global ended

    if ended:
        return "time"

    hours = ClockHand(24, h)
    minutes = ClockHand(60, m)
    seconds = ClockHand(60, s )

    if (hours.getValue() == time.localtime().tm_hour and
    minutes.getValue() == time.localtime().tm_min and
    seconds.getValue() == time.localtime().tm_sec + 1) :
        ended = True
    
    print(f'end time: {h}:{m}:{s}\nclock: {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}')

    # end time: 1:22:0
    # clock: 0:22:58
    # diff: 01:59:02

    # end time: 1:22:0
    # clock: 0:22:59
    # diff: 01:59:01

    # end time: 1:22:0
    # clock: 0:23:0
    # diff: 00:59:00

    # end time: 1:22:0
    # clock: 0:23:1
    # diff: 00:58:59

    # end time: 1:22:0
    # clock: 0:23:2
    # diff: 00:58:58 FROZEN
    
    withdrawed_sec = time.localtime().tm_sec # == 5
    withdrawed_min = time.localtime().tm_min + seconds.extraMinus(time.localtime().tm_sec) # == 4 + 
    withdrawed_hour = time.localtime().tm_hour + minutes.extraMinus(time.localtime().tm_min)
    # print(f'withdrawed_hour: {withdrawed_hour}\nwithdrawed_min: {withdrawed_min}\nwithdrawed_sec: {withdrawed_sec}')

    seconds.withdraw(withdrawed_sec)
    minutes.withdraw(withdrawed_min)
    hours.withdraw(withdrawed_hour)

    print(f'diff: {hours}:{minutes}:{seconds}\n')

    # returns values in format M:SS
    if hours.getValue() == 0:
        return(f'{minutes.getValue()}:{minutes}')

    # returns values in format H:MM:SS
    return(f'{hours.getValue()}:{minutes}:{seconds}')


# TO BE DECOMMISSIONED SOME TIME LATER
# TO BE DECOMMISSIONED SOME TIME LATER
# TO BE DECOMMISSIONED SOME TIME LATER
def substractLocalTimeFrom2(h, m, s):
    global ended

    # turns on when we are out of time
    if ended:
        return "time"

    # time from input
    new_h = h
    new_m = m
    new_s = s - 1
    
    # the current time
    local_h = time.localtime().tm_hour
    local_m = time.localtime().tm_min
    local_s = time.localtime().tm_sec  

    # seconds for countdown
    timer_s = new_s - local_s
    if timer_s < 0 :
        timer_s = secondsLimit + (new_s - local_s)
        new_m -= 1
    
    # minutes for countdown
    timer_m = new_m - local_m
    if timer_m < 0 :
        timer_m = minutesLimit + (new_m - local_m)
        new_h -= 1
    
    # hours for countdown
    timer_h = new_h - local_h
    if timer_h < 0 :
        timer_h = hoursLimit + (new_h - local_h)
    
    #switches boolean when out of time
    if timer_h == 0 and timer_m == 0 and timer_s == 0:

        ended = True

    # returns values in format M:SS
    if timer_h == 0:
        return(f'{timer_m}:{strval(timer_s)}')

    # returns values in format H:MM:SS
    return(f'{timer_h}:{strval(timer_m)}:{strval(timer_s)}')

# def returnCalculated(h, m, s):
#     global ended

#     #switches boolean when out of time
#     if h + m + s == 0:
#         ended = True
#         pass

#     # returns values in format M:SS
#     if h == 0:
#         return(f'{m}:{strval(s)}')

#     # returns values in format H:MM:SS
#     return(f'{h}:{strval(m)}:{strval(s)}')


