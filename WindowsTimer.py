import time
import logging
from ClockHand import *

logging.basicConfig(filename='ATC.log', level=logging.INFO,
                    format='{asctime} {levelname:<8} {message}',
                    style='{')

finished = False
paused = False


def add_current_time_to(h, m, s):

    seconds = ClockHand(60, time.localtime().tm_sec)
    minutes = ClockHand(60, time.localtime().tm_min)
    hours = ClockHand(24, time.localtime().tm_hour)

    advanced_sec = s
    advanced_min = m + seconds.extra_value(s)
    advanced_hour = h + minutes.extra_value(m)

    seconds.advance(advanced_sec)
    minutes.advance(advanced_min)
    hours.advance(advanced_hour)

    # updated part of the code - to avoid showing an extra minute for a sec when the user entries are: {1:0:0}
    # extra second is zero when we countdown only seconds
    # we take away one second when we start the countdown from more than a minute, thus we avoid showing extra minute for a sec
    # therefore these lines are a crutch
    extra_second = 1
    if h == 0 and m == 0:
        extra_second = 0

    sec = seconds.get_value() - extra_second
    min = minutes.get_value()
    hour = hours.get_value()

    if sec < 0:
        sec = 0

    return hour, min, sec

    # old part of the code (save for the rollback)
    # if m > 0 and seconds.get_value() > 0:
    #     return hours.get_value(), minutes.get_value(), seconds.get_value() - 1
    # return hours.get_value(), minutes.get_value(), seconds.get_value()


def time_diff(h, m, s, h2, m2, s2):
    # case when s > 59 is for paused mode when sum of (received seconds + pause_tics) is higher than limit
    if s > 59:
        seconds = ClockHand(60, 0)
        minutes = ClockHand(60, 0)
        hours = ClockHand(24, 0)

        advanced_sec = s
        advanced_min = m + seconds.extra_value(s)
        advanced_hour = h + minutes.extra_value(m)

        seconds.advance(advanced_sec)
        minutes.advance(advanced_min)
        hours.advance(advanced_hour)
        logging.info('\nTime End: "{}:{}:{}"'.format(hours, minutes, seconds))
    # normal case when we work with pause_tics == 0 can be addressed in a simpler way:
    else:
        seconds = ClockHand(60, s)
        minutes = ClockHand(60, m)
        hours = ClockHand(24, h)

    withdrawed_sec = s2
    withdrawed_min = m2 + seconds.extra_minus(s2)
    withdrawed_hour = h2 + \
        minutes.extra_minus(m2)

    # a tricky part of the code that no one knows why is needed but indeed is needed
    if minutes.get_value() == m2 and seconds.extra_minus(s2) > 0:
        withdrawed_hour = h2 + minutes.extra_minus(m2) + \
            seconds.extra_minus(s2)

    seconds.withdraw(withdrawed_sec)
    minutes.withdraw(withdrawed_min)
    hours.withdraw(withdrawed_hour)

    if seconds.get_value() < 6 or seconds.get_value() > 54:
        logging.info('\nTime End: "{}:{}:{}"\nLocal time: "{}:{}:{}"\nTime diff: "{}:{}:{}"'.format(h, m, s,
                                                                                                    h2, m2, s2,
                                                                                                    hours, minutes, seconds))

    return hours.get_value(), minutes.get_value(), seconds.get_value()


def check_if_finished(countdown):
    global finished
    if (countdown[0] == 0 and
        countdown[1] == 0 and
            countdown[2] == 0):
        finished = True


def get_countdown(h, m, s):

    view = time_diff(h, m, s, time.localtime().tm_hour,
                     time.localtime().tm_min, time.localtime().tm_sec)
                     
    check_if_finished(view)

    if finished:
        return 'finished'
    

    hours = ClockHand(24, view[0])
    minutes = ClockHand(60, view[1])

    advanced_hour = minutes.extra_value(1)
    minutes.advance_one()
    hours.advance(advanced_hour)

    if hours.get_value() == 0:
        if view[2] < 6 or view[2] > 54:
            logging.info('Output time: "{}:{}"'.format(minutes, view[2]))
        return (f'{minutes.get_value()}') # prod
        return (f'{minutes.get_value()}:{view[2]}') # test

    if view[2] < 6 or view[2] > 54:
        logging.info('Output time: "{}:{}:{}"'.format(hours, minutes, view[2]))
    return (f'{hours.get_value()}:{minutes}') # prod
    return (f'{hours.get_value()}:{minutes}:{view[2]}') # test


def stopwatch(h, m, s):
    timer = time_diff(time.localtime().tm_hour,
                     time.localtime().tm_min, time.localtime().tm_sec, h, m, s)

    minutes = ClockHand(60, timer[1])

    if timer[0] == 0:
        if timer[2] < 6 or timer[2] > 54:
            logging.info('Output time: "{}:{}"'.format(timer[1], timer[2]))
        return (f'{minutes.get_value()}') # prod
        return (f'{minutes.get_value()}:{timer[2]}') # test

    if timer[2] < 6 or timer[2] > 54:
        logging.info('Output time: "{}:{}:{}"'.format(timer[0], timer[1], timer[2]))
    return (f'{timer[0]}:{minutes}')


# OUTDATED DUE TO time_diff() func
# def substract_local_time_from(h, m, s):
#     hours = ClockHand(24, h)
#     minutes = ClockHand(60, m)
#     seconds = ClockHand(60, s)
#     withdrawed_sec = time.localtime().tm_sec
#     withdrawed_min = time.localtime().tm_min + seconds.extra_minus(time.localtime().tm_sec)
#     withdrawed_hour = time.localtime().tm_hour + \
#         minutes.extra_minus(time.localtime().tm_min)

#     # a tricky part of the code that no one knows why is needed but indeed is needed
#     if minutes.get_value() == time.localtime().tm_min and seconds.extra_minus(time.localtime().tm_sec) > 0:
#         withdrawed_hour = time.localtime().tm_hour + minutes.extra_minus(time.localtime().tm_min) + \
#             seconds.extra_minus(time.localtime().tm_sec)

#     seconds.withdraw(withdrawed_sec)
#     minutes.withdraw(withdrawed_min)
#     hours.withdraw(withdrawed_hour)

#     if seconds.get_value() < 6 or seconds.get_value() > 54:
#         logging.info('\nTime End: "{}:{}:{}"\nLocal time: "{}:{}:{}"\nTime diff: "{}:{}:{}"'.format(h, m, s,
#                                                                                                     time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec,
#                                                                                                     hours, minutes, seconds))

    # return hours.get_value(), minutes.get_value(), seconds.get_value()

# def stopwatch(h, m, s):
#     stopwatch_time = time_diff(time.localtime().tm_hour, time.localtime(
#     ).tm_min, time.localtime().tm_sec, h, m, s)
#     if stopwatch_time[0] == 0:
#         return (f'{stopwatch_time[1]}')
#     return (f'{stopwatch_time[0]}:{stopwatch_time[1]}')