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

    # Format filename in case user omits suffix.
    if not _file_name.endswith(".json"):
       _file_name = (_file_name + ".json")

    # create path to files.
    path = Path(RESOURCES / _file_name)
    with path.open() as f:
        data = json.load(f)
        world_size = tuple(data["world_size"])                              # Format world size to tuple.
        population = {}
        for coordinates, cell in data["population"].items():
            coords = ast.literal_eval(coordinates)                          # Format cell coordinates to tuple.
            cell_dict = {}
            if cell is None:
                population[coords] = None                                   # Add rim-cells to population dictionary.
                continue
            cell_dict["state"] = cell["state"]                              # Add cell states to cell dictionary.
            formatted_neighbours = [tuple(n) for n in cell["neighbours"]]   # Format list of tuple neighbours.
            cell_dict["neighbours"] = formatted_neighbours                  # Add neighbours to cell dictionary.
            population[coords] = cell_dict            # Add coordinates and cell dictionary to population dictionary.
    return (population, world_size)


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """

    # Set up logger at info level.
    gol_logger = logging.getLogger("gol_logger")
    gol_logger.setLevel(logging.INFO)

    # Set log path and open in write mode.
    path = Path(RESOURCES / "gol.log")
    file_handler = logging.FileHandler(path, mode="w")
    gol_logger.addHandler(file_handler)

    return gol_logger


def simulation_decorator(_func):
    """ Function decorator, used to run full extent of simulation. """

    gol_logger = create_logger()

    def wrapper_function(_generations: int, _population: dict, _world_size: tuple):
        """ Wrapper function, calculates log information and calls decorated function """
        for generation in range(0, _generations):
            cb.clear_console()

            # Calculate amount of cells in the population, rim cells excluded.
            population = len(_population) - ((_world_size[0] * 2) + (_world_size[1] * 2) - 4)

            alive = 0       # Alive counter.
            elders = 0      # Elder counter.
            p_elders = 0    # Prime elders counter.
            dead = 0        # Dead counter.
            for coords, cell in _population.items():
                if cell is None:
                    continue

                if cell["state"] != cb.STATE_DEAD:
                    alive = alive + 1
                if cell["state"] == cb.STATE_ELDER:
                    elders = elders + 1
                if cell["state"] == cb.STATE_PRIME_ELDER:
                    p_elders = p_elders + 1
                elif cell["state"] == cb.STATE_DEAD:
                    dead = dead + 1

            # Format logger.
            gol_logger.info(f"GENERATION {generation}\n  Population: {population}\n  Alive: {alive}\n  "
                            f"Elders: {elders}\n  Prime Elders: {p_elders}\n  Dead: {dead}")

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
        # Raise AssertionError if there are more or less than two values or if empty string in width_height list.
        assert len(width_height) == 2 and "" not in width_height, \
            "World size should contain width and height, separated by 'x'. Ex: '80x40'"

        # Convert to integers and place width and length in variables.
        width = int(width_height[0])
        height = int(width_height[1])

        # Raise ValueError if either value is below one.
        if height < 1 or width < 1:
            raise ValueError("Both width and height needs to have positive values above zero.")

    except (AssertionError, ValueError) as e:
        # Print different errors.
        print(e)
        print("Using default world size: 80x40")
        # Set default values.
        width = 80
        height= 40

    return (width, height)


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """

    population = {}

    pattern = cb.get_pattern(_seed_pattern, _world_size)
    width_coords = range(_world_size[0])
    height_coords = range(_world_size[1])
    coordinates = itertools.product(height_coords, width_coords)

    for y, x in coordinates:
        # Declare rim cells.
        cell = {}
        if x == 0 or y == 0 or x == (_world_size[0] -1) or y == (_world_size[1] -1):
            population[(y, x)] = None
            continue
        if pattern is not None:
            if (y, x) in pattern:
                state = cb.STATE_ALIVE
            else:
                state = cb.STATE_DEAD
        else:
            random_cell = random.randint(0, 20)
            if random_cell > 16:
                state = cb.STATE_ALIVE
            else:
                state = cb.STATE_DEAD

        cell["state"] = state
        cell["neighbours"] = calc_neighbour_positions((y, x))
        cell["age"] = 0
        population[(y, x)] = cell
    return population


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """

    y, x = _cell_coord
    N = (y, (x - 1))
    NE = ((y + 1), (x - 1))
    E = ((y + 1), x)
    SE = ((y + 1), (x + 1))
    S = (y, (x + 1))
    SW = ((y - 1), (x + 1))
    W = ((y - 1), x)
    NW = ((y - 1), (x - 1))
    return [N, NE, E, SE, S, SW, W, NW]


@simulation_decorator
def run_simulation(_generations: int, _population: dict, _world_size: tuple):
    """ Runs a tick in the simulation. """
    return update_world(_population, _world_size)


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """

    next_gen = {}
    for coords_, cell in _cur_gen.items():
        new_cell = {}
        if cell is None:
            cb.progress(cb.get_print_value(cb.STATE_RIM))
            if coords_[1] == (_world_size[0] - 1):
                cb.progress("\n")
            next_gen[coords_] = cell
            continue

        print_val = cb.get_print_value(cell["state"])
        cb.progress(print_val)

        if cell["state"] != cb.STATE_DEAD and count_alive_neighbours(cell["neighbours"], _cur_gen) == 2:
            new_cell["state"] = cb.STATE_ALIVE
        elif count_alive_neighbours(cell["neighbours"], _cur_gen) == 3:
            new_cell["state"] = cb.STATE_ALIVE
        else:
            new_cell["state"] = cb.STATE_DEAD

        if new_cell["state"] != cb.STATE_DEAD:
            new_cell["age"] = (cell["age"] + 1)
        else:
            new_cell["age"] = 0

        if new_cell["age"] > 10:
            new_cell["state"] = cb.STATE_PRIME_ELDER
        elif new_cell["age"] > 4:
            new_cell["state"] = cb.STATE_ELDER

        new_cell["neighbours"] = cell["neighbours"]
        next_gen[coords_] = new_cell
    return next_gen


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """

    living_counter = 0
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
