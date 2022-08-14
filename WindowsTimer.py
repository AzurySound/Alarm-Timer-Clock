from itertools import count
import time
from ClockHand import *

finished = False


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

    if minutes.get_value() > 0 and seconds.get_value() > 0:
        return hours.get_value(), minutes.get_value(), seconds.get_value() - 1

    return hours.get_value(), minutes.get_value(), seconds.get_value()


def substract_local_time_from(h, m, s):
    hours = ClockHand(24, h)
    minutes = ClockHand(60, m)
    seconds = ClockHand(60, s)
    # print(f'end time:{hours}:{minutes}:{seconds}\ncurrent time: {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}')

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

    return hours.get_value(), minutes.get_value(), seconds.get_value()


def check_if_finished(countdown):
    global finished
    if (countdown[0] == 0 and
        countdown[1] == 0 and
            countdown[2] == 0):
        finished = True


def get_countdown(h, m, s):
    view = substract_local_time_from(h, m, s)
    check_if_finished(view)

    if finished:
        return 'finished'

    hours = ClockHand(24, view[0])
    minutes = ClockHand(60, view[1])

    advanced_hour = minutes.extra_value(1)
    minutes.advance_one()
    hours.advance(advanced_hour)

    if hours.get_value() == 0:
        return (f'{minutes.get_value()}')

    return (f'{hours.get_value()}:{minutes}')
