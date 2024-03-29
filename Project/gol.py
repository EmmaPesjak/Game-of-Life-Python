#!/usr/bin/env python
"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead (populated or unpopulated).
Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

****************************************************************************************************
   1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
   2. Any live cell with two or three live neighbours lives on to the next generation.
   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
****************************************************************************************************

The initial pattern constitutes the seed of the system.

The first generation is created by applying the above rules simultaneously to every cell in the
seed—births and deaths occur simultaneously, and the discrete moment at which this happens is
sometimes called a tick. The rules continue to be applied repeatedly to create further generations.

You run this script as a module:
    python -m Project.gol.py
"""

import argparse
import ast
import random
import json
import logging
import itertools
from pathlib import Path
from ast import literal_eval
from time import sleep

import Project.code_base as cb

__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"


# -----------------------------------------
# IMPLEMENTATIONS FOR HIGHER GRADES, C - B
# -----------------------------------------

def load_seed_from_file(_file_name: str) -> tuple:
    """ Load population seed from file. Returns tuple: population (dict) and world_size (tuple). """

    # Format filename in case user omits the suffix.
    if not _file_name.endswith(".json"):
        _file_name = (_file_name + ".json")

    # Create path to the file, open the file and read the data.
    path = Path(RESOURCES / _file_name)
    with path.open() as f:
        data = json.load(f)

        # Convert world size to tuple.
        world_size = tuple(data["world_size"])

        # Create population dictionary, loop over JSON population dictionary items.
        population = {}
        for json_coordinates, json_cell in data["population"].items():
            # Convert string coordinates to tuple.
            coordinates = ast.literal_eval(json_coordinates)
            # Set rim cell to value None and continue
            if json_cell is None:
                population[coordinates] = None
                continue

            # Store cell state in a new cell dictionary, convert neighbours from JSON
            # file to list of tuples and store. Add age and store all information in
            # the new population dictionary.
            cell = {
                "state": json_cell["state"],
                "neighbours": [tuple(n) for n in json_cell["neighbours"]],
                "age": 0
            }
            population[coordinates] = cell

    return tuple([population, world_size])


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """

    # Set up the logger at info level.
    gol_logger = logging.getLogger("gol_logger")
    gol_logger.setLevel(logging.INFO)

    # Set log path, configure file handler at info level and see to that the file
    # will be opened in write mode.
    path = Path(RESOURCES / "gol.log")
    file_handler = logging.FileHandler(path, mode="w")
    gol_logger.addHandler(file_handler)

    return gol_logger


def simulation_decorator(_func):
    """ Function decorator, used to run full extent of simulation. """
    gol_logger = create_logger()

    def wrapper_function(_generations: int, _population: dict, _world_size: tuple):
        """ Wrapper function, calculates log information and calls decorated function """

        # Iterate over each generation.
        for generation in range(0, _generations):
            cb.clear_console()

            # Calculate amount of cells in the population, rim cells excluded.
            population = len(_population) - ((_world_size[0] * 2) + (_world_size[1] * 2) - 4)

            alive = 0       # Alive counter.
            elders = 0      # Elder counter.
            p_elders = 0    # Prime elder counter.
            dead = 0        # Dead counter.

            # Increment each counter for each possible cell state, elders and prime
            # elders also count as alive, skip rim cells.
            for coords, cell in _population.items():
                if cell is None:
                    continue

                if cell["state"] != cb.STATE_DEAD:
                    alive = alive + 1

                if cell["state"] == cb.STATE_ELDER:
                    elders = elders + 1
                elif cell["state"] == cb.STATE_PRIME_ELDER:
                    p_elders = p_elders + 1
                elif cell["state"] == cb.STATE_DEAD:
                    dead = dead + 1

            # Format logger output.
            gol_logger.info(f"GENERATION {generation}\n  Population: {population}\n  "
                            f"Alive: {alive}\n  Elders: {elders}\n  Prime Elders: "
                            f"{p_elders}\n  Dead: {dead}")

            # Call decorated function and store the updated population states.
            _population = _func(generation, _population, _world_size)
            sleep(0.2)

    return wrapper_function


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """

    # Split input string with "x" to list.
    width_height = _arg.split("x")

    try:
        # Raise AssertionError if there are more or less than two values or if empty string
        # in width_height list.
        assert len(width_height) == 2 and "" not in width_height, \
            "World size should contain width and height, separated by 'x'. Ex: '80x40'"

        # Convert to integers and place width and length in variables.
        width = int(width_height[0])
        height = int(width_height[1])

        # Raise ValueError if either value is below one, zero or negative world size is not valid.
        if height < 1 or width < 1:
            raise ValueError("Both width and height needs to have positive values above zero.")

    # To continue with default values on bad input, catch input errors, print them, and
    # set default values.
    except (AssertionError, ValueError) as e:
        print(e)
        print("Using default world size: 80x40")
        width = 80
        height = 40

    return tuple([width, height])


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """

    population = {}     # Dictionary for population.

    # By default no pattern is used. If seed pattern argument is given,
    # get pattern from code base.
    pattern = None
    if _seed_pattern is not None:
        pattern = cb.get_pattern(_seed_pattern, _world_size)

    # Create ranges of width and height from world size, then create each
    # coordinate by taking the product of the ranges.
    width_range = range(_world_size[0])
    height_range = range(_world_size[1])
    # Height and width are flipped to conform with seed patterns in code base.
    coordinates = itertools.product(height_range, width_range)

    # Loop over each cell with their coordinates, and set cell state, either by
    # pattern or randomized. Axes are flipped (y, x) to conform with provided
    # seed patterns in code base.
    for y, x in coordinates:
        # Check if coordinate is at outer boundaries, if so, set rim cell
        # i.e. None and continue.
        if x == 0 or y == 0 or x == (_world_size[0] - 1) or y == (_world_size[1] - 1):
            population[(y, x)] = None
            continue

        # In case of seed pattern, set cell state to live or dead according to
        # coordinates in pattern.
        if pattern is not None:
            if (y, x) in pattern:
                state = cb.STATE_ALIVE
            else:
                state = cb.STATE_DEAD

        # Randomize cell state if no pattern is to be used.
        else:
            random_state = random.randint(0, 20)
            if random_state > 16:
                state = cb.STATE_ALIVE
            else:
                state = cb.STATE_DEAD

        # Map cell state, neighbours and age to cell dictionary, then map coordinates
        # and cell dictionary to population dictionary.
        cell = {
            "state": state,
            "neighbours": calc_neighbour_positions((y, x)),
            "age": 0
        }
        population[(y, x)] = cell
    return population


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """

    # Axes are flipped (y, x) to conform with provided seed patterns in code base.
    y, x = _cell_coord
    return [(y, (x - 1)), ((y + 1), (x - 1)), ((y + 1), x), ((y + 1), (x + 1)), (y, (x + 1)),
            ((y - 1), (x + 1)), ((y - 1), x), ((y - 1), (x - 1))]


@simulation_decorator
def run_simulation(_generations: int, _population: dict, _world_size: tuple):
    """ Runs a tick in the simulation. """
    return update_world(_population, _world_size)


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """
    next_gen = {}   # Create dictionary for next generation.

    # Loop over current cells and coordinates to print current cell state, and set
    # the state and age for next generation.
    for coords, cell in _cur_gen.items():
        # Print rim cell, print new line after every last rim cell of each row,
        # set the coordinate to rim cell in next generation and continue.
        # Cell coordinates from dictionary have flipped axes, hence coords[1].
        if cell is None:
            cb.progress(cb.get_print_value(cb.STATE_RIM))
            if coords[1] == (_world_size[0] - 1):
                cb.progress("\n")
            next_gen[coords] = cell
            continue

        # Print cell that is not rim cell.
        cb.progress(cb.get_print_value(cell["state"]))

        # Create new cell for next generation with default values.
        new_cell = {
            "state": cb.STATE_DEAD,
            "neighbours": cell["neighbours"],
            "age": 0
        }

        # Count alive neighbours and check if the count fulfils the survival
        # requirements for next generation.
        alive_neighbour_count = count_alive_neighbours(cell["neighbours"], _cur_gen)
        if (cell["state"] != cb.STATE_DEAD and alive_neighbour_count == 2)\
                or (alive_neighbour_count == 3):

            # If cell is not a newborn, i.e. cell was alive in previous generation;
            # increment cell age by 1.
            if cell["state"] != cb.STATE_DEAD:
                new_cell["age"] = (cell["age"] + 1)

            # Determine if cell should be prime elder, elder or just alive by
            # checking the new age.
            if new_cell["age"] > 10:
                new_cell["state"] = cb.STATE_PRIME_ELDER
            elif new_cell["age"] > 5:
                new_cell["state"] = cb.STATE_ELDER
            else:
                new_cell["state"] = cb.STATE_ALIVE

        # Store the new cell in the next generation dictionary.
        next_gen[coords] = new_cell
    return next_gen


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """
    living_counter = 0
    # Loop over each neighbour and increment living counter for each living neighbour.
    for neighbour in _neighbours:
        if _cells[neighbour] is None:
            continue
        if _cells[neighbour]["state"] != cb.STATE_DEAD:
            living_counter = living_counter + 1

    return living_counter


def main():
    """ The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!! """
    epilog = "DT179G Project v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-g', '--generations', dest='generations', type=int, default=50,
                        help='Amount of generations the simulation should run. Defaults to 50.')
    parser.add_argument('-s', '--seed', dest='seed', type=str,
                        help='Starting seed. If omitted, a randomized seed will be used.')
    parser.add_argument('-ws', '--worldsize', dest='worldsize', type=str, default='80x40',
                        help='Size of the world, in terms of width and height. Defaults to 80x40.')
    parser.add_argument('-f', '--file', dest='file', type=str,
                        help='Load starting seed from file.')

    args = parser.parse_args()

    try:
        if not args.file:
            raise AssertionError
        population, world_size = load_seed_from_file(args.file)
    except (AssertionError, FileNotFoundError):
        world_size = parse_world_size_arg(args.worldsize)
        population = populate_world(world_size, args.seed)

    run_simulation(args.generations, population, world_size)


if __name__ == "__main__":
    main()
