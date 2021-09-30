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
    # TODO: Replace with implementation!
    with open("../_Resources/ass3_log_conf.json") as f:
        data = json.load(f)

    logging.config.dictConfig(data)
    return logging.getLogger("ass_3_logger")


def measurements_decorator(func):
    """Function decorator, used for time measurements."""
    @wraps(func)
    def wrapper(nth_nmb: int) -> tuple:
        # TODO: Replace with implementation!

        values = []
        starttime = timer()
        LOGGER.info("Starting measurements...")
        for num in range(nth_nmb, -1, -1):
            fib_val = func(num)
            values.append(fib_val)
            if num % 5 == 0:
                LOGGER.debug(f"{num}: {fib_val}")
        endtime = timer()
        duration = endtime - starttime
        return (duration, values)
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
    # TODO: Replace with implementation!
    memory = {0: 0, 1: 1}
    def fib(_n):
        if not _n in memory:
            memory[_n] = fib(_n - 1) + fib(_n - 2)
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
    # TODO: Replace with implementation!

    print(line)
    print(f"DURATION FOR EACH APPROACH WITHIN INTERVAL: {nth_value}-0".center(72), end="")
    print(line)

    print(f"{' ':>15}{'Seconds':>15}{'Milliseconds':>15}{'Microseconds':>15}{'Nanoseconds':>15}")

    for key, value in fib_details.items():
        sec = duration_format(value[0], "Seconds")
        millisec = duration_format(value[0], "Milliseconds")
        microsec = duration_format(value[0], "Microseconds")
        nanosec = duration_format(value[0], "Nanoseconds")
        fibs = key.title()
        print(f"{fibs:<15}{sec:>15}{millisec:>15}{microsec:>15}{nanosec:>15}")


def write_to_file(fib_details: dict):
    """Function to write information to file."""
    # TODO: Replace with implementation!

    for name, fibb in fib_details.items():
        with open(f'../_Resources/{name.replace(" ", "_")}.txt', "w") as file:
            values = fibb[1]
            seq_nr = []
            i = len(values)
            while i > 0:
                i = i - 1
                seq_nr.append(i)

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
