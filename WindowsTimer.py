import time
from ClockHand import *

ended = False

#  Hooray! Commissioned as an oop approach with the ClockHand class!
def add_current_time_to(h, m, s):
    hours = ClockHand(24, time.localtime().tm_hour)
    minutes = ClockHand(60, time.localtime().tm_min)
    seconds = ClockHand(60, time.localtime().tm_sec)
    
    advanced_sec = s
    advanced_min = m + seconds.extra_value(s)
    advanced_hour = h + minutes.extra_value(m)

    seconds.advance(advanced_sec)
    minutes.advance(advanced_min)
    hours.advance(advanced_hour)

    return hours.get_value(), minutes.get_value(), seconds.get_value()


def substract_local_time_from(h, m, s):
    global ended

    if ended:
        return "time"

    hours = ClockHand(24, h)
    minutes = ClockHand(60, m)
    seconds = ClockHand(60, s)
    seconds.withdraw_one() # since tkinter makes us wait for 1 sec more to update its window
    minutes.advance_one()  # since we want to round minutes to upper value (00:00:30 => 00:01:00)

    if (hours.get_value() == time.localtime().tm_hour and
    minutes.get_value() == time.localtime().tm_min + 1 and # here's + 1 since we advanced minutes by 1 two lines above
    seconds.get_value() == time.localtime().tm_sec) :
        ended = True
    
    withdrawed_sec = time.localtime().tm_sec
    withdrawed_min = time.localtime().tm_min + seconds.extra_minus(time.localtime().tm_sec)
    withdrawed_hour = time.localtime().tm_hour + minutes.extra_minus(time.localtime().tm_min)

    if minutes.get_value() == time.localtime().tm_min and seconds.extra_minus(time.localtime().tm_sec) > 0:
        withdrawed_hour = time.localtime().tm_hour + minutes.extra_minus(time.localtime().tm_min) + seconds.extra_minus(time.localtime().tm_sec)
    
    seconds.withdraw(withdrawed_sec)
    minutes.withdraw(withdrawed_min)
    hours.withdraw(withdrawed_hour)

    if hours.get_value() == 0:
        return(f'{minutes.get_value()}')

    return(f'{hours.get_value()}:{minutes}')