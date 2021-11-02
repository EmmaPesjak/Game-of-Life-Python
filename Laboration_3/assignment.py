#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 3
You find the description for the assignment in Moodle, where each detail regarding requirements
are stated. Below you find the inherent code, some of which fully defined. You add implementation
for those functions which are needed:

 - create_logger()
 - measurements_decorator(..)
 - fibonacci_memory(..)
 - print_statistics(..)
 - write_to_file(..)
"""

from pathlib import Path
from timeit import default_timer as timer
from functools import wraps
import argparse
import logging
import logging.config
import json
from timeit import default_timer as timer

__version__ = '1.1'
__desc__ = "Program used for measuríng execution time of various Fibonacci implementations!"

RESOURCES = Path(__file__).parent / "../_Resources/"


def create_logger() -> logging.Logger:
    """Create and return logger object."""

    with open(RESOURCES / "ass3_log_conf.json") as f:     # Open json file with custom logger configuration.
        data = json.load(f)                               # Load into variable.
    logging.config.dictConfig(data)                       # Set up logging with file in variable.
    return logging.getLogger("ass_3_logger")


def measurements_decorator(func):
    """Function decorator, used for time measurements."""
    @wraps(func)
    def wrapper(nth_nmb: int) -> tuple:
        values = []                                 # List of calculated fibonacci values.
        starttime = timer()                         # Timer for start time.
        LOGGER.info("Starting measurements...")     # Log info level logger for console output.
        for num in range(nth_nmb, -1, -1):          # Iterate from nth_nmb to 0.
            fib_val = func(num)                     # Call fibonacci function to calculate value.
            values.append(fib_val)                  # Add to list "values".
            if num % 5 == 0:                        # Log only every fifth iteration with logger below.
                LOGGER.debug(f"{num}: {fib_val}")   # Log debug level logger for file ass_3.log output.
        endtime = timer()                           # Timer for end time.
        duration = endtime - starttime
        return (duration, values)                   # Return tuple of duration and values.
    return wrapper


@measurements_decorator
def fibonacci_iterative(nth_nmb: int) -> int:
    """An iterative approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    old, new = 0, 1
    if nth_nmb in (0, 1):
        return nth_nmb
    for __ in range(nth_nmb - 1):
        old, new = new, old + new
    return new


@measurements_decorator
def fibonacci_recursive(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    def fib(_n):
        return _n if _n <= 1 else fib(_n - 1) + fib(_n - 2)
    return fib(nth_nmb)


@measurements_decorator
def fibonacci_memory(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value, storing those already calculated."""
    memory = {0: 0, 1: 1}   #Dictionary starts with values 0 and 1 to avoid RecursionError
    def fib(_n):
        if not _n in memory:                            # If not already in dictionary, do calculation below.
            memory[_n] = fib(_n - 1) + fib(_n - 2)      # Add key and value to dictionary.
        return memory[_n]
    return fib(nth_nmb)


def duration_format(duration: float, precision: str) -> str:
    """Function to convert number into string. Switcher is dictionary type here.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    switcher = {
        'Seconds': "{:.5f}".format(duration),
        'Milliseconds': "{:.5f}".format(duration * 1_000),
        'Microseconds': "{:.1f}".format(duration * 1_000_000),
        'Nanoseconds': "{:d}".format(int(duration * 1_000_000_000))
    }

    # get() method of dictionary data type returns value of passed argument if it is present in
    # dictionary otherwise second argument will be assigned as default value of passed argument
    return switcher.get(precision, "nothing")


def print_statistics(fib_details: dict, nth_value: int):
    """Function which handles printing to console."""
    line = '\n' + ("---------------" * 5)

    print(line)
    # Print centered header.
    print(f"DURATION FOR EACH APPROACH WITHIN INTERVAL: {nth_value}-0".center(72), end="")
    print(line)
    # Print right justified column headers.
    print(f"{' ':>15}{'Seconds':>15}{'Milliseconds':>15}{'Microseconds':>15}{'Nanoseconds':>15}")

    # Loop over fib_details dictionary to get duration times and row headers.
    for key, value in fib_details.items():
        # Call duration_format to format duration times.
        sec = duration_format(value[0], "Seconds")
        millisec = duration_format(value[0], "Milliseconds")
        microsec = duration_format(value[0], "Microseconds")
        nanosec = duration_format(value[0], "Nanoseconds")
        # Variable for row header.
        fibs = key.title()
        # Print left justified row header and left justified duration times.
        print(f"{fibs:<15}{sec:>15}{millisec:>15}{microsec:>15}{nanosec:>15}")


def write_to_file(fib_details: dict):
    """Function to write information to file."""
    for name, fibb in fib_details.items():
        with open(RESOURCES / f'{name.replace(" ", "_")}.txt', "w") as file:  # Open/create file in write mode.
            values = fibb[1]        # Make list for fibonacci values.
            seq_nr = []             # Make list of sequence numbers.
            i = len(values)         # Variable to count amount of fibonacci values.

            # Loop to append sequence number to list, from nth_nmb to 0.
            while i > 0:
                i = i - 1
                seq_nr.append(i)

            # Zip sequence number and fibonacci value and then write to file.
            zipped = zip(seq_nr, values)
            for sequence, value in zipped:
                file.write(f"{sequence}: {value}\n")


def main():
    """The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    epilog = "DT179G Assignment 3 v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('nth', metavar='nth', type=int, nargs='?', default=30,
                        help="nth Fibonacci sequence to find.")

    global LOGGER  # ignore warnings raised from linters, such as PyLint!
    LOGGER = create_logger()

    args = parser.parse_args()
    nth_value = args.nth  # nth value to sequence. Will fallback on default value!

    fib_details = {  # store measurement information in a dictionary
        'fib iteration': fibonacci_iterative(nth_value),
        'fib recursion': fibonacci_recursive(nth_value),
        'fib memory': fibonacci_memory(nth_value)
    }

    print_statistics(fib_details, nth_value)    # print information in console
    write_to_file(fib_details)                  # write data files


if __name__ == "__main__":
    main()
