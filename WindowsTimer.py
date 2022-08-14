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

    # print(f'end time:{hours}:{minutes}:{seconds}\ncurrent time: {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}')

    if (hours.get_value() == time.localtime().tm_hour and
        minutes.get_value() == time.localtime().tm_min and
            seconds.get_value() == time.localtime().tm_sec):
        ended = True

    withdrawed_sec = time.localtime().tm_sec
    withdrawed_min = time.localtime().tm_min + seconds.extra_minus(time.localtime().tm_sec)
    withdrawed_hour = time.localtime().tm_hour + \
        minutes.extra_minus(time.localtime().tm_min)

    if minutes.get_value() == time.localtime().tm_min and seconds.extra_minus(time.localtime().tm_sec) > 0:
        withdrawed_hour = time.localtime().tm_hour + minutes.extra_minus(time.localtime().tm_min) + \
            seconds.extra_minus(time.localtime().tm_sec)

    seconds.withdraw(withdrawed_sec)
    minutes.withdraw(withdrawed_min)
    hours.withdraw(withdrawed_hour)
    # print(f'diff:{hours}:{minutes}:{seconds}\n')

    hours_to_show = ClockHand(24, hours.get_value())
    minutes_to_show = ClockHand(60, minutes.get_value())

    advanced_hour_to_show = minutes_to_show.extra_value(1)

    minutes_to_show.advance(1)
    hours_to_show.advance(advanced_hour_to_show)

    if hours_to_show.get_value() == 0:
        return (f'{minutes_to_show.get_value()}')

    return (f'{hours_to_show.get_value()}:{minutes_to_show}')
