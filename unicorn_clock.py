#! /usr/bin/env python3
"""Displays a nice clock in various colors."""

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
    0: partial(grab_digit, field_name="tm_hour", the_op=operator.floordiv),
    1: partial(grab_digit, field_name="tm_hour", the_op=operator.mod),
    2: returns_zero,
    3: partial(grab_digit, field_name="tm_min", the_op=operator.floordiv),
    4: partial(grab_digit, field_name="tm_min", the_op=operator.mod),
    5: returns_zero,
    6: partial(grab_digit, field_name="tm_sec", the_op=operator.floordiv),
    7: partial(grab_digit, field_name="tm_sec", the_op=operator.mod),
}

def get_pixel_for_time(some_time, column, row):
    """Returns 1 or 0 for a pixel for the given time.time some_time.

    column: the desired column
    row: the desired row"""
    return 0 if ((COLUMN_TO_DIGIT[column](some_time) & (1 << row)) == 0) else 1

unicornhat.set_layout(unicornhat.PHAT)
unicornhat.brightness(0.5)
while True:
    snapshot = time.localtime()
    for column in range(8):
        for row in range(4):
            unicornhat.set_pixel(column, row,
                                 get_pixel_for_time(snapshot, column, row),
                                 0, 0)
    unicornhat.show()
    time.sleep(0.1)
