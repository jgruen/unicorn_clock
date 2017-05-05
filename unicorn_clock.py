#! /usr/bin/env python3
"""Displays a nice clock in various colors."""

import functools
import operator
import time

import unicornhat

def returns_zero(someval):
    """Always returns 0."""
    return 0

def grab_digit(some_time, field_name, the_op):
    """Grabs a digit from some_time.

    some_time: a time.time object
    field_name: the field name to pull from some_time that has the value
    the_op: operation (either operator.floordiv or operator.mod) for the value
            (div'd or mod'd by 10 to get the digit)

    Returns: the digit"""
    return the_op(getattr(some_time, field_name), 10)

# Map of column-number to callable to grab the decimal digit for that column
COLUMN_TO_DIGIT = {
    0: functools.partial(grab_digit, field_name="tm_sec",
                         the_op=operator.mod),
    1: functools.partial(grab_digit, field_name="tm_sec",
                         the_op=operator.floordiv),
    2: returns_zero,
    3: functools.partial(grab_digit, field_name="tm_min",
                         the_op=operator.mod),
    4: functools.partial(grab_digit, field_name="tm_min",
                         the_op=operator.floordiv),
    5: returns_zero,
    6: functools.partial(grab_digit, field_name="tm_hour",
                         the_op=operator.mod),
    7: functools.partial(grab_digit, field_name="tm_hour",
                         the_op=operator.floordiv),
}

def get_pixel_for_time(some_time, column, row):
    """Returns 1 or 0 for a pixel for the given time.time some_time.

    column: the desired column
    row: the desired row"""
    return 0 if ((COLUMN_TO_DIGIT[column](some_time) & (1 << row)) == 0) else 1

unicornhat.set_layout(unicornhat.PHAT)
unicornhat.brightness(0.5)

old_snapshot = None
while True:
    time.sleep(0.1)
    snapshot = time.localtime()
    if snapshot == old_snapshot:
        # second didn't roll over yet
        continue
    for column in range(8):
        for row in range(4):
            unicornhat.set_pixel(column, row,
                                 (get_pixel_for_time(snapshot, column, row) *
                                  100),
                                 0, 0)
    unicornhat.show()
    # debug only
    print(time.asctime(snapshot))
    old_snapshot = snapshot
